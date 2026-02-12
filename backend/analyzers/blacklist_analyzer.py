import os
import requests
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("GOOGLE_SAFE_KEY")

def check_blacklist(url: str):
    if not API_KEY:
        return {
            "blacklisted": False,
            "score": 0,
            "status": "skipped",
            "details": "Blacklist check skipped (Missing API Key)"
        }

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client": {
            "clientId": "phishguard",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
        data = response.json()

        if "matches" in data:
            return {
                "blacklisted": True,
                "score": 90,
                "status": "unsafe",
                "details": "URL found in Google Safe Browsing blacklist"
            }

        return {
            "blacklisted": False,
            "score": 0,
            "status": "safe",
            "details": "URL not found in blacklists"
        }

    except Exception as e:
        return {
            "blacklisted": False,
            "score": 0,
            "status": "error",
            "details": f"Blacklist check failed: {str(e)}"
        }
