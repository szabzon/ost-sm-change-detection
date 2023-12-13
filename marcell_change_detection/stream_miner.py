

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
from sklearn.ensemble import RandomForestClassifier
import json


class DriftDetectionProcessFunction(ProcessFunction):
    def open(self, runtime_context):
        # Initialize the classifier and DDM model
        self.clf = RandomForestClassifier()
        self.ddm = DDM()

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
env.add_jars("file:///flink-connector-kafka.jar")
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
