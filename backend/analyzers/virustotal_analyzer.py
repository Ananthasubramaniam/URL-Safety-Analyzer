import requests
import os

VT_API_KEY = os.getenv("VT_API_KEY")   # store key in .env

def check_virustotal(url: str) -> dict:
    if not VT_API_KEY:
        return {"score": 0, "details": "VirusTotal API key missing"}

    endpoint = "https://www.virustotal.com/api/v3/urls"

    headers = {
        "x-apikey": VT_API_KEY
    }

    try:
        # Submit URL
        submit = requests.post(endpoint, headers=headers, data={"url": url})
        analysis_id = submit.json()["data"]["id"]

        # Get report
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        report = requests.get(report_url, headers=headers).json()

        stats = report["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        vt_score = (malicious * 5) + (suspicious * 2)

        return {
            "score": vt_score,
            "details": f"VirusTotal flagged {malicious} malicious engines"
        }

    except Exception as e:
        return {"score": 0, "details": "VirusTotal check failed"}
