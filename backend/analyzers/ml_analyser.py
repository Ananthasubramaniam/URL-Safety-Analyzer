

import joblib
import os
from utils.feature_extractor import FeatureExtractor

# Get model path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_model.pkl")

# Load model once when file starts
model = joblib.load(MODEL_PATH)


def ml_predict(url: str) -> dict:
    """
    Takes a URL and returns ML phishing score.
    """

    try:
        # Step 1: Convert URL to numeric features
        extractor = FeatureExtractor()              
        features = extractor.extract_features(url) 

        # Step 2: Model prediction
        probability = model.predict_proba([features])[0][1]

        # Step 3: Convert to score
        score = int(probability * 100)

        return {
            "ml_score": score,
            "ml_probability": round(probability, 2)
        }

    except Exception as e:
        return {
            "ml_score": 0,
            "error": str(e)
        }
