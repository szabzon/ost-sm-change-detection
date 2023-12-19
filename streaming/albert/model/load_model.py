import joblib

def get_model():
    # Load the model from the file
    model = joblib.load('../../albert/model/random_forest_model.joblib')
    return model
