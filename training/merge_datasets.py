import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PHISH = os.path.join(BASE_DIR, "datasets", "processed", "phishing_urls.csv")
SAFE = os.path.join(BASE_DIR, "datasets", "processed", "safe_urls.csv")
FINAL = os.path.join(BASE_DIR, "datasets", "raw_urls.csv")

phish_df = pd.read_csv(PHISH)
safe_df = pd.read_csv(SAFE)

final_df = pd.concat([phish_df, safe_df])
final_df = final_df.sample(frac=1).reset_index(drop=True)

final_df.to_csv(FINAL, index=False)

print("Final dataset ready.")
