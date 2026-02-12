import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "email_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "email_vectorizer.pkl")


class EmailAnalyzer:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.vectorizer = joblib.load(VECTORIZER_PATH)

    def analyze(self, subject: str, body: str):
        text = f"{subject} {body}"

        # Transform to TF-IDF
        features = self.vectorizer.transform([text])

        # Probability of spam/phishing
        prob = self.model.predict_proba(features)[0][1]

        verdict = "phishing" if prob > 0.6 else "safe"

        score = int(prob * 100)

        details = []
        if prob > 0.8:
            details.append("High spam/phishing probability")
        elif prob > 0.6:
            details.append("Suspicious email content")
        else:
            details.append("Looks safe")

        return {
            "score": score,
            "verdict": verdict,
            "details": details,
            "ml_probability": float(prob)
        }
