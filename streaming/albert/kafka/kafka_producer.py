from kafka import KafkaProducer
import json

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

class KafkaDataStreamer:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        # Initialize the Kafka producer
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, 
                                      value_serializer=json_serializer,
                                      api_version=(0, 10, 1))

    def stream_data(self, data):
        for _, row in data.iterrows():
            message = row.to_dict()
            self.producer.send(self.topic, value=message)