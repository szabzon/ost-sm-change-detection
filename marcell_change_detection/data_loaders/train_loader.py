import os
import pandas as pd
from sklearn.model_selection import train_test_split


class TrainLoader:
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