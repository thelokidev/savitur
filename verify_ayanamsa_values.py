import sys
import os
import swisseph as swe
from datetime import datetime

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.getcwd(), 'PyJHora/src'))

from jhora import const, utils
from jhora.panchanga import drik

def verify_ayanamsa_values():
    # Set a specific date for verification (e.g., today)
    today = datetime.now()
    jd = utils.gregorian_to_jd(drik.Date(today.year, today.month, today.day))
    
    print(f"Verifying Ayanamsa values for Date: {today.strftime('%Y-%m-%d')} (JD: {jd})")
    print("-" * 60)
    print(f"{'Mode':<20} | {'Value (Degrees)':<20} | {'Value (DMS)':<20}")
    print("-" * 60)

    modes_to_test = ['LAHIRI', 'SENTHIL', 'SUNDAR_SS']
    
    for mode in modes_to_test:
        try:
            # Reset before each test to ensure clean state
            swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY) 
            
            # Set the mode
            drik.set_ayanamsa_mode(mode, jd=jd)
            
            # Get the value
            # Note: get_ayanamsa_value returns float degrees
            # We need to access the internal value for custom modes if get_ayanamsa_value doesn't handle it
            # But looking at drik.py, get_ayanamsa_value handles custom keys.
            
            val = drik.get_ayanamsa_value(jd)
            print(f"Debug: Mode={mode}, Type of val={type(val)}, Value={val}")
            
            if isinstance(val, (int, float)):
                dms = utils.to_dms(val)
                dms_str = f"{dms[0]}° {dms[1]}' {dms[2]:.2f}\""
                print(f"{mode:<20} | {val:<20.6f} | {dms_str:<20}")
            else:
                print(f"{mode:<20} | {str(val):<20} | {'N/A':<20}")
            
        except Exception as e:
            print(f"{mode:<20} | {'ERROR':<20} | {str(e)}")

if __name__ == "__main__":
    verify_ayanamsa_values()
