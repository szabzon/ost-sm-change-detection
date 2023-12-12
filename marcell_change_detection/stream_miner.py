'''
input_topic = 'hai-preprocessed'
input_bootstrap_servers = ['localhost:9092']
consumer = StreamConsumer(input_topic, input_bootstrap_servers)
#%%
output_topic = 'hai-results'
output_bootstrap_servers = ['localhost:9092']
producer = ResultsProducer(output_topic, output_bootstrap_servers)
#%%
# initialize drift detector
ddm = DDM()

# consume the streamed data from kafka and detect drift
msg = consumer.consume_next()
i = 0
while msg:
    # get the data from the message
    data = msg.value
    #print(data['features'])
    # convert the dictionary to a dataframe
    X = pd.DataFrame(data['features'], index=[0])
    # get the labels
    y = pd.DataFrame(data['labels'], index=[0])
    # predict the labels
    y_pred = clf.predict(X)
    # get the accuracy
    accuracy = accuracy_score(y, y_pred)
    # detect drift
    ddm.add_element(accuracy)
    warning_detected = ddm.detected_warning_zone()
    drift_detected = ddm.detected_change()
    
    # send the results
    producer.send({'accuracy': accuracy, 'warning_detected': warning_detected, 'drift_detected': drift_detected})
    
    # print the results
    """if accuracy < 0.5:
        print('Iteration {}'.format(i), 'Accuracy {}'.format(accuracy))
    """
    if i % 1000 == 0:
        print('Iteration {}'.format(i), 'Accuracy {}'.format(accuracy))
    if drift_detected:
        print(f'{datetime.now()} - accuracy: {accuracy} - drift detected: {drift_detected}')
    # get the next message
    msg = consumer.consume_next()
    i += 1
'''

import os
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from drift_detectors.ddm import DDM
from model_trainer import DataLoaderProcessor, ModelTrainerTester


"""
Class for mining the stream.
Load and process the data. Train the model, and test it. 
Consume the data from the stream and detect drift.
Use the drift detector to detect drift.
Produce the results.
"""

