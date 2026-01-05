"""
Simple API test script
Run this after starting the server to test endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_panchanga():
    """Test panchanga calculation"""
    print("Testing panchanga calculation...")
    data = {
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
    
    response = requests.post(f"{BASE_URL}/api/v1/panchanga/calculate", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Date: {result['date']}")
        print(f"Place: {result['place']['name']}")
        print(f"Sunrise: {result['sunrise']}")
        print(f"Tithi: {result['tithi']['name']} ({result['tithi']['paksha']} Paksha)")
        print(f"Nakshatra: {result['nakshatra']['name']}")
        print(f"Yoga: {result['yoga']['name']}")
        print(f"Karana: {result['karana']['name']}")
        print(f"Vaara: {result['vaara']}\n")
    else:
        print(f"Error: {response.text}\n")

def test_planets():
    """Test planet positions"""
    print("Testing planet positions...")
    data = {
        "date": "2024-10-05",
        "time": "12:00:00",
        "place": {
            "name": "Mumbai",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone": 5.5
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/panchanga/planets", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Ascendant: {result['ascendant']['rasi_name']} {result['ascendant']['degrees_in_rasi']:.2f}°")
        print("\nPlanets:")
        for planet in result['planets']:
            print(f"  {planet['name']:10s}: {planet['rasi_name']:12s} {planet['degrees_in_rasi']:5.2f}°")
        print()
    else:
        print(f"Error: {response.text}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("PyJHora API Test")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_panchanga()
        test_planets()
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: {e}")

