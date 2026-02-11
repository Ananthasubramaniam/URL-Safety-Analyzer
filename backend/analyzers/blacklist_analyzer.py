import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_SAFE_KEY")

def check_blacklist(url: str):
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
                "score": 90
            }

        return {
            "blacklisted": False,
            "score": 0
        }

    except Exception as e:
        return {
            "blacklisted": False,
            "score": 0,
            "error": str(e)
        }
