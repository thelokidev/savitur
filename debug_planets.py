#!/usr/bin/env python3
import requests
import json

# Test data
TEST_DATA = {
    "date": "2024-10-05",
    "time": "12:00:00",
    "place": {
        "name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": 5.5
    },
    "ayanamsa": "LAHIRI"
}

BASE_URL = "http://localhost:8000/api/v1/panchanga"

def test_planets_endpoint():
    """Test the planets endpoint specifically"""
    url = f"{BASE_URL}/planets"

    try:
        response = requests.post(url, json=TEST_DATA, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 500:
            print("Error response:")
            print(response.text)
        else:
            result = response.json()
            print("Success!")
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_planets_endpoint()
