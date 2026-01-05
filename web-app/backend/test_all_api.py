"""
Comprehensive API Test Script
Tests all major endpoints to verify everything is working
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, url, data=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            print(f"[OK] {name}: SUCCESS")
            return True
        else:
            print(f"[FAIL] {name}: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"[ERROR] {name}: {str(e)[:100]}")
        return False

# Test data
test_birth_details = {
    "birth_details": {
        "name": "Test Person",
        "date": "1990-01-15",
        "time": "10:30:00",
        "place": {
            "name": "Chennai",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone": 5.5
        }
    },
    "ayanamsa": "LAHIRI"
}

test_panchanga = {
    "date": "2024-01-15",
    "time": "12:00:00",
    "place": {
        "name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": 5.5
    }
}

test_dhasa = {
    "birth_details": {
        "date": "1990-01-15",
        "time": "10:30:00",
        "place": {
            "name": "Delhi",
            "latitude": 28.7041,
            "longitude": 77.1025,
            "timezone": 5.5
        }
    },
    "dhasa_type": "vimsottari",
    "include_antardhasa": True,
    "ayanamsa": "LAHIRI"
}

test_yoga = {
    "birth_details": {
        "date": "1990-01-15",
        "time": "10:30:00",
        "place": {
            "name": "Mumbai",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone": 5.5
        }
    },
    "ayanamsa": "LAHIRI"
}

test_strength = {
    "birth_details": {
        "date": "1990-01-15",
        "time": "10:30:00",
        "place": {
            "name": "Bangalore",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "timezone": 5.5
        }
    },
    "calculation_type": "shadbala",
    "ayanamsa": "LAHIRI"
}

test_compatibility = {
    "boy": {
        "date": "1990-01-15",
        "time": "10:30:00",
        "place": {
            "name": "Mumbai",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone": 5.5
        }
    },
    "girl": {
        "date": "1992-05-20",
        "time": "14:45:00",
        "place": {
            "name": "Chennai",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone": 5.5
        }
    },
    "compatibility_type": "north",
    "ayanamsa": "LAHIRI"
}

print("=" * 60)
print(" PyJHora API - Comprehensive Test Suite")
print("=" * 60)
print()

results = []

# 1. Health & Root
print("1. HEALTH & ROOT ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("Health Check", "GET", f"{BASE_URL}/health"))
results.append(test_endpoint("Root", "GET", f"{BASE_URL}/"))
print()

# 2. Panchanga
print("2. PANCHANGA ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("Panchanga Calculate", "POST", f"{BASE_URL}/api/v1/panchanga/calculate", test_panchanga))
results.append(test_endpoint("Planet Positions", "POST", f"{BASE_URL}/api/v1/panchanga/planets", test_panchanga))
print()

# 3. Charts
print("3. CHART ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("Rasi Chart (D-1)", "POST", f"{BASE_URL}/api/v1/charts/rasi", test_birth_details))
results.append(test_endpoint("Navamsa Chart (D-9)", "POST", f"{BASE_URL}/api/v1/charts/divisional/9", test_birth_details))
results.append(test_endpoint("Special Lagnas", "POST", f"{BASE_URL}/api/v1/charts/special-lagnas", test_birth_details))
results.append(test_endpoint("Upagrahas", "POST", f"{BASE_URL}/api/v1/charts/upagrahas", test_birth_details))
results.append(test_endpoint("Arudha Padas", "POST", f"{BASE_URL}/api/v1/charts/arudha-padas", test_birth_details))
print()

# 4. Dhasa
print("4. DHASA ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("Vimsottari Dhasa", "POST", f"{BASE_URL}/api/v1/dhasa/vimsottari", test_dhasa))
results.append(test_endpoint("Ashtottari Dhasa", "POST", f"{BASE_URL}/api/v1/dhasa/graha/ashtottari", test_dhasa))
results.append(test_endpoint("Chara Dhasa", "POST", f"{BASE_URL}/api/v1/dhasa/raasi/chara", test_dhasa))
results.append(test_endpoint("Applicable Dhasas", "POST", f"{BASE_URL}/api/v1/dhasa/applicable", test_dhasa))
print()

# 5. Yogas & Doshas
print("5. YOGA & DOSHA ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("All Yogas", "POST", f"{BASE_URL}/api/v1/yogas/all-yogas", test_yoga))
results.append(test_endpoint("All Doshas", "POST", f"{BASE_URL}/api/v1/yogas/all-doshas", test_yoga))
print()

# 6. Strength
print("6. STRENGTH ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("Shadbala", "POST", f"{BASE_URL}/api/v1/strength/shadbala", test_strength))
results.append(test_endpoint("Ashtakavarga", "POST", f"{BASE_URL}/api/v1/strength/ashtakavarga", test_strength))
results.append(test_endpoint("Shodhaya Pinda", "POST", f"{BASE_URL}/api/v1/strength/shodhaya-pinda", test_strength))
results.append(test_endpoint("Bhava Bala", "POST", f"{BASE_URL}/api/v1/strength/bhava-bala", test_strength))
print()

# 7. Compatibility
print("7. COMPATIBILITY ENDPOINTS")
print("-" * 60)
results.append(test_endpoint("North Indian Compatibility", "POST", f"{BASE_URL}/api/v1/compatibility/north-indian", test_compatibility))
results.append(test_endpoint("South Indian Compatibility", "POST", f"{BASE_URL}/api/v1/compatibility/south-indian", test_compatibility))
results.append(test_endpoint("Both Methods", "POST", f"{BASE_URL}/api/v1/compatibility/both-methods", test_compatibility))
print()

# Summary
print("=" * 60)
print(" TEST SUMMARY")
print("=" * 60)
total = len(results)
passed = sum(results)
failed = total - passed
print(f"Total Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Success Rate: {(passed/total*100):.1f}%")
print()

if passed == total:
    print("SUCCESS! ALL TESTS PASSED! API is fully operational!")
else:
    print(f"WARNING: {failed} test(s) failed. Please check the errors above.")

print("=" * 60)

