
import sys
import os

# Add PyJHora/src to path
sys.path.append(os.path.join(os.getcwd(), 'PyJHora', 'src'))

from jhora.panchanga import drik
from jhora import const
import swisseph as swe

def test_ayanamsa(ayanamsa_name, jd):
    print(f"Testing Ayanamsa: {ayanamsa_name}")
    
    # Set ayanamsa mode
    # We mimic what panchanga_service.py does:
    # const._DEFAULT_AYANAMSA_MODE = ayanamsa
    # drik.set_ayanamsa_mode(ayanamsa)
    
    const._DEFAULT_AYANAMSA_MODE = ayanamsa_name
    drik.set_ayanamsa_mode(ayanamsa_name)
    
    # Calculate Sun longitude
    # drik.sidereal_longitude calls set_ayanamsa_mode internally too
    sun_long = drik.sidereal_longitude(jd, const._SUN)
    
    print(f"Sun Longitude ({ayanamsa_name}): {sun_long}")
    return sun_long

def main():
    # Date: 2025-11-20
    # We can use a fixed JD for testing
    jd = 2460999.75 # Approx JD for 2025-11-20
    
    print(f"Testing with JD: {jd}")
    
    lahiri_long = test_ayanamsa("LAHIRI", jd)
    raman_long = test_ayanamsa("RAMAN", jd)
    true_citra_long = test_ayanamsa("TRUE_CITRA", jd)
    
    print("-" * 30)
    print(f"Lahiri:     {lahiri_long}")
    print(f"Raman:      {raman_long}")
    print(f"True Citra: {true_citra_long}")
    
    if abs(lahiri_long - raman_long) < 0.0001:
        print("FAIL: Lahiri and Raman are identical!")
    else:
        print("SUCCESS: Lahiri and Raman are different.")

    if abs(lahiri_long - true_citra_long) < 0.0001:
        print("FAIL: Lahiri and True Citra are identical!")
    else:
        print("SUCCESS: Lahiri and True Citra are different.")

if __name__ == "__main__":
    main()
