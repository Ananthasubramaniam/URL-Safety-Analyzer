import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from scipy import sparse


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_PATH = os.path.join(BASE_DIR, "datasets", "processed", "email_features.npz")
LABEL_PATH = os.path.join(BASE_DIR, "datasets", "processed", "email_labels.pkl")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "email_model.pkl")


print("Loading features...")

X = sparse.load_npz(FEATURE_PATH)
y = joblib.load(LABEL_PATH)

print("Feature shape:", X.shape)


print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training model...")

model = LogisticRegression(
    max_iter=2000,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Evaluating...")

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)
print(classification_report(y_test, y_pred))


print("Saving model...")

joblib.dump(model, MODEL_PATH)

print("Done!")
