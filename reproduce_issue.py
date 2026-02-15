import requests
import json
import time

url = "http://localhost:8000/generate/character"
payload = {
    "id": "kaelen",
    "force": True
}
headers = {
    "Content-Type": "application/json"
}

# Wait for server to be ready (simple retry)
for i in range(5):
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            break
    except:
        time.sleep(1)

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
