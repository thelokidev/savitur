import sys
import os
import warnings

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.getcwd(), 'PyJHora/src'))

from jhora import const
from jhora.panchanga import drik
import swisseph as swe

# Mock warnings to capture them
def custom_warn(message, category=None, stacklevel=1, source=None):
    print(f"WARNING: {message}")

warnings.warn = custom_warn

print("Available Ayanamsa Modes:")
for k, v in const.available_ayanamsa_modes.items():
    print(f"'{k}': {v} (type: {type(v)})")

def test_set_mode(mode, jd=None):
    print(f"\nTesting mode: {mode}")
    try:
        drik.set_ayanamsa_mode(mode, jd=jd)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Test cases
test_set_mode("LAHIRI")
test_set_mode("SENTHIL", jd=2459000.5) # Needs JD
test_set_mode("SUNDAR_SS", jd=2459000.5) # Needs JD
test_set_mode("KP-SENTHIL")
