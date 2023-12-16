'''from data_loaders.stream_preprocessor import StreamPreprocessor

input_columns = ['time', 'P1_B2004', 'P1_B2016', 'P1_B3004', 'P1_B3005', 'P1_B4002', 'P1_B4005', 'P1_B400B', 'P1_B4022', 'P1_FCV01D', 'P1_FCV01Z', 'P1_FCV02D', 'P1_FCV02Z', 'P1_FCV03D', 'P1_FCV03Z', 'P1_FT01', 'P1_FT01Z', 'P1_FT02', 'P1_FT02Z', 'P1_FT03', 'P1_FT03Z', 'P1_LCV01D', 'P1_LCV01Z', 'P1_LIT01', 'P1_PCV01D', 'P1_PCV01Z', 'P1_PCV02D', 'P1_PCV02Z', 'P1_PIT01', 'P1_PIT02', 'P1_PP01AD', 'P1_PP01AR', 'P1_PP01BD', 'P1_PP01BR', 'P1_PP02D', 'P1_PP02R', 'P1_STSP', 'P1_TIT01', 'P1_TIT02', 'P2_24Vdc', 'P2_ASD', 'P2_AutoGO', 'P2_CO_rpm', 'P2_Emerg', 'P2_HILout', 'P2_MSD', 'P2_ManualGO', 'P2_OnOff', 'P2_RTR', 'P2_SIT01', 'P2_SIT02', 'P2_TripEx', 'P2_VT01', 'P2_VTR01', 'P2_VTR02', 'P2_VTR03', 'P2_VTR04', 'P2_VXT02', 'P2_VXT03', 'P2_VYT02', 'P2_VYT03', 'P3_FIT01', 'P3_LCP01D', 'P3_LCV01D', 'P3_LH', 'P3_LIT01', 'P3_LL', 'P3_PIT01', 'P4_HT_FD', 'P4_HT_LD', 'P4_HT_PO', 'P4_HT_PS', 'P4_LD', 'P4_ST_FD', 'P4_ST_GOV', 'P4_ST_LD', 'P4_ST_PO', 'P4_ST_PS', 'P4_ST_PT01', 'P4_ST_TT01', 'attack', 'attack_P1', 'attack_P2', 'attack_P3']

stream_preprocessor = StreamPreprocessor('hai-input', 'hai-preprocessed', input_columns)

stream_preprocessor.run()

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
                print(f'Processed {i} messages')'''
import json

import pandas as pd
# create a flink job that does the same thing as the stream preprocessor but in flink
import pyflink
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import ProcessFunction
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


# implement the process function
class StreamPreprocessorProcessFunction(ProcessFunction):
    """
    Class for preprocessing the stream in flink.
    Prepare the data for testing. Split the data to features and labels.
    """

    def open(self, runtime_context):
        """
        Open the process function
        :param runtime_context: the runtime context
        :return:
        """
        self.input_keys = input_columns

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

    def process_element(self, value, ctx: 'ProcessFunction.Context'):
        """
        Run the stream preprocessor for one element in the stream.
        Prepare the data for testing. Split the data to features and labels.
        :param value: the value of the element in the stream
        :param ctx: the context
        :return:
        """
        # print(value)
        data = json.loads(value)
        data = self.prepare_data(data)
        output_dict = self.map_keys(data, self.input_keys)
        ctx.output('hai-preprocessed', json.dumps(output_dict))


# set it up
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env.add_jars(
    "file:///home/pyflink/flink/flink_dependencies/flink-connector-kafka.jar",
    "file:///home/pyflink/flink/flink_dependencies/kafka-clients.jar"
)

# define the kafka properties
kafka_properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'flink-stream-preprocessor-job'
}

# create a kafka consumer
consumer = FlinkKafkaConsumer(
    'hai-input',
    SimpleStringSchema(),
    properties=kafka_properties
)

# create a kafka producer
producer = FlinkKafkaProducer(
    'hai-preprocessed',
    SimpleStringSchema(),
    producer_config=kafka_properties
)

# add the kafka consumer to the environment
input_stream = env.add_source(consumer)

# define the input columns
input_columns = ['time', 'P1_B2004', 'P1_B2016', 'P1_B3004', 'P1_B3005', 'P1_B4002', 'P1_B4005', 'P1_B400B', 'P1_B4022', 'P1_FCV01D', 'P1_FCV01Z', 'P1_FCV02D', 'P1_FCV02Z', 'P1_FCV03D', 'P1_FCV03Z', 'P1_FT01', 'P1_FT01Z', 'P1_FT02', 'P1_FT02Z', 'P1_FT03', 'P1_FT03Z', 'P1_LCV01D', 'P1_LCV01Z', 'P1_LIT01', 'P1_PCV01D', 'P1_PCV01Z', 'P1_PCV02D', 'P1_PCV02Z', 'P1_PIT01', 'P1_PIT02', 'P1_PP01AD', 'P1_PP01AR', 'P1_PP01BD', 'P1_PP01BR', 'P1_PP02D', 'P1_PP02R', 'P1_STSP', 'P1_TIT01', 'P1_TIT02', 'P2_24Vdc', 'P2_ASD', 'P2_AutoGO', 'P2_CO_rpm', 'P2_Emerg', 'P2_HILout', 'P2_MSD', 'P2_ManualGO', 'P2_OnOff', 'P2_RTR', 'P2_SIT01', 'P2_SIT02', 'P2_TripEx', 'P2_VT01', 'P2_VTR01', 'P2_VTR02', 'P2_VTR03', 'P2_VTR04', 'P2_VXT02', 'P2_VXT03', 'P2_VYT02', 'P2_VYT03', 'P3_FIT01', 'P3_LCP01D', 'P3_LCV01D', 'P3_LH', 'P3_LIT01', 'P3_LL', 'P3_PIT01', 'P4_HT_FD', 'P4_HT_LD', 'P4_HT_PO', 'P4_HT_PS', 'P4_LD', 'P4_ST_FD', 'P4_ST_GOV', 'P4_ST_LD', 'P4_ST_PO', 'P4_ST_PS', 'P4_ST_PT01', 'P4_ST_TT01', 'attack', 'attack_P1', 'attack_P2', 'attack_P3']

# apply the process function to the input stream
processed_stream = input_stream.process(StreamPreprocessorProcessFunction())

# add the kafka producer to the environment
processed_stream.add_sink(producer)

# execute the job
env.execute('Stream Preprocessor Job')

