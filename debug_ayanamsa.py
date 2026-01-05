import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.getcwd(), 'PyJHora/src'))

from jhora import const
from jhora.panchanga import drik
import swisseph as swe

print("Available Ayanamsa Modes:")
for k, v in const.available_ayanamsa_modes.items():
    print(f"'{k}': {v} (type: {type(v)})")

def test_set_mode(mode):
    print(f"\nTesting mode: {mode}")
    try:
        drik.set_ayanamsa_mode(mode)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

test_set_mode("LAHIRI")
test_set_mode("SENTHIL")
test_set_mode("SUNDAR_SS")
test_set_mode("TRUE_CITRA")
test_set_mode("KP")
