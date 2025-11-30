import joblib
from model import Model, FEATURES


MODEL_PATH = 'models/brightpawn_model.joblib'


def train_and_save(df):
    clf = Model()
    metrics = clf.fit(df)
    joblib.dump(clf, MODEL_PATH)
    return metrics