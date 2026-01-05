"""
PyJHora Example Usage Script
Demonstrates common Vedic Astrology calculations
"""

from jhora.panchanga import drik
from jhora import utils, const
from datetime import datetime


def example_panchanga():
    """Calculate basic panchanga for a given date, time, and place"""
    print("=" * 60)
    print("PANCHANGA CALCULATION EXAMPLE")
    print("=" * 60)
    
    # Define location (example: Chennai, India)
    place = drik.Place('Chennai', 13.0827, 80.2707, +5.5)
    
    # Define date and time
    dob = (2024, 10, 5)  # Year, Month, Day
    tob = (12, 0, 0)     # Hour, Minute, Second
    
    # Convert to Julian Day
    jd = utils.julian_day_number(dob, tob)
    
    print(f"\nLocation: {place.Place}")
    print(f"Date: {dob[0]}-{dob[1]:02d}-{dob[2]:02d}")
    print(f"Time: {tob[0]:02d}:{tob[1]:02d}:{tob[2]:02d}")
    print(f"Julian Day: {jd:.2f}\n")
    
    # Calculate sunrise and sunset
    sunrise = drik.sunrise(jd, place)
    sunset = drik.sunset(jd, place)
    print(f"Sunrise: {sunrise[1]}")
    print(f"Sunset: {sunset[1]}")
    
    # Calculate tithi
    tithi_info = drik.tithi(jd, place)
    tithi_names = ['Prathama', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
                   'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
                   'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya']
    tithi_num = tithi_info[0]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    tithi_name = tithi_names[(tithi_num - 1) % 15]
    print(f"\nTithi: {tithi_name} ({paksha} Paksha)")
    
    # Calculate nakshatra
    nak_info = drik.nakshatra(jd, place)
    nakshatra_names = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
                      'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
                      'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
                      'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
                      'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati']
    print(f"Nakshatra: {nakshatra_names[nak_info[0]]}")
    
    # Calculate yoga
    yoga_info = drik.yogam(jd, place)
    yoga_names = ['Vishkambha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana', 'Atiganda',
                 'Sukarma', 'Dhriti', 'Shoola', 'Ganda', 'Vriddhi', 'Dhruva',
                 'Vyaghata', 'Harshana', 'Vajra', 'Siddhi', 'Vyatipata', 'Variyan',
                 'Parigha', 'Shiva', 'Siddha', 'Sadhya', 'Shubha', 'Shukla',
                 'Brahma', 'Indra', 'Vaidhriti']
    print(f"Yoga: {yoga_names[yoga_info[0] - 1]}")
    
    # Calculate karana
    karana_info = drik.karana(jd, place)
    karana_names = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
                   'Shakuni', 'Chatushpada', 'Naga', 'Kimstughna']
    print(f"Karana: {karana_names[karana_info[0]]}")
    
    # Calculate vaara (weekday)
    vaara = drik.vaara(jd)
    vaara_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    print(f"Vaara: {vaara_names[vaara]}")
    
    # Rahu Kala
    rahu_kala = drik.raahu_kaalam(jd, place)
    print(f"\nRahu Kala: {rahu_kala[0]} - {rahu_kala[1]}")


def example_planet_positions():
    """Calculate positions of planets"""
    print("\n\n" + "=" * 60)
    print("PLANET POSITIONS EXAMPLE")
    print("=" * 60)
    
    place = drik.Place('Mumbai', 19.0760, 72.8777, +5.5)
    dob = (2024, 10, 5)
    tob = (12, 0, 0)
    jd = utils.julian_day_number(dob, tob)
    
    print(f"\nDate: {dob[0]}-{dob[1]:02d}-{dob[2]:02d} at {tob[0]:02d}:{tob[1]:02d}")
    print(f"Location: {place.Place}\n")
    
    planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    rasi_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    print("Planet Longitudes:")
    print("-" * 50)
    
    for i in range(7):  # Sun to Saturn
        longitude = drik.sidereal_longitude(jd, i)
        rasi = int(longitude / 30)
        degrees_in_rasi = longitude % 30
        print(f"{planet_names[i]:10s}: {longitude:7.2f}° ({rasi_names[rasi]}, {degrees_in_rasi:.2f}°)")
    
    # Calculate ascendant (Lagna)
    asc_data = drik.ascendant(jd, place)
    asc = asc_data[0] if isinstance(asc_data, (list, tuple)) else asc_data
    asc_rasi = int(asc / 30)
    asc_deg = asc % 30
    print(f"{'Ascendant':10s}: {asc:7.2f}° ({rasi_names[asc_rasi]}, {asc_deg:.2f}°)")


def example_horoscope_chart():
    """Generate basic horoscope information"""
    print("\n\n" + "=" * 60)
    print("HOROSCOPE CHART EXAMPLE")
    print("=" * 60)
    
    from jhora.horoscope.chart import charts
    
    place = drik.Place('Delhi', 28.6139, 77.2090, +5.5)
    dob = (1990, 1, 15)
    tob = (10, 30, 0)
    jd = utils.julian_day_number(dob, tob)
    
    print(f"\nBirth Details:")
    print(f"Date: {dob[0]}-{dob[1]:02d}-{dob[2]:02d}")
    print(f"Time: {tob[0]:02d}:{tob[1]:02d}")
    print(f"Place: {place.Place}\n")
    
    # Get Rasi chart
    rasi_chart = charts.rasi_chart(jd, place)
    
    print("Rasi Chart (D-1):")
    print("-" * 50)
    
    planet_names_short = ['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa', 'Ra', 'Ke', 'La']
    rasi_names = const.rasi_names_en
    
    # Group planets by house
    houses = {}
    for planet_idx, (rasi, longitude) in enumerate(rasi_chart):
        if rasi not in houses:
            houses[rasi] = []
        houses[rasi].append(planet_names_short[planet_idx])
    
    for house in range(12):
        planets_in_house = houses.get(house, [])
        planets_str = ', '.join(planets_in_house) if planets_in_house else '-'
        print(f"House {house + 1:2d} ({rasi_names[house]:10s}): {planets_str}")
    
    # Get Navamsa chart
    print("\nNavamsa Chart (D-9):")
    print("-" * 50)
    navamsa_chart = charts.navamsa_chart(jd, place)
    
    houses_d9 = {}
    for planet_idx, (rasi, longitude) in enumerate(navamsa_chart):
        if rasi not in houses_d9:
            houses_d9[rasi] = []
        houses_d9[rasi].append(planet_names_short[planet_idx])
    
    for house in range(12):
        planets_in_house = houses_d9.get(house, [])
        planets_str = ', '.join(planets_in_house) if planets_in_house else '-'
        print(f"House {house + 1:2d} ({rasi_names[house]:10s}): {planets_str}")


def example_dhasa_calculation():
    """Calculate Vimsottari Dasha"""
    print("\n\n" + "=" * 60)
    print("VIMSOTTARI DASHA EXAMPLE")
    print("=" * 60)
    
    from jhora.horoscope.dhasa.graha import vimsottari
    
    place = drik.Place('Bangalore', 12.9716, 77.5946, +5.5)
    dob = (1990, 5, 10)
    tob = (14, 30, 0)
    
    print(f"\nBirth Details:")
    print(f"Date: {dob[0]}-{dob[1]:02d}-{dob[2]:02d}")
    print(f"Time: {tob[0]:02d}:{tob[1]:02d}")
    print(f"Place: {place.Place}\n")
    
    jd = utils.julian_day_number(dob, tob)
    
    # Calculate Vimsottari Dasha
    dhasa_periods = vimsottari.vimsottari_dhasa(dob, tob, place)
    
    planet_names = ['Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus']
    
    print("Vimsottari Maha Dasha Periods:")
    print("-" * 70)
    print(f"{'Planet':<10} {'Start Date':<12} {'End Date':<12} {'Duration (years)'}")
    print("-" * 70)
    
    for period in dhasa_periods[:9]:  # Show first 9 periods
        planet_idx = period[0]
        start_date = period[1]
        end_date = period[2]
        duration = period[3]
        
        print(f"{planet_names[planet_idx]:<10} {start_date[0]:04d}-{start_date[1]:02d}-{start_date[2]:02d}  "
              f"{end_date[0]:04d}-{end_date[1]:02d}-{end_date[2]:02d}  {duration:.2f}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PyJHora - Vedic Astrology Calculations")
    print("Example Usage Demonstrations")
    print("=" * 60)
    
    # Run examples - comment out examples that have errors
    try:
        example_panchanga()
    except Exception as e:
        print(f"Error in panchanga example: {e}")
    
    try:
        example_planet_positions()
    except Exception as e:
        print(f"Error in planet positions example: {e}")
    
    # Commenting out complex examples for now
    # try:
    #     example_horoscope_chart()
    # except Exception as e:
    #     print(f"Error in horoscope chart example: {e}")
    
    # try:
    #     example_dhasa_calculation()
    # except Exception as e:
    #     print(f"Error in dhasa calculation example: {e}")
    
    print("\n\n" + "=" * 60)
    print("Basic examples completed!")
    print("=" * 60)
    print("\nFor GUI applications with full features, run:")
    print("  python -m jhora.ui.horo_chart_tabs")
    print("  python -m jhora.ui.panchangam")
    print("\nFor more examples, see the documentation in src/jhora/")

