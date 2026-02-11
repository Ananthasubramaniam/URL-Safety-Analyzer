import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "datasets", "raw_downloads", "top-1m.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "datasets", "processed", "safe_urls.csv")

# Load domain list
df = pd.read_csv(INPUT_PATH, header=None)

# Take first 5000 domains only (enough for hackathon)
domains = df[1].head(5000)

# Convert to https URLs
safe_urls = ["https://" + d for d in domains]

safe_df = pd.DataFrame({
    "url": safe_urls,
    "label": 0
})

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

safe_df.to_csv(OUTPUT_PATH, index=False)

print("Safe dataset saved.")
