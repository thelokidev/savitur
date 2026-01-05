
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/panchanga"

def get_planets(date_str, ayanamsa):
    payload = {
        "date": date_str,
        "time": "04:30:00",
        "place": {
            "name": "Chennai, India",
            "latitude": 13.0878,
            "longitude": 80.2785,
            "timezone": 5.5
        },
        "ayanamsa": ayanamsa
    }
    
    try:
        response = requests.post(f"{BASE_URL}/planets", json=payload)
        response.raise_for_status()
        data = response.json()
        sun = next((p for p in data['planets'] if p['name'] == 'Sun'), None)
        return sun['longitude'] if sun else None
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def to_dms(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = (deg - d - m/60) * 3600
    return f"{d}d {m}' {s:.2f}\""

def main():
    # Try Nov 9, 1998
    date1 = "1998-11-09"
    print(f"Testing Date: {date1}")
    lahiri_long = get_planets(date1, "LAHIRI")
    raman_long = get_planets(date1, "RAMAN")
    
    print(f"Lahiri Sun: {lahiri_long} ({to_dms(lahiri_long) if lahiri_long else 'N/A'})")
    print(f"Raman Sun:  {raman_long} ({to_dms(raman_long) if raman_long else 'N/A'})")
    
    # Try Sep 11, 1998
    date2 = "1998-09-11"
    print(f"\nTesting Date: {date2}")
    lahiri_long2 = get_planets(date2, "LAHIRI")
    raman_long2 = get_planets(date2, "RAMAN")
    
    print(f"Lahiri Sun: {lahiri_long2} ({to_dms(lahiri_long2) if lahiri_long2 else 'N/A'})")
    print(f"Raman Sun:  {raman_long2} ({to_dms(raman_long2) if raman_long2 else 'N/A'})")

if __name__ == "__main__":
    main()
