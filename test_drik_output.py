"""Test to see what drik module actually returns"""
import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PyJHora/src'))

from jhora.panchanga import drik
from jhora import utils, const

# Set ayanamsa
const._DEFAULT_AYANAMSA_MODE = "LAHIRI"
drik.set_ayanamsa_mode("LAHIRI")

# Create place (Chennai)
place = drik.Place("Chennai", 13.0827, 80.2707, 5.5)

# Date and time
dob = (2024, 10, 5)
tob = (12, 0, 0)

# Calculate Julian day
jd = utils.julian_day_number(dob, tob)

print("Testing drik module outputs:")
print("=" * 60)

# Test Brahma Muhurta
print("\n1. Brahma Muhurta:")
try:
    brahma = drik.brahma_muhurtha(jd, place)
    print(f"   Type: {type(brahma)}")
    print(f"   Value: {brahma}")
    if isinstance(brahma, (list, tuple)):
        for i, item in enumerate(brahma):
            print(f"   [{i}]: {item} (type: {type(item)})")
except Exception as e:
    print(f"   Error: {e}")

# Test Muhurthas
print("\n2. All Muhurthas:")
try:
    muhurthas = drik.muhurthas(jd, place)
    print(f"   Type: {type(muhurthas)}")
    print(f"   Length: {len(muhurthas)}")
    if len(muhurthas) > 0:
        print(f"   First item: {muhurthas[0]}")
        print(f"   First item type: {type(muhurthas[0])}")
        if isinstance(muhurthas[0], (list, tuple)):
            for i, item in enumerate(muhurthas[0]):
                print(f"   [0][{i}]: {item} (type: {type(item)})")
except Exception as e:
    print(f"   Error: {e}")

# Test Eclipses
print("\n3. Solar Eclipse:")
try:
    solar_eclipse = drik.next_solar_eclipse(jd, place)
    print(f"   Type: {type(solar_eclipse)}")
    print(f"   Value: {solar_eclipse}")
except Exception as e:
    print(f"   Error: {e}")

# Test Sankranti
print("\n4. Sankranti:")
try:
    next_sankranti = drik.next_sankranti(jd, place)
    print(f"   Type: {type(next_sankranti)}")
    print(f"   Value: {next_sankranti}")
    if isinstance(next_sankranti, (list, tuple)):
        for i, item in enumerate(next_sankranti):
            print(f"   [{i}]: {item} (type: {type(item)})")
except Exception as e:
    print(f"   Error: {e}")

# Test Gauri Choghadiya
print("\n5. Gauri Choghadiya:")
try:
    choghadiya = drik.gauri_choghadiya(jd, place)
    print(f"   Type: {type(choghadiya)}")
    print(f"   Value (first 200 chars): {str(choghadiya)[:200]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)

