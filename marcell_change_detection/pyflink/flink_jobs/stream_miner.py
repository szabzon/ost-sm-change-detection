

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
from pyflink.common import Configuration

import pandas as pd
from sklearn.metrics import accuracy_score
from ../../drift_detectors import DDM, BasicWindowDDM, HDDM_W
from sklearn.ensemble import RandomForestClassifier
import json
from joblib import load


class DriftDetectionProcessFunction(ProcessFunction):
    def __init__(self):
        # Initialize the ProcessFunction
        super().__init__()

    def open(self, runtime_context):
        # Initialize the model and the drift detector
        self.clf = trained_model
        self.ddm = chosen_drift_detector

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
env.add_jars(
    "file:///home/pyflink/flink/flink_dependencies/flink-connector-kafka.jar",
    "file:///home/pyflink/flink/flink_dependencies/kafka-clients.jar"
)

# Define the Kafka properties
# set serializer
# set deserializer
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

# Load the trained model
model_path = 'marcell_change_detection/models/basic_model.joblib'
trained_model = load(model_path)

# Load the drift detector
# Change the drift detector here!
chosen_drift_detector = DDM()

# Add the Kafka consumer to the environment
input_stream = env.add_source(consumer)

# Apply the ProcessFunction to the input stream
processed_stream = input_stream.process(DriftDetectionProcessFunction())

# Create a Kafka producer
producer = FlinkKafkaProducer(
    'hai-results',
    SimpleStringSchema(),
    producer_config=kafka_properties
)

# Add the Kafka producer to the environment
processed_stream.add_sink(producer)

# Execute the Flink job
env.execute("PyFlink Drift Detection")
