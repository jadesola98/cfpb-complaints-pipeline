import json

import requests

URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

# Identify the client; some sites block requests without a browser-like User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.consumerfinance.gov/data-research/consumer-complaints/search/",
}

params = {
    "size": 3,
    "date_received_min": "2026-10-01",
    "no_aggs": "true",
}

response = requests.get(URL, params=params, headers=HEADERS, timeout=60)
print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()
print("Total matching complaints:", data["hits"]["total"])
print("\nFirst complaint:")
print(json.dumps(data["hits"]["hits"][0]["_source"], indent=2))