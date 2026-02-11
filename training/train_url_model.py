# training/train_url_model.py

import os
import sys
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.utils.feature_extractor import FeatureExtractor


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "raw_urls.csv")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "backend", "models", "phishing_model.pkl")


def main():
    print("Loading dataset...")
    data = pd.read_csv(DATA_PATH)

    extractor = FeatureExtractor()

    X = []
    y = []

    print("Extracting features...")
    for _, row in data.iterrows():
        url = row['url']
        label = row['label']

        features = extractor.extract_features(url)
        X.append(features)
        y.append(label)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    print("Evaluating...")
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print("Accuracy:", acc)

    print("Saving model...")
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump(model, MODEL_SAVE_PATH)

    print("Model saved at:", MODEL_SAVE_PATH)


if __name__ == "__main__":
    main()
