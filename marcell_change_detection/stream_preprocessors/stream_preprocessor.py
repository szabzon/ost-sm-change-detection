import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
import json


# Consume the unprocessed kafka stream
class StreamPreprocessor:
    def __init__(
            self,
            input_topic,
            output_topic,
            input_keys,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
    ):
        """
        Class for preprocessing the data from the kafka stream.
        Prepare the data for testing. Split the data to features and labels.
        :param input_topic: the topic to consume from
        :param output_topic: the topic to produce to
        :param input_keys: ordered list of keys in the input message
        :param bootstrap_servers: kafka bootstrap servers
        :param auto_offset_reset: auto offset
        """

        self.input_topic = input_topic
        self.output_topic = output_topic
        self.input_keys = input_keys
        self.consumer = KafkaConsumer(
            input_topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def map_keys(self, message, input_keys):

        """
        Map the keys from the input message to the output message.
        Split the data to features and labels.
        :param message: kafka message of type dict
        :param input_keys: ordered list of keys in the input message
        :return: output_dict: dict with keys 'time', 'features', 'labels'
        """
        # print(message)
        output_dict = {
            'time': message.pop('time'),
            'features': {},
            'labels': {}
        }
        for key in input_keys:
            if key == 'time':
                continue
            if key.startswith('attack'):
                output_dict['labels'][key] = message.pop(key)
            else:
                output_dict['features'][key] = message.pop(key)

        return output_dict

    def prepare_data(self, message_dict):
        """
        Prepare the data for testing.
        :param message_dict: kafka message of type dict
        :return: a dict of preprocessed data
        """
        # fill missing values with 0
        for key in message_dict:
            if message_dict[key] == '':
                message_dict[key] = 0

        return message_dict

    def run(self):
        """
        Run the stream preprocessor.
        :return:
        """
        for i, message in enumerate(self.consumer):
            preprocessed_message = self.prepare_data(message.value)
            output_dict = self.map_keys(preprocessed_message, self.input_keys)
            self.producer.send(self.output_topic, json.dumps(output_dict).encode('utf-8'))
            if i % 10000 == 0:
                print(f'Processed {i} messages')
