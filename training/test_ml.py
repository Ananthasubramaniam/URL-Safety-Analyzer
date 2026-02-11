import os
import sys
import joblib

# Fix imports
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from backend.utils.feature_extractor import FeatureExtractor

MODEL_PATH = os.path.join(BASE_DIR, "backend", "models", "phishing_model.pkl")

print("Loading model...")
model = joblib.load(MODEL_PATH)

extractor = FeatureExtractor()

while True:
    url = input("\nEnter URL (or 'exit'): ")

    if url == "exit":
        break

    features = extractor.extract_features(url)

    prob = model.predict_proba([features])[0][1]
    score = int(prob * 100)

    print("Phishing Probability:", round(prob, 2))
    print("Risk Score:", score)
