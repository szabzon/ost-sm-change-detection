import os
from sklearn.model_selection import train_test_split
from functools import reduce
from pyspark.sql import DataFrame
import pandas as pd


class TrainLoaderPython:
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

    def preprocess_data(self, data_frame):
        """
        Prepare the data for training
        """
        data_frame = data_frame.dropna()
        data_frame = data_frame.drop_duplicates()
        data_frame = data_frame.reset_index(drop=True)
        # do more stuff here

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


class TrainLoaderSpark:
    def __init__(self, spark, data_folder, data_filenames, label_columns):
        """
        Class for loading the training data and preparing it for training
        """
        self.spark = spark
        self.data_folder = data_folder
        self.data_filenames = data_filenames
        self.label_columns = label_columns

    def get_data(self):
        """
        Get the training data from the csv files in the data folder
        Join the dataframes from the different files
        """
        data_list = []
        for data_filename in self.data_filenames:
            data_path = f"{self.data_folder}/{data_filename}"
            data_list.append(self.spark.read.csv(data_path, header=True, inferSchema=True))

        # join the dataframes
        data_frame = reduce(DataFrame.unionAll, data_list)

        return data_frame

    def preprocess_data(self, data_frame):
        """
        Prepare the data for training
        """
        # drop NAs
        processed_data = data_frame.dropna()

        return processed_data

    def split_data(self, data_frame, test_size=0.2, random_state=42):
        """
        Split the data into train and test
        :param data_frame: the data frame to split
        :param test_size: the size of the test set
        :param random_state: the random state for the split
        :return: the train and test data frames split into features and labels
        """

        # the label columns are known beforehand
        # the feature columns are all the columns except the label columns
        # get feature columns
        feature_columns = [col for col in data_frame.columns if col not in self.label_columns]

        # split the data into train and test
        train, test = data_frame.randomSplit([0.8, 0.2], seed=42)

        # split the train and test into features and labels
        X_train = train.select(feature_columns)
        X_test = test.select(feature_columns)
        y_train = train.select(self.label_columns)
        y_test = test.select(self.label_columns)

        return X_train, X_test, y_train, y_test

    def get_column_names(self, data_frame):
        """
        Get the column names from the data frame
        :param data_frame: the data frame to get the column names from
        """
        column_names = data_frame.columns.tolist()

        return column_names
