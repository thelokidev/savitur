"""
Calculate comprehensive Jyotish data for birth details
Date: September 11, 1998, 4:30 AM
Location: Chennai, India
"""
import sys
import os
import json
from datetime import datetime

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PyJHora/src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web-app/backend'))

from jhora.panchanga import drik
from jhora.horoscope.chart import charts
from jhora.horoscope.dhasa.graha import vimsottari
from jhora import utils, const

# Birth details
BIRTH_DATE = "1998-09-11"
BIRTH_TIME = "04:30:00"
PLACE_NAME = "Chennai, India"
LATITUDE = 13.0827
LONGITUDE = 80.2707
TIMEZONE = 5.5

# Set ayanamsa
AYANAMSA = "LAHIRI"
const._DEFAULT_AYANAMSA_MODE = AYANAMSA
drik.set_ayanamsa_mode(AYANAMSA)

def format_degrees(degrees):
    """Format degrees to degrees, minutes, seconds"""
    deg = int(degrees)
    minutes = (degrees - deg) * 60
    min_int = int(minutes)
    sec = (minutes - min_int) * 60
    return f"{deg}° {min_int}' {sec:.2f}\""

def format_time_from_jd(jd_fraction):
    """Convert Julian Day fraction to time string"""
    hours = (jd_fraction % 1) * 24
    h = int(hours)
    m = int((hours - h) * 60)
    s = int(((hours - h) * 60 - m) * 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_rasi_name(rasi_num):
    """Get Rasi name from number"""
    rasi_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return rasi_names[rasi_num]

def get_nakshatra_name(nak_num):
    """Get Nakshatra name from number"""
    nakshatra_names = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    return nakshatra_names[nak_num]

def main():
    print("=" * 80)
    print("VEDIC ASTROLOGY CALCULATION")
    print("=" * 80)
    print(f"\nBirth Details:")
    print(f"  Date: {BIRTH_DATE}")
    print(f"  Time: {BIRTH_TIME}")
    print(f"  Place: {PLACE_NAME}")
    print(f"  Coordinates: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Timezone: UTC+{TIMEZONE}")
    print(f"  Ayanamsa: {AYANAMSA}")
    print("\n" + "=" * 80)
    
    # Create place object
    place = drik.Place(PLACE_NAME, LATITUDE, LONGITUDE, TIMEZONE)
    
    # Parse date and time
    year, month, day = map(int, BIRTH_DATE.split('-'))
    dob = (year, month, day)
    hour, minute, second = map(int, BIRTH_TIME.split(':'))
    tob = (hour, minute, second)
    
    # Calculate Julian Day
    jd = utils.julian_day_number(dob, tob)
    print(f"\nJulian Day: {jd:.6f}")
    
    # Calculate Ayanamsa
    ayanamsa_value = drik.get_ayanamsa_value(jd)
    print(f"Ayanamsa Value: {ayanamsa_value:.6f}°")
    
    # ========== PANCHANGA CALCULATIONS ==========
    print("\n" + "=" * 80)
    print("PANCHANGA (ALMANAC DETAILS)")
    print("=" * 80)
    
    # Tithi
    try:
        tithi_info = drik.tithi(jd, place)
        print(f"\nTithi: {tithi_info[0]}")
        if len(tithi_info) > 1:
            print(f"Tithi End Time: {tithi_info[1]}")
    except Exception as e:
        print(f"\nTithi calculation error: {e}")
        tithi_info = ["N/A"]
    
    # Nakshatra
    try:
        nakshatra_info = drik.nakshatra(jd, place)
        nak_num = nakshatra_info[0]
        nak_pada = nakshatra_info[1]
        nak_name = get_nakshatra_name(nak_num - 1)
        print(f"\nNakshatra: {nak_name} ({nak_num})")
        print(f"Pada: {nak_pada}")
        if len(nakshatra_info) > 2:
            print(f"Nakshatra End Time: {nakshatra_info[2]}")
    except Exception as e:
        print(f"\nNakshatra calculation error: {e}")
        nakshatra_info = [0, 0]
        nak_name = "N/A"
        nak_pada = 0
    
    # Yoga
    try:
        yoga_info = drik.yoga(jd, place)
        print(f"\nYoga: {yoga_info[0]}")
        if len(yoga_info) > 1:
            print(f"Yoga End Time: {yoga_info[1]}")
    except Exception as e:
        print(f"\nYoga calculation error: {e}")
        yoga_info = ["N/A"]
    
    # Karana
    try:
        karana_info = drik.karana(jd, place)
        print(f"\nKarana: {karana_info[0]}")
    except Exception as e:
        print(f"\nKarana calculation error: {e}")
        karana_info = ["N/A"]
    
    # Vaara (Weekday)
    try:
        vaara = drik.vaara(jd)
        print(f"\nVaara (Weekday): {vaara}")
    except Exception as e:
        print(f"\nVaara calculation error: {e}")
        vaara = "N/A"
    
    # ========== BIRTH CHART CALCULATIONS ==========
    print("\n" + "=" * 80)
    print("BIRTH CHART (RASI CHART - D-1)")
    print("=" * 80)
    
    # Get Rasi chart
    chart_data = charts.rasi_chart(jd, place, AYANAMSA)
    
    # Ascendant (Lagna)
    lagna_longitude = chart_data[0][0]
    lagna_rasi = int(lagna_longitude / 30)
    lagna_degrees = (lagna_longitude % 30)
    lagna_name = get_rasi_name(lagna_rasi)
    
    print(f"\nAscendant (Lagna):")
    print(f"  Sign: {lagna_name}")
    print(f"  Longitude: {format_degrees(lagna_longitude)}")
    print(f"  Degrees in Sign: {format_degrees(lagna_degrees)}")
    
    # Planet positions
    planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    print(f"\nPlanetary Positions:")
    
    for i, planet_name in enumerate(planet_names):
        if i < len(chart_data[0]) - 1:  # Exclude Lagna
            planet_longitude = chart_data[0][i + 1]
            planet_rasi = int(planet_longitude / 30)
            planet_degrees = (planet_longitude % 30)
            rasi_name = get_rasi_name(planet_rasi)
            
            # Get Nakshatra for planet
            planet_nak = int(planet_longitude / (360 / 27))
            planet_nak_name = get_nakshatra_name(planet_nak)
            planet_nak_pada = int((planet_longitude % (360 / 27)) / (360 / 108)) + 1
            
            # Check retrograde (simplified - would need actual calculation)
            retrograde = False  # Would need to calculate from ephemeris
            
            retro_str = " (R)" if retrograde else ""
            print(f"  {planet_name:8s}: {format_degrees(planet_longitude):15s} | "
                  f"{rasi_name:12s} | {format_degrees(planet_degrees):15s} | "
                  f"{planet_nak_name} ({planet_nak_pada}){retro_str}")
    
    # House positions
    print(f"\nHouses (Bhava):")
    houses = chart_data[1]
    for house_num in range(1, 13):
        house_sign = houses[house_num - 1]
        house_name = get_rasi_name(house_sign)
        print(f"  House {house_num:2d}: {house_name}")
    
    # ========== DASHA CALCULATIONS ==========
    print("\n" + "=" * 80)
    print("DASHA PERIODS (VIMSOTTARI DASHA)")
    print("=" * 80)
    
    try:
        # Get Vimsottari Dasha
        dasha_data = vimsottari.vimsottari_dasha(jd, place, AYANAMSA)
        
        # Balance at birth
        balance = dasha_data[0]
        print(f"\nBalance Dasha at Birth:")
        print(f"  Planet: {balance[0]}")
        print(f"  Balance: {balance[1]:.6f} years")
        print(f"  Start Date: {balance[2]}")
        
        # Current Mahadasha and Antardasha
        if len(dasha_data) > 1:
            current_md = dasha_data[1]
            print(f"\nCurrent Mahadasha:")
            print(f"  Planet: {current_md[0]}")
            print(f"  Start: {current_md[1]}")
            print(f"  End: {current_md[2]}")
            print(f"  Duration: {current_md[3]} years")
            
            if len(current_md) > 4:
                print(f"\n  Current Antardasha:")
                current_ad = current_md[4]
                print(f"    Planet: {current_ad[0]}")
                print(f"    Start: {current_ad[1]}")
                print(f"    End: {current_ad[2]}")
        
        # Next few Mahadashas
        print(f"\nUpcoming Mahadashas:")
        for i in range(2, min(6, len(dasha_data))):
            md = dasha_data[i]
            print(f"  {md[0]}: {md[1]} to {md[2]} ({md[3]} years)")
            
    except Exception as e:
        print(f"\nDasha calculation error: {e}")
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nLagna (Ascendant): {lagna_name}")
    print(f"Moon Sign (Rashi): {get_rasi_name(int(chart_data[0][2] / 30))}")
    print(f"Sun Sign: {get_rasi_name(int(chart_data[0][1] / 30))}")
    print(f"Birth Nakshatra: {nak_name} - Pada {nak_pada}")
    print(f"Birth Tithi: {tithi_info[0]}")
    print(f"Birth Yoga: {yoga_info[0]}")
    print(f"Birth Karana: {karana_info[0]}")
    
    print("\n" + "=" * 80)
    print("CALCULATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

