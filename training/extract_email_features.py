import os
import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "datasets", "processed", "email_training_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

  
    text = re.sub(r"[^a-z\s]", " ", text)

    
    text = re.sub(r"\s+", " ", text)

    return text.strip()


print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("Cleaning text...")
df["text"] = df["text"].apply(clean_text)

X_text = df["text"]
y = df["label"]


print("Vectorizing text...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,      
    ngram_range=(1, 2),     
    min_df=2               
)

X = vectorizer.fit_transform(X_text)


print("Saving sparse features...")
sparse.save_npz(os.path.join(OUTPUT_DIR, "email_features.npz"), X)

print("Saving labels...")
joblib.dump(y.values, os.path.join(OUTPUT_DIR, "email_labels.pkl"))

print("Saving vectorizer...")
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "email_vectorizer.pkl"))

print("Feature extraction complete!")
