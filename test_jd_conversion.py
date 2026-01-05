"""Test JD to time conversion"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PyJHora/src'))

from jhora.panchanga import drik
from jhora import utils, const

# Test converting JD fraction to time
jd_fraction = 4.409582018852234  # From brahma muhurta start

print(f"JD fraction: {jd_fraction}")
print(f"As hours: {jd_fraction * 24}")

# Create a time string from hours
hours = jd_fraction * 24
h = int(hours)
m = int((hours - h) * 60)
s = int(((hours - h) * 60 - m) * 60)
print(f"Time: {h:02d}:{m:02d}:{s:02d}")

# Check if there's a utils function
print("\nChecking utils module for time conversion:")
print([x for x in dir(utils) if 'time' in x.lower() or 'hour' in x.lower()])

