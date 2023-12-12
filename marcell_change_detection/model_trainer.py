'''
def get_data(data_folder, data_filenames):
    """
    Get the training data from the csv files in the data folder
    Join the dataframes from the different files
    """
    data_list = list()
    for data_filename in data_filenames:
        data_path = os.path.join(data_folder, data_filename).replace(os.sep, '/')
        data_list.append(pd.read_csv(data_path, index_col=0))

    data_frame = pd.concat(data_list, axis=0, ignore_index=True)

    return data_frame
#%%
# import csv training data
data_folder = '../../hai_dataset/hai/hai-21.03'
data_filenames = ['train1.csv', 'train2.csv', 'train3.csv']
df = get_data(data_folder, data_filenames)
#%%
# split into train and test
label_columns = ['attack', 'attack_P1', 'attack_P2', 'attack_P3']
X_train, X_test, y_train, y_test = train_test_split(df.drop(label_columns, axis=1), df[label_columns], test_size=0.33, random_state=42)
#%%
# save the column names to a list
column_names = X_train.columns.tolist()
print(column_names)
#%%
y_train.head()
#%%
# initialize classifier
clf = RandomForestClassifier()
#%%
# do the initial training
clf.fit(X_train, y_train)
#%%
# get the initial accuracy
y_pred = clf.predict(X_test)
accuracy_score(y_test, y_pred)
'''


import os
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class DataLoaderProcessor:
    """
    Class for loading the training data and preparing it for training
    """
    def __init__(self, data_folder, data_filenames, label_columns):
        self.data_folder = data_folder
        self.data_filenames = data_filenames
        self.label_columns = label_columns

    def get_data(self):
        """
        Get the training data from the csv files in the data folder
        Join the dataframes from the different files
        """
        data_list = list()
        for data_filename in self.data_filenames:
            data_path = os.path.join(self.data_folder, data_filename).replace(os.sep, '/')
            data_list.append(pd.read_csv(data_path, index_col=0))

        data_frame = pd.concat(data_list, axis=0, ignore_index=True)

        return data_frame

    def split_data(self, data_frame, test_size=0.33, random_state=42):
        """
        Split the data into train and test
        """
        X_train, X_test, y_train, y_test = train_test_split(data_frame.drop(self.label_columns, axis=1), data_frame[self.label_columns], test_size=test_size, random_state=random_state)

        return X_train, X_test, y_train, y_test

    def get_column_names(self, data_frame):
        """
        Get the column names from the data frame
        """
        column_names = data_frame.columns.tolist()

        return column_names


class ModelTrainerTester:
    """
    Class for training the model
    """
    def __init__(self, classifier, X_train, y_train):
        self.classifier = classifier
        self.X_train = X_train
        self.y_train = y_train

    def train_model(self):
        """
        Train the model
        """
        self.classifier.fit(self.X_train, self.y_train)

        return self.classifier

    def test_model(self, X_test, y_test):
        """
        Test the model
        """
        y_pred = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        return y_pred, accuracy
