import requests
import json

url = "http://localhost:8000/api/bulk-analyze"
headers = {"Content-Type": "application/json"}
data = ["http://google.com", "http://example.com", "javascript:alert(1)"]

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Exception: {e}")
