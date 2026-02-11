import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "datasets", "raw_downloads", "openphish.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "datasets", "processed", "phishing_urls.csv")

with open(INPUT_PATH, "r") as f:
    urls = f.read().splitlines()

df = pd.DataFrame({
    "url": urls,
    "label": 1
})

df.drop_duplicates(inplace=True)
df.to_csv(OUTPUT_PATH, index=False)

print("Phishing dataset saved.")
