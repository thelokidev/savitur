#!/usr/bin/env python
"""
Test script to verify PyJHora strength calculations
"""
import sys
sys.path.insert(0, 'o:/savitur/PyJHora/src')

from jhora.panchanga import drik
from jhora.horoscope.chart import charts, strength
from jhora import const,utils

# Set ayanamsa
drik.set_ayanamsa_mode("LAHIRI")

# Test birth data
dob = (1990, 1, 1)
tob = (12, 0, 0)
place = drik.Place('Chennai', 13.0827, 80.2707, +5.5)

# Calculate JD
jd = utils.julian_day_number(dob, tob)

# Get planet positions
planet_positions = charts.divisional_chart(jd, place, divisional_chart_factor=1)

print("Planet Positions:")
print(planet_positions)
print("\n")

# Test Shadbala for Sun (index 0)
print("=== Testing Shadbala for Sun (index 0) ===")
try:
    sthana = strength.sthana_bala(jd, place, planet_positions, 0)
    print(f"Sthana Bala: {sthana} (type: {type(sthana)})")
    
    dig = strength.dig_bala(jd, place, planet_positions, 0)
    print(f"Dig Bala: {dig} (type: {type(dig)})")
    
    kaala = strength.kaala_bala(jd, place, planet_positions, 0)
    print(f"Kaala Bala: {kaala} (type: {type(kaala)})")
    
    cheshta = strength.cheshta_bala(jd, place, 0)
    print(f"Cheshta Bala: {cheshta} (type: {type(cheshta)})")
    
    naisargika = strength.naisargika_bala(0)
    print(f"Naisargika Bala: {naisargika} (type: {type(naisargika)})")
    
    drik = strength.drik_bala(jd, place, planet_positions, 0)
    print(f"Drik Bala: {drik} (type: {type(drik)})")
    
    total = sthana + dig + kaala + cheshta + naisargika + drik
    print(f"Total Shadbala: {total}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n")

# Test Vimsopaka Bala
print("=== Testing Vimsopaka Bala ===")
try:
    dhasavarga = charts.vimsopaka_dhasavarga_of_planets(jd, place)
    print(f"Dhasavarga: {dhasavarga}")
    print(f"Type: {type(dhasavarga)}")
    print(f"Length: {len(dhasavarga) if hasattr(dhasavarga, '__len__') else 'N/A'}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n")

# Test Harsha Bala
print("=== Testing Harsha Bala ===")
try:
    hb = strength.harsha_bala(dob, tob, place)
    print(f"Harsha Bala: {hb}")
    print(f"Type: {type(hb)}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
