
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/panchanga"

def get_planets(ayanamsa):
    payload = {
        "date": "2025-11-20",
        "time": "06:00:00",
        "place": {
            "name": "Chennai, India",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone": 5.5
        },
        "ayanamsa": ayanamsa
    }
    
    try:
        response = requests.post(f"{BASE_URL}/planets", json=payload)
        response.raise_for_status()
        data = response.json()
        # Get Sun longitude
        sun = next((p for p in data['planets'] if p['name'] == 'Sun'), None)
        return sun['longitude'] if sun else None
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def main():
    lahiri_long = get_planets("LAHIRI")
    raman_long = get_planets("RAMAN")
    
    print(f"Lahiri Sun Longitude: {lahiri_long}")
    print(f"Raman Sun Longitude:  {raman_long}")
    
    if lahiri_long is not None and raman_long is not None:
        if abs(lahiri_long - raman_long) < 0.0001:
            print("FAIL: API returns identical positions!")
        else:
            print("SUCCESS: API returns different positions.")
    else:
        print("Could not get data.")

if __name__ == "__main__":
    main()
