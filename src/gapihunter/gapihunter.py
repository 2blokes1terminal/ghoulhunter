import requests
import os


def check_url(domain):
    api_key = os.environ["GAPI_KEY"]
    req = requests.post(
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}",
        json={
            "client": {
                "clientId": "test-icicles",
                "clientVersion": "1.5.2"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                    "UNWANTED_SOFTWARE"
                ],
                "platformTypes": ["WINDOWS"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": f"https://{domain}/"}
                ]
            }
        }
    )

    return req.json()
