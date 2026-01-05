import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

# Birth Details from User Screenshot
birth_details = {
    "date": "1998-09-11",
    "time": "04:30:00",
    "place": {
        "name": "Chennai, India",
        "latitude": 13.0878,
        "longitude": 80.2785,
        "timezone": 5.5
    }
}

def get_planet_positions(ayanamsa):
    url = f"{BASE_URL}/panchanga/planets"
    payload = {
        "date": birth_details["date"],
        "time": birth_details["time"],
        "place": birth_details["place"],
        "ayanamsa": ayanamsa
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract Sun's longitude
        if "planets" in data:
            sun = next((p for p in data["planets"] if p["name"] == "Sun"), None)
            if sun:
                return sun["longitude"]
        return None
    except Exception as e:
        print(f"Error fetching {ayanamsa}: {e}")
        return None

def main():
    print("Verifying Ayanamsa Values...")
    
    lahiri_sun = get_planet_positions("LAHIRI")
    raman_sun = get_planet_positions("RAMAN")
    ss_sun = get_planet_positions("SURYASIDDHANTA")
    
    print(f"LAHIRI Sun: {lahiri_sun}")
    print(f"RAMAN Sun:  {raman_sun}")
    print(f"SS Sun:     {ss_sun}")
    
    if lahiri_sun == ss_sun:
        print("\nWARNING: LAHIRI and SURYASIDDHANTA values are IDENTICAL!")
    else:
        print("\nSUCCESS: LAHIRI and SURYASIDDHANTA values are DIFFERENT.")

if __name__ == "__main__":
    main()
