import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "datasets", "email_raw")
OUT_PATH = os.path.join(BASE_DIR, "datasets", "processed", "email_training_data.csv")

def load_spamassassin():
    df = pd.read_csv(os.path.join(RAW_DIR, "SpamAssasin.csv"))
    df["text"] = (
        df["subject"].fillna("") + " " +
        df["body"].fillna("")
    )
    df = df[["text", "label"]]
    return df

def load_enron():
    df = pd.read_csv(os.path.join(RAW_DIR, "Enron.csv"))
    df["text"] = (
        df["subject"].fillna("") + " " +
        df["body"].fillna("")
    )
    df = df[["text", "label"]]
    return df

def load_phishing():
    df = pd.read_csv(os.path.join(RAW_DIR, "phishing_email.csv"))
    df["text"] = df["text_combined"].fillna("")
    df = df[["text", "label"]]
    return df

print("Loading datasets...")

spam = load_spamassassin()
enron = load_enron()
phish = load_phishing()

print("Merging...")
merged = pd.concat([spam, enron, phish], ignore_index=True)

print("Saving unified dataset...")
merged.to_csv(OUT_PATH, index=False)

print("Done!")
