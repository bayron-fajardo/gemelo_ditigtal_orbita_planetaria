import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv()

APP_ID = os.getenv("app_id")
APP_SECRET = os.getenv("app_secret")


auth_string = f"{APP_ID}:{APP_SECRET}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {auth_encoded}",
    "Content-Type": "application/json"
}


PARAMS = {
    "latitude": "3.403776",
    "longitude": "-76.547798",
    "elevation": "970.2",
    "from_date": "2025-11-14",
    "to_date": "2025-11-14",
    "time": "12:00:00",
    "output": "rows"
}

PLANETS = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn"]
BASE_URL = "https://api.astronomyapi.com/api/v2/bodies/positions"

results = []

for planet in PLANETS:
    url = f"{BASE_URL}/{planet}"
    response = requests.get(url, headers=HEADERS, params=PARAMS)

    
    results.append({
        "planet": planet,
        "status": response.status_code,
        "data": response.text
    })


for item in results:
    print(f"\nPlanet: {item['planet']}")
    print(f"Status: {item['status']}")
    print(f"Response: {item['data']}")
