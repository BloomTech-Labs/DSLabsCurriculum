import datetime
from typing import List, Tuple

import joblib
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class Model:

    def __init__(self, df: DataFrame, target: str, features: List[str]):
        X_train, X_test, y_train, y_test = train_test_split(
            df[features],
            df[target],
            test_size=0.20,
            random_state=831592708,
            stratify=df[target],
        )
        self.model = RandomForestClassifier(
            max_depth=10,
            max_features=3,
            n_estimators=66,
            n_jobs=-1,
            random_state=831592708,
        )
        self.model.fit(X_train, y_train)
        baseline_score = 1 / df[target].unique().shape[0]
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info = {
            "Model Name": "Random Forest Classifier",
            "Train/Total Count": f"{X_train.shape[0]}/{df.shape[0]}",
            "Baseline Score": f"{baseline_score:.1%}",
            "Training Score": f"{train_score:.1%}",
            "Testing Score": f"{test_score:.1%}",
            "Timestamp": timestamp,
        }

    def __call__(self, feature_basis: DataFrame) -> List[Tuple]:
        prediction = self.model.predict(feature_basis)
        probability = self.model.predict_proba(feature_basis)
        return list(zip(prediction, map(max, probability)))

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.info.items())

    def __str__(self):
        return repr(self)

    def save(self, filepath):
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath: str):
        return joblib.load(filepath)
