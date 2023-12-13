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

    def run(self):
        for i, message in enumerate(self.consumer):
            output_dict = self.map_keys(message.value, self.input_keys)
            self.producer.send(self.output_topic, json.dumps(output_dict).encode('utf-8'))
            if i % 10000 == 0:
                print(f'Processed {i} messages')