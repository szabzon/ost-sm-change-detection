

"""
Class for mining the stream.
Load and process the data. Train the model, and test it. 
Consume the data from the stream and detect drift.
Use the drift detector to detect drift.
Produce the results.
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import ProcessFunction
from pyflink.common.serialization import SimpleStringSchema

import pandas as pd
from sklearn.metrics import accuracy_score
from drift_detectors.ddm import DDM
from drift_detectors.basic_window_ddm import BasicWindowDDM
from model_handlers.model_trainer import ModelTrainerTester
from sklearn.ensemble import RandomForestClassifier
import json
from data_loaders.train_loader import TrainLoader


class DriftDetectionProcessFunction(ProcessFunction):
    def __init__(self):
        # Initialize the ProcessFunction
        super().__init__()

    def load_data(self):
        # import csv training data
        data_folder = '../../hai_dataset/hai/hai-21.03'
        data_filenames = ['train1.csv', 'train2.csv', 'train3.csv']
        label_columns = ['attack', 'attack_P1', 'attack_P2', 'attack_P3']
        # Load the training data
        data_loader = TrainLoader(data_folder=data_folder, data_filenames=data_filenames, label_columns=label_columns)
        df = data_loader.get_data()
        return data_loader.split_data(data_frame=df)

    def train_model(self, X_train, X_test, y_train, y_test):
        # Train the classifier
        model_handler = ModelTrainerTester(classifier=self.clf, X_train=X_train, y_train=y_train)
        clf = model_handler.train_model()
        _, tr_accuracy = model_handler.test_model(X_test=X_test, y_test=y_test)
        return clf

    def open(self, runtime_context):
        # Initialize the model and the drift detector
        self.clf = RandomForestClassifier()
        self.ddm = DDM()

        X_train, X_test, y_train, y_test = self.load_data()
        self.clf = self.train_model(X_train, X_test, y_train, y_test)

    def process_element(self, value, ctx, collector):
        # Extract features and labels from the input value
        data = json.loads(value)
        X = pd.DataFrame(data['features'], index=[0])
        y = pd.DataFrame(data['labels'], index=[0])

        # Predict labels using the classifier
        y_pred = self.clf.predict(X)

        # Calculate accuracy
        accuracy = accuracy_score(y, y_pred)

        # Update the DDM model and check for drift
        self.ddm.add_element(accuracy)
        warning_detected = self.ddm.detected_warning_zone()
        drift_detected = self.ddm.detected_change()

        # Send the results to Kafka
        producer.send('hai-results', value={'accuracy': accuracy, 'warning_detected': warning_detected, 'drift_detected': drift_detected})

        '''# Print the results (optional)
        if ctx.get_current_key() % 1000 == 0:
            print('Iteration {}'.format(ctx.get_current_key()), 'Accuracy {}'.format(accuracy))
        if drift_detected:
            print(f'{datetime.now()} - accuracy: {accuracy} - drift detected: {drift_detected}')'''

# Set up the StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
env.get_config()
env.add_jars("file:///flink_dependencies/flink-connector-kafka.jar")
#env.add_classpaths("file:///flink-connector-kafka.jar")

# Define the Kafka properties
kafka_properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'flink-drift-detection-job'
}

# Create a Kafka consumer
consumer = FlinkKafkaConsumer(
    'hai-preprocessed',
    SimpleStringSchema(),
    properties=kafka_properties
)

# Add the Kafka consumer to the environment
input_stream = env.add_source(consumer)

# Apply the ProcessFunction to the input stream
processed_stream = input_stream.process(DriftDetectionProcessFunction())

# Create a Kafka producer
producer = FlinkKafkaProducer(
    'hai-results',
    SimpleStringSchema(),
    properties=kafka_properties
)

# Add the Kafka producer to the environment
processed_stream.add_sink(producer)

# Execute the Flink job
env.execute("PyFlink Drift Detection Example")
