import pandas as pd
from kafka import KafkaProducer
from time import sleep


class KafkaDataStreamer:
    """
    Class to stream data to Kafka
    The data is read from a CSV file and sent to Kafka topic
    """
    def __init__(self, bootstrap_servers, topic):
        """
        Initialize the Kafka producer
        :param bootstrap_servers: bootstrap servers for the Kafka cluster
        :param topic: Kafka topic to which the data is sent
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        # Initialize the Kafka producer
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, api_version=(0, 10, 1))

    def stream_data(self, data_paths):
        """
        Read the data from the CSV file and send it to Kafka topic
        :param data_path: the path to the CSV file
        :return:
        """
        for data_path in data_paths:
            data = pd.read_csv(data_path)
            for i, row in data.iterrows():
                message = row.to_json()
                self.producer.send(self.topic, value=message.encode('utf-8'))
                if i % 10000 == 0:
                    print('Sent message #{}'.format(i))