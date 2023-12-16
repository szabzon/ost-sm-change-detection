from sklearn.metrics import accuracy_score


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



