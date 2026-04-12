"""
AstroSDK 2.0 Example: REST API Usage
Demonstrates how to interact with the AstroSDK V2 API using the requests library.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def get_planet_position():
    print("\n--- 1. Fetching Single Planet Position (Geocentric Sideal) ---")
    url = f"{BASE_URL}/api/v2/astronomy/planet-position"
    params = {
        "planet": "JUPITER",
        "time": "2024-04-08T18:00:00Z"
    }
    # 2.0 uses headers for calculation context
    headers = {
        "X-Astro-Is-Sidereal": "true",
        "X-Astro-Sidereal-Mode": "LAHIRI"
    }
    response = requests.get(url, params=params, headers=headers)
    print(json.dumps(response.json(), indent=2))

def get_topocentric_moon():
    print("\n--- 2. Fetching Topocentric Moon Position ---")
    url = f"{BASE_URL}/api/v2/astronomy/planet-position"
    params = {
        "planet": "MOON",
        "time": "2024-04-08T18:00:00Z",
        "coordinate_system": "topocentric",
        "latitude": 25.3,
        "longitude": -104.1
    }
    response = requests.get(url, params=params)
    print(json.dumps(response.json(), indent=2))

def create_natal_chart():
    print("\n--- 3. Generating Natal Chart (POST Request) ---")
    url = f"{BASE_URL}/api/v2/charts/natal"
    payload = {
        "time": {"time": "2024-04-08T18:00:00Z"},
        "location": {
            "latitude": 40.7128, 
            "longitude": -74.0060,
            "altitude": 10
        },
        "settings": {
            "house_system": "P",
            "is_sidereal": True
        }
    }
    response = requests.post(url, json=payload)
    data = response.json()
    print(f"Calculation Fingerprint: {data['meta']['calculation_fingerprint']}")
    print(f"Ascendant: {data['data']['ascendant']:.2f}°")
    print(f"Planets Found: {len(data['data']['planets'])}")

if __name__ == "__main__":
    try:
        get_planet_position()
        get_topocentric_moon()
        create_natal_chart()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to AstroSDK. Is the uvicorn server running?")
