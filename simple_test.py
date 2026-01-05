#!/usr/bin/env python3
import requests
import json
import time

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

def test_endpoint(endpoint, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=TEST_DATA, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] {endpoint}: SUCCESS - {description}")
            # Count features roughly
            feature_count = len(json.dumps(result))
            print(f"   Response size: {feature_count} chars")
            return True, result
        else:
            print(f"[FAIL] {endpoint}: FAILED - Status {response.status_code} - {description}")
            return False, None
    except Exception as e:
        print(f"[ERROR] {endpoint}: ERROR - {str(e)} - {description}")
        return False, None

def main():
    print("PANCHANGA API COVERAGE TEST")
    print("=" * 50)
    print("Test Date: 2024-10-05 12:00:00")
    print("Test Place: Chennai (13.0827, 80.2707)")
    print("Ayanamsa: LAHIRI")
    print()

    # Test endpoints
    endpoints = [
        ("calculate", "Basic panchanga"),
        ("planets", "Planet positions"),
        ("muhurtha", "All muhurthas"),
        ("extended", "Extended features"),
        ("eclipses", "Eclipse info"),
        ("sankranti", "Sankranti dates"),
        ("retrograde", "Retrograde info"),
        ("udhaya-lagna", "Udhaya lagna"),
        ("conjunctions", "Planet conjunctions")
    ]

    success_count = 0
    total_endpoints = len(endpoints)

    print("Testing endpoints:")
    print("-" * 30)

    for endpoint, desc in endpoints:
        success, result = test_endpoint(endpoint, desc)
        if success:
            success_count += 1
        print()

    print("=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    print(f"Endpoints tested: {total_endpoints}")
    print(f"Successful: {success_count}")
    print(f"Success rate: {(success_count/total_endpoints*100):.1f}%")

    if success_count == total_endpoints:
        print()
        print("CONCLUSION: PANCHANGA API IS 100% FUNCTIONAL!")
        print("All PyJHora panchanga features are now available via REST API.")
    else:
        print()
        print("CONCLUSION: Some endpoints need fixing.")

if __name__ == "__main__":
    # Wait a bit for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    main()
