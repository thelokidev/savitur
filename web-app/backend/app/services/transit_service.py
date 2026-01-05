"""
Transit Service - Handles transit calculations using PyJHora
"""
import sys
import os
from datetime import datetime, date
from typing import Optional, Any, Dict, List

# Add PyJHora to path
pyjhora_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))
if pyjhora_path not in sys.path:
    sys.path.insert(0, pyjhora_path)

from jhora.panchanga import drik
from jhora.horoscope.chart import charts
from jhora import utils, const

# Rasi names
RASI_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
              'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
RASI_SHORT = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

NAKSHATRA_NAMES = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Ayanamsa modes mapping
AYANAMSA_MODES = {
    'LAHIRI': 'LAHIRI',
    'KP': 'KP',
    'RAMAN': 'RAMAN',
    'TRUE_CITRA': 'TRUE_CITRA',
    'TRUE_PUSHYA': 'TRUE_PUSHYA',
}


class TransitService:
    """Service for calculating transit positions"""
    
    def _parse_birth_details(self, birth_details: dict) -> tuple:
        """Parse birth details into PyJHora format"""
        # Parse date
        date_str = birth_details.get('date', '')
        if isinstance(date_str, str):
            date_parts = date_str.split('-')
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
        else:
            year, month, day = date_str.year, date_str.month, date_str.day
        dob = drik.Date(year, month, day)
        
        # Parse time
        time_str = birth_details.get('time', '12:00:00')
        if isinstance(time_str, str):
            time_parts = time_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            second = int(float(time_parts[2])) if len(time_parts) > 2 else 0
        else:
            hour, minute, second = 12, 0, 0
        tob = (hour, minute, second)
        
        # Parse place
        place_data = birth_details.get('place', {})
        latitude = float(place_data.get('latitude', 0))
        longitude = float(place_data.get('longitude', 0))
        timezone = float(place_data.get('timezone', 5.5))
        place_name = place_data.get('name', 'Unknown')
        
        place = drik.Place(place_name, latitude, longitude, timezone)
        
        # Set ayanamsa
        ayanamsa = birth_details.get('ayanamsa', 'LAHIRI')
        ayanamsa_mode = AYANAMSA_MODES.get(ayanamsa.upper(), 'LAHIRI')
        drik.set_ayanamsa_mode(ayanamsa_mode)
        
        return dob, tob, place, ayanamsa_mode
    
    def _parse_transit_datetime(self, transit_datetime: Optional[str], place: drik.Place) -> float:
        """Parse transit datetime string to Julian Day"""
        if transit_datetime:
            try:
                # Parse ISO format datetime
                if 'T' in transit_datetime:
                    dt = datetime.fromisoformat(transit_datetime.replace('Z', '+00:00'))
                else:
                    dt = datetime.strptime(transit_datetime, '%Y-%m-%d %H:%M:%S')
                transit_dob = drik.Date(dt.year, dt.month, dt.day)
                transit_tob = (dt.hour, dt.minute, dt.second)
            except:
                # Default to now
                now = datetime.now()
                transit_dob = drik.Date(now.year, now.month, now.day)
                transit_tob = (now.hour, now.minute, now.second)
        else:
            # Default to current time
            now = datetime.now()
            transit_dob = drik.Date(now.year, now.month, now.day)
            transit_tob = (now.hour, now.minute, now.second)
        
        jd = utils.julian_day_number(transit_dob, transit_tob)
        return jd, transit_dob, transit_tob
    
    def _get_planet_position(self, jd: float, place: drik.Place, planet_index: int) -> dict:
        """Get position details for a single planet"""
        try:
            jd_utc = jd - place.timezone / 24.0
            
            if planet_index == 8:  # Ketu
                rahu_long = drik.sidereal_longitude(jd_utc, const._RAHU)
                longitude = (rahu_long + 180) % 360
            elif planet_index == 7:  # Rahu
                longitude = drik.sidereal_longitude(jd_utc, const._RAHU)
            else:
                planet_const = [const._SUN, const._MOON, const._MARS, const._MERCURY, 
                               const._JUPITER, const._VENUS, const._SATURN][planet_index]
                longitude = drik.sidereal_longitude(jd_utc, planet_const)
            
            # Calculate rasi and degree
            rasi = int(longitude / 30)
            degree_in_rasi = longitude % 30
            degrees = int(degree_in_rasi)
            minutes = int((degree_in_rasi - degrees) * 60)
            
            # Get nakshatra
            nak_num, pada, _ = drik.nakshatra_pada(longitude)
            nakshatra_name = NAKSHATRA_NAMES[nak_num - 1] if 1 <= nak_num <= 27 else 'Unknown'
            
            return {
                'longitude': longitude,
                'rasi': rasi,
                'rasi_name': RASI_NAMES[rasi],
                'rasi_short': RASI_SHORT[rasi],
                'degree': degrees,
                'minute': minutes,
                'degree_str': f"{degrees}°{minutes:02d}'",
                'nakshatra': nakshatra_name,
                'nakshatra_num': nak_num,
                'pada': pada,
                'nakshatra_pada': f"{nakshatra_name}-{pada}"
            }
        except Exception as e:
            return {
                'longitude': 0,
                'rasi': 0,
                'rasi_name': 'Unknown',
                'rasi_short': '---',
                'degree': 0,
                'minute': 0,
                'degree_str': "0°00'",
                'nakshatra': 'Unknown',
                'nakshatra_num': 1,
                'pada': 1,
                'nakshatra_pada': 'Unknown-1',
                'error': str(e)
            }
    
    def _get_house_from_reference(self, planet_rasi: int, reference_rasi: int) -> int:
        """Calculate house number from a reference point (Lagna or Moon)"""
        return ((planet_rasi - reference_rasi) % 12) + 1
    
    def get_current_transit(self, birth_details: dict, transit_datetime: Optional[str] = None) -> dict:
        """Get current transit positions for all planets"""
        try:
            dob, tob, place, ayanamsa = self._parse_birth_details(birth_details)
            jd_transit, transit_dob, transit_tob = self._parse_transit_datetime(transit_datetime, place)
            
            # Get retrograde planets
            try:
                retro_planets = drik.planets_in_retrograde(jd_transit, place)
            except:
                retro_planets = []
            
            planets = {}
            for i, planet_name in enumerate(PLANET_NAMES):
                pos = self._get_planet_position(jd_transit, place, i)
                pos['is_retrograde'] = i in retro_planets
                pos['planet'] = planet_name
                pos['planet_index'] = i
                planets[planet_name] = pos
            
            return {
                'transit_date': f"{transit_dob.year}-{transit_dob.month:02d}-{transit_dob.day:02d}",
                'transit_time': f"{transit_tob[0]:02d}:{transit_tob[1]:02d}:{transit_tob[2]:02d}",
                'planets': planets
            }
        except Exception as e:
            return {'error': f"Transit calculation error: {str(e)}"}
    
    def get_transit_vs_natal(self, birth_details: dict, transit_datetime: Optional[str] = None) -> dict:
        """Get both natal and transit positions with house calculations from both Lagna and Moon"""
        try:
            dob, tob, place, ayanamsa = self._parse_birth_details(birth_details)
            jd_natal = utils.julian_day_number(dob, tob)
            jd_transit, transit_dob, transit_tob = self._parse_transit_datetime(transit_datetime, place)
            
            # Get natal chart
            natal_chart = charts.rasi_chart(jd_natal, place)
            
            # Get natal Lagna and Moon rasi
            natal_lagna_rasi = natal_chart[0][1][0]  # Ascendant rasi
            natal_moon_rasi = natal_chart[2][1][0]   # Moon rasi
            
            # Get natal planet positions
            natal_planets = {}
            for i, planet_name in enumerate(PLANET_NAMES):
                pos = self._get_planet_position(jd_natal, place, i)
                pos['planet'] = planet_name
                pos['planet_index'] = i
                natal_planets[planet_name] = pos
            
            # Get transit retrograde planets
            try:
                retro_planets = drik.planets_in_retrograde(jd_transit, place)
            except:
                retro_planets = []
            
            # Get transit planet positions with house from both references
            transit_planets = {}
            for i, planet_name in enumerate(PLANET_NAMES):
                pos = self._get_planet_position(jd_transit, place, i)
                pos['is_retrograde'] = i in retro_planets
                pos['planet'] = planet_name
                pos['planet_index'] = i
                
                # Calculate house from Lagna
                pos['house_from_lagna'] = self._get_house_from_reference(pos['rasi'], natal_lagna_rasi)
                
                # Calculate house from Moon
                pos['house_from_moon'] = self._get_house_from_reference(pos['rasi'], natal_moon_rasi)
                
                transit_planets[planet_name] = pos
            
            return {
                'birth_date': f"{dob.year}-{dob.month:02d}-{dob.day:02d}",
                'birth_time': f"{tob[0]:02d}:{tob[1]:02d}:{tob[2]:02d}",
                'transit_date': f"{transit_dob.year}-{transit_dob.month:02d}-{transit_dob.day:02d}",
                'transit_time': f"{transit_tob[0]:02d}:{transit_tob[1]:02d}:{transit_tob[2]:02d}",
                'natal_lagna_rasi': natal_lagna_rasi,
                'natal_lagna_name': RASI_NAMES[natal_lagna_rasi],
                'natal_moon_rasi': natal_moon_rasi,
                'natal_moon_name': RASI_NAMES[natal_moon_rasi],
                'natal_planets': natal_planets,
                'transit_planets': transit_planets
            }
        except Exception as e:
            import traceback
            return {'error': f"Transit overlay calculation error: {str(e)}", 'traceback': traceback.format_exc()}
    
    def get_planet_entry_dates(self, birth_details: dict, transit_datetime: Optional[str] = None) -> dict:
        """Get upcoming sign entry dates for all planets"""
        try:
            dob, tob, place, ayanamsa = self._parse_birth_details(birth_details)
            jd_transit, transit_dob, transit_tob = self._parse_transit_datetime(transit_datetime, place)
            
            entries = []
            
            # Only calculate for slower moving planets (Mars to Saturn, Rahu, Ketu)
            # Sun and Moon change signs too frequently
            planets_to_check = [
                (0, 'Sun'),
                (2, 'Mars'),
                (3, 'Mercury'),
                (4, 'Jupiter'),
                (5, 'Venus'),
                (6, 'Saturn'),
            ]
            
            for planet_idx, planet_name in planets_to_check:
                try:
                    result = drik.next_planet_entry_date(planet_idx, jd_transit, place, direction=1)
                    if result:
                        entry_jd, entry_long = result
                        entry_rasi = int(entry_long / 30)
                        
                        # Convert JD to datetime
                        y, m, d, fh = drik.jd_to_gregorian(entry_jd)
                        hours = int(fh)
                        minutes = int((fh - hours) * 60)
                        
                        entries.append({
                            'planet': planet_name,
                            'planet_index': planet_idx,
                            'entering_rasi': entry_rasi,
                            'entering_rasi_name': RASI_NAMES[entry_rasi],
                            'entry_date': f"{int(y)}-{int(m):02d}-{int(d):02d}",
                            'entry_time': f"{hours:02d}:{minutes:02d}",
                            'entry_datetime': f"{int(y)}-{int(m):02d}-{int(d):02d} {hours:02d}:{minutes:02d}",
                            'entry_jd': entry_jd
                        })
                except Exception as e:
                    # Skip this planet if calculation fails
                    pass
            
            # Sort by entry date
            entries.sort(key=lambda x: x.get('entry_jd', 0))
            
            return {
                'from_date': f"{transit_dob.year}-{transit_dob.month:02d}-{transit_dob.day:02d}",
                'entries': entries
            }
        except Exception as e:
            return {'error': f"Planet entry calculation error: {str(e)}"}


# Singleton instance
_transit_service = None

def get_transit_service() -> TransitService:
    global _transit_service
    if _transit_service is None:
        _transit_service = TransitService()
    return _transit_service
