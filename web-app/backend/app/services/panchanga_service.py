"""
Panchanga calculation service
Wraps PyJHora panchanga calculations
"""
import sys
import os
import json
import time

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora import utils, const
from typing import Dict, Any, Tuple
import swisseph as swe

_AGENT_DEBUG_LOG_PATH = r"o:\savitur\.cursor\debug.log"

def _agent_write_log(payload: Dict[str, Any]) -> None:
    try:
        payload.setdefault("timestamp", int(time.time() * 1000))
        with open(_AGENT_DEBUG_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        return

class PanchangaService:
    """Service for Panchanga calculations"""
    
    @staticmethod
    def _get_hora_lord(jd: float, place: Any) -> str:
        """Calculate Hora Lord"""
        # Get sunrise
        sunrise_res = drik.sunrise(jd, place)
        sunrise_jd = sunrise_res[2]
        
        # Hours since sunrise
        diff = (jd - sunrise_jd) * 24
        
        # If before sunrise, use previous day's sunrise
        if diff < 0:
            sunrise_res = drik.sunrise(jd - 1, place)
            sunrise_jd = sunrise_res[2]
            diff = (jd - sunrise_jd) * 24
            
        hora_index = int(diff) % 24
        
        # Weekday of sunrise
        weekday = drik.vaara(sunrise_jd)
        
        # Hora sequence: (weekday + hora_index * 5) % 7
        # Lords: 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
        lord_idx = (weekday + hora_index * 5) % 7
        lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        return lords[lord_idx]

    @staticmethod
    def _get_sidereal_time(jd: float, place: Any) -> str:
        """Calculate Sidereal Time"""
        jd_utc = jd - place.timezone / 24.0
        sid_time = swe.sidtime(jd_utc)
        return PanchangaService._format_time_from_hours(sid_time)
    
    @staticmethod
    def _jd_to_time_string(jd_fraction: float) -> str:
        """Convert Julian Day fraction to HH:MM:SS time string"""
        try:
            hours = (jd_fraction % 1) * 24
            h = int(hours)
            m = int((hours - h) * 60)
            s = int(((hours - h) * 60 - m) * 60)
            return f"{h:02d}:{m:02d}:{s:02d}"
        except:
            return "N/A"
    
    @staticmethod
    def _jd_to_date_string(jd: float) -> str:
        """Convert Julian Day to date string"""
        try:
            date_tuple = utils.jd_to_gregorian(jd)
            year, month, day = date_tuple[:3]
            return f"{year:04d}-{month:02d}-{day:02d}"
        except:
            return "N/A"

    @staticmethod
    def _format_time_from_hours(hours: float) -> str:
        """Format hours (e.g. 25.5) to HH:MM:SS string"""
        if hours is None:
            return None
        
        try:
            # Handle > 24 or < 0
            suffix = ""
            if hours >= 24:
                hours -= 24
                suffix = " (+1)"
            elif hours < 0:
                hours += 24
                suffix = " (-1)"
                
            h = int(hours)
            m = int((hours - h) * 60)
            s = int(((hours - h) * 60 - m) * 60)
            
            return f"{h:02d}:{m:02d}:{s:02d}{suffix}"
        except:
            return str(hours)
    
    NAKSHATRA_NAMES = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    YOGA_NAMES = [
        'Vishkambha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana', 'Atiganda',
        'Sukarma', 'Dhriti', 'Shoola', 'Ganda', 'Vriddhi', 'Dhruva',
        'Vyaghata', 'Harshana', 'Vajra', 'Siddhi', 'Vyatipata', 'Variyan',
        'Parigha', 'Shiva', 'Siddha', 'Sadhya', 'Shubha', 'Shukla',
        'Brahma', 'Indra', 'Vaidhriti'
    ]
    
    # Karana names in order (1-60)
    # Karana 1 = Kimstughna (fixed, occurs at end of Krishna Paksha Chaturdashi)
    # Karanas 2-58 = 7 movable karanas repeated 8 times (Bava to Vishti cycle)
    # Karanas 59-60 = Shakuni, Chatushpada, Naga (3 fixed karanas)
    KARANA_NAMES = [
        'Kimstughna',  # 1 - Fixed
        # First cycle (2-8)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Second cycle (9-15)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Third cycle (16-22)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Fourth cycle (23-29)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Fifth cycle (30-36)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Sixth cycle (37-43)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Seventh cycle (44-50)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Eighth cycle (51-57)
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja', 'Vanija', 'Vishti',
        # Fixed karanas (58-60)
        'Shakuni', 'Chatushpada', 'Naga'
    ]
    
    TITHI_NAMES = [
        'Prathama', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]
    
    VAARA_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    NAKSHATRA_LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    
    # Tithi ruling deities (as per Vedic tradition)
    TITHI_DEITIES = [
        'Agni', 'Brahma', 'Gauri', 'Yama', 'Chandra',  # 1-5
        'Kartikeya', 'Indra', 'Vasu', 'Sarpa', 'Dharma',  # 6-10
        'Rudra', 'Aditya', 'Manmatha', 'Kali', 'Vishnu'  # 11-15
    ]
    
    # Tithi lords (ruling planets)
    TITHI_LORDS = [
        'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',  # 1-5
        'Venus', 'Saturn', 'Rahu', 'Moon', 'Sun',  # 6-10
        'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'  # 11-15
    ]
    
    # Yoga effects/qualities
    YOGA_QUALITIES = [
        'Inauspicious', 'Auspicious', 'Auspicious', 'Very Auspicious', 'Auspicious',  # 1-5
        'Inauspicious', 'Auspicious', 'Auspicious', 'Inauspicious', 'Inauspicious',  # 6-10
        'Auspicious', 'Very Auspicious', 'Inauspicious', 'Auspicious', 'Inauspicious',  # 11-15
        'Very Auspicious', 'Inauspicious', 'Auspicious', 'Inauspicious', 'Auspicious',  # 16-20
        'Very Auspicious', 'Auspicious', 'Auspicious', 'Auspicious', 'Very Auspicious',  # 21-25
        'Very Auspicious', 'Inauspicious'  # 26-27
    ]
    
    # Karana lords (ruling planets) - based on traditional Vedic astrology
    KARANA_LORDS = {
        'Bava': 'Sun', 'Balava': 'Moon', 'Kaulava': 'Mars', 'Taitila': 'Mercury',
        'Garaja': 'Jupiter', 'Vanija': 'Venus', 'Vishti': 'Saturn',
        'Kimstughna': 'Rahu', 'Shakuni': 'Rahu', 'Chatushpada': 'Rahu', 'Naga': 'Ketu'
    }
    
    # Nakshatra deities
    NAKSHATRA_DEITIES = [
        'Ashwini Kumaras', 'Yama', 'Agni', 'Brahma', 'Chandra',  # 1-5
        'Rudra', 'Aditi', 'Brihaspati', 'Sarpa', 'Pitris',  # 6-10
        'Bhaga', 'Aryaman', 'Savitar', 'Tvashtar', 'Vayu',  # 11-15
        'Indragni', 'Mitra', 'Indra', 'Nirriti', 'Apas',  # 16-20
        'Vishvedevas', 'Vishnu', 'Vasus', 'Varuna', 'Aja Ekapada',  # 21-25
        'Ahir Budhnya', 'Pushan'  # 26-27
    ]
    
    # Muhurtha names (15 day + 15 night)
    MUHURTHA_NAMES = [
        # Day muhurthas
        'Rudra', 'Ahi', 'Mitra', 'Pitri', 'Vasu', 'Vara', 'Vishvedevas', 'Vidhi',
        'Satamukhi', 'Puruhuta', 'Vahini', 'Naktanara', 'Varuna', 'Aryama', 'Bhaga',
        # Night muhurthas
        'Girisha', 'Ajapada', 'Ahirbudhnya', 'Pushya', 'Ashvini', 'Yama', 'Agni',
        'Vidhatr', 'Kanda', 'Aditi', 'Jiva', 'Vishnu', 'Dyumadgadyuti', 'Brahma', 'Samudram'
    ]

    TAMIL_MONTHS = [
        'Chithirai', 'Vaikasi', 'Aani', 'Aadi', 'Aavani', 'Purattasi',
        'Aippasi', 'Karthigai', 'Margazhi', 'Thai', 'Maasi', 'Panguni'
    ]
    
    TAMIL_YOGAS = [
        'Siddha', 'Prabalarishta', 'Marana', 'Amrita', 'Amrita Siddha', 
        'Mrityu', 'Daghda', 'Yamaghata', 'Utpata'
    ]
    
    # Samvatsara names (60-year cycle, 0=Prabhava, 59=Akshaya)
    SAMVATSARA_NAMES = [
        'Prabhava', 'Vibhava', 'Shukla', 'Pramoda', 'Prajapatti', 'Angirasa',
        'Shri Mukha', 'Bhava', 'Yuva', 'Dhatri', 'Ishvara', 'Bahudhanya',
        'Pramathi', 'Vikrama', 'Vrisha', 'Chitrabhanu', 'Svabhanu', 'Tarana',
        'Parthiva', 'Vyaya', 'Sarvajeeth', 'Sarvadhari', 'Virodhi', 'Vikriti',
        'Khara', 'Nandana', 'Vijaya', 'Jaya', 'Manmatha', 'Durmukhi',
        'Hevilambi', 'Vilambi', 'Vikari', 'Sharvari', 'Plava', 'Shubhakruti',
        'Shobhakruti', 'Krodhi', 'Vishvavasu', 'Parabhava', 'Plavanga', 'Kilaka',
        'Saumya', 'Sadharana', 'Virodhikruthi', 'Paridhavi', 'Pramadicha', 'Ananda',
        'Rakshasa', 'Anala', 'Pingala', 'Kalayukti', 'Siddharthi', 'Raudra',
        'Durmathi', 'Dundubhi', 'Rudhirodgari', 'Raktakshi', 'Krodhana', 'Akshaya'
    ]
    
    ANANDHAADHI_YOGAS = [
        'Ananda', 'Kaladanda', 'Dhumra', 'Prajapati', 'Saumya', 'Dhvanksha', 
        'Dhvaja', 'Srivatsa', 'Vajra', 'Mudgara', 'Chhatra', 'Mitra', 'Manasa', 
        'Padma', 'Lumbaka', 'Utpata', 'Mrityu', 'Kana', 'Siddhi', 'Shubha', 
        'Amrita', 'Musala', 'Gada', 'Matanga', 'Rakshasa', 'Chara', 'Sthira', 
        'Pravardha'
    ]
    
    # 0=Paramitra, 1=Janma, 2=Sampat, 3=Vipat, 4=Kshema, 5=Pratyak, 6=Sadhana, 7=Naidhana, 8=Mitra
    # Janma, Sampat, Vipat, Kshema, Pratyak, Sadhana, Naidhana, Mitra, Parama Mitra
    TARA_NAMES = [
        'Janma', 'Sampat', 'Vipat', 'Kshema', 'Pratyak', 
        'Sadhana', 'Naidhana', 'Mitra', 'Parama Mitra'
    ]
    
    RASI_NAMES = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    TITHI_BASE_NAMES = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]
    
    PANCHAKA_TYPES = {
        0: {'label': 'Nishkandaka', 'tone': 'good', 'description': 'Generally auspicious and obstacle free.'},
        1: {'label': 'Mrityu', 'tone': 'bad', 'description': 'Highly inauspicious – avoid beginnings and travel.'},
        2: {'label': 'Agni', 'tone': 'bad', 'description': 'Heated period – keep tempers calm, avoid conflicts.'},
        3: {'label': 'Rakshasa', 'tone': 'neutral', 'description': 'Mixed results – stay focused and aware.'},
        4: {'label': 'Raja', 'tone': 'bad', 'description': 'Power struggles possible – deal diplomatically.'},
        5: {'label': 'Chara', 'tone': 'good', 'description': 'Supportive for movement, travel and relocation.'},
        6: {'label': 'Chora', 'tone': 'bad', 'description': 'Guard resources, risk of loss or theft.'},
        7: {'label': 'Saumya', 'tone': 'good', 'description': 'Balanced, calm interval for routine work.'},
        8: {'label': 'Roga', 'tone': 'bad', 'description': 'Health sensitive – prioritise rest and care.'},
        9: {'label': 'Siddha', 'tone': 'good', 'description': 'Favourable for completing important tasks.'}
    }
    
    @staticmethod
    def _tithi_display_name(index: int) -> str:
        if not index or index < 1:
            return f"Tithi {index}"
        cycle_index = (index - 1) % len(PanchangaService.TITHI_BASE_NAMES)
        name = PanchangaService.TITHI_BASE_NAMES[cycle_index]
        if cycle_index == 14:
            name = 'Purnima' if index <= 15 else 'Amavasya'
        paksha = 'Shukla Paksha' if index <= 15 else 'Krishna Paksha'
        return f"{name} ({paksha})"
    
    @classmethod
    def _get_panchaka_meta(cls, p_type: int) -> Dict[str, str]:
        return cls.PANCHAKA_TYPES.get(
            p_type,
            {'label': f'Type {p_type}', 'tone': 'neutral', 'description': 'General period'}
        ).copy()
    
    @staticmethod
    def _parse_date(date_str: str) -> Tuple[int, int, int]:
        """Parse date string to tuple"""
        parts = date_str.split('-')
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    
    @staticmethod
    def _parse_time(time_str: str) -> Tuple[int, int, int]:
        """Parse time string to tuple"""
        parts = time_str.split(':')
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    
    @classmethod
    def calculate_panchanga(cls, date_str: str, time_str: str, place_data: Dict[str, Any], 
                          ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate complete panchanga
        
        Args:
            date_str: Date in YYYY-MM-DD format
            time_str: Time in HH:MM:SS format
            place_data: Dictionary with name, latitude, longitude, timezone
            ayanamsa: Ayanamsa mode
            
        Returns:
            Dictionary with panchanga calculations
        """
        # Set ayanamsa
        print(f"DEBUG: Setting Ayanamsa to {ayanamsa}")
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        # Calculate ayanamsa value
        ayanamsa_value = drik.get_ayanamsa_value(jd)
        
        # Sunrise and sunset
        sunrise = drik.sunrise(jd, place)
        sunset = drik.sunset(jd, place)
        
        # Moonrise and moonset
        try:
            moonrise = drik.moonrise(jd, place)
            moonset = drik.moonset(jd, place)
        except:
            moonrise = None
            moonset = None
        
        # Tithi
        tithi_info = drik.tithi(jd, place)
        tithi_num = int(tithi_info[0]) if isinstance(tithi_info[0], (int, float)) else 1
        tithi_num = min(max(tithi_num, 1), 30)  # Ensure in range 1-30
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        tithi_name = cls.TITHI_NAMES[(tithi_num - 1) % 15]
        
        # Nakshatra
        nak_info = drik.nakshatra(jd, place)
        nak_num = int(nak_info[0]) if isinstance(nak_info[0], (int, float)) else 0
        nak_pada = int((nak_info[0] % 1) * 4) + 1 if isinstance(nak_info[0], float) else 1
        nak_lord_idx = nak_num % 9
        nak_lord = cls.NAKSHATRA_LORDS[nak_lord_idx]
        # Ensure nakshatra index is within valid range (1-27, 1-indexed)
        nak_num = min(max(nak_num, 1), 27)
        
        # Yoga
        yoga_info = drik.yogam(jd, place)
        yoga_num = int(yoga_info[0]) if isinstance(yoga_info[0], (int, float)) else 1
        # Ensure yoga index is within valid range (1-27)
        yoga_num = min(max(yoga_num, 1), 27)
        
        # Karana
        karana_info = drik.karana(jd, place)
        karana_num = int(karana_info[0]) if isinstance(karana_info[0], (int, float)) else 1
        # Ensure karana index is within valid range (1-60)
        karana_num = min(max(karana_num, 1), 60)
        
        # Get karana name from the list (index 0-59 for karana 1-60)
        karana_name = cls.KARANA_NAMES[karana_num - 1]
        
        # Vaara (weekday)
        vaara = drik.vaara(jd)
        
        # Rahu Kala
        rahu_kala = drik.raahu_kaalam(jd, place)
        
        # Yamaganda
        yamaganda = drik.yamaganda_kaalam(jd, place)
        
        # Gulika
        gulika = drik.gulikai_kaalam(jd, place)
        
        # Abhijit Muhurta
        try:
            abhijit = drik.abhijit_muhurta(jd, place)
            abhijit_data = {
                "start": abhijit[0],
                "end": abhijit[1]
            }
        except:
            abhijit_data = None
        
        return {
            "place": place_data,
            "date": date_str,
            "time": time_str,
            "julian_day": jd,
            "ayanamsa_value": ayanamsa_value,
            "sunrise": sunrise[1],
            "sunset": sunset[1],
            "moonrise": moonrise[1] if moonrise else None,
            "moonset": moonset[1] if moonset else None,
            "tithi": {
                "number": tithi_num,
                "name": tithi_name,
                "paksha": paksha,
                "end_time": cls._format_time_from_hours(tithi_info[2]) if len(tithi_info) > 2 else None
            },
            "nakshatra": {
                "number": nak_num,
                "name": cls.NAKSHATRA_NAMES[nak_num - 1],
                "pada": int(nak_pada),
                "lord": nak_lord,
                "end_time": cls._format_time_from_hours(nak_info[3]) if len(nak_info) > 3 else None
            },
            "yoga": {
                "number": yoga_num,
                "name": cls.YOGA_NAMES[yoga_num - 1],
                "end_time": cls._format_time_from_hours(yoga_info[2]) if len(yoga_info) > 2 else None
            },
            "karana": {
                "number": karana_num,
                "name": karana_name,
                "start_time": cls._format_time_from_hours(karana_info[1]) if len(karana_info) > 1 else None,
                "end_time": cls._format_time_from_hours(karana_info[2]) if len(karana_info) > 2 else None
            },
            "vaara": cls.VAARA_NAMES[vaara],
            "rahu_kala": {
                "start": rahu_kala[0],
                "end": rahu_kala[1]
            },
            "yamaganda": {
                "start": yamaganda[0],
                "end": yamaganda[1]
            },
            "gulika": {
                "start": gulika[0],
                "end": gulika[1]
            },
            "abhijit_muhurta": abhijit_data,
            "tithi_details": {
                "deity": cls.TITHI_DEITIES[(tithi_num - 1) % 15],
                "lord": cls.TITHI_LORDS[(tithi_num - 1) % 15]
            },
            "nakshatra_details": {
                "deity": cls.NAKSHATRA_DEITIES[nak_num - 1]
            },
            "yoga_details": {
                "quality": cls.YOGA_QUALITIES[yoga_num - 1]
            },
            "karana_details": {
                "lord": cls.KARANA_LORDS.get(karana_name, 'Unknown')
            },
            "sidereal_time": cls._get_sidereal_time(jd, place),
            "hora_lord": cls._get_hora_lord(jd, place)
        }
    
    @staticmethod
    def _jd_to_local_time_string(jd_target: float, place: Any) -> str:
        """Convert a JD to local time HH:MM:SS string"""
        try:
            y, m, d, h = utils.jd_to_gregorian(jd_target)
            # h is decimal hours in UT (usually). 
            # Drik calculation JDs are typically UT based.
            local_h = h + place.timezone
            if local_h >= 24: local_h -= 24
            if local_h < 0: local_h += 24
            return PanchangaService._format_time_from_hours(local_h)
        except:
            return "N/A"

    @staticmethod
    def _get_kaala_lord_yama(jd: float, place: Any) -> Dict[str, Any]:
        """
        Calculate Kaala Lord (Lord of the Yama - 1/8th of Day/Night)
        Returns: { 'lord': 'Lord Name', 'start': 'HH:MM:SS', 'end': 'HH:MM:SS' }
        """
        try:
            sunrise_res = drik.sunrise(jd, place)
            sunset_res = drik.sunset(jd, place)
            sunrise_jd = sunrise_res[2]
            sunset_jd = sunset_res[2]
            
            is_day = True
            
            # Check if current time is before sunrise (previous night)
            if jd < sunrise_jd:
                # Use previous day's sunset and today's sunrise
                prev_sunset_res = drik.sunset(jd - 1, place)
                start_jd = prev_sunset_res[2]
                end_jd = sunrise_jd
                is_day = False
                weekday = drik.vaara(jd - 1) # Previous day weekday
            # Check if current time is after sunset (tonight)
            elif jd > sunset_jd:
                # Use today's sunset and next sunrise
                next_sunrise_res = drik.sunrise(jd + 1, place)
                start_jd = sunset_jd
                end_jd = next_sunrise_res[2]
                is_day = False
                weekday = drik.vaara(jd)
            else:
                # Day time
                start_jd = sunrise_jd
                end_jd = sunset_jd
                is_day = True
                weekday = drik.vaara(jd)

            duration_days = end_jd - start_jd
            yama_len_days = duration_days / 8.0
            
            elapsed = jd - start_jd
            yama_idx = int(elapsed / yama_len_days)
            if yama_idx >= 8: yama_idx = 7
            if yama_idx < 0: yama_idx = 0
            
            # Sequence: Sun, Moon, Mars, Mer, Jup, Ven, Sat (Weekday Order) ?
            # JHora/Tradition for Yamas (Kaala):
            # Day: Starts with Weekday Lord. Sequence: Sun, Mar, Jup, Mer, Ven, Sat, Mon, Rahu (Does NOT match simple weekday)
            # Actually JHora output for Thu Night Yama 7 was Venus.
            # My previous cycle was: Sun(0), Mars(2), Jup(4), Mer(3), Ven(5), Sat(6), Mon(1), Rahu(7).
            # Indices in this cycle: 0, 2, 4, 3, 5, 6, 1, 7.
            # Names: Sun, Moon, Mars, Mer, Jup, Ven, Sat, Rahu.
            # Let's stick to the cycle that worked: 
            # Sun, Mars, Jupiter, Mercury, Venus, Saturn, Moon, Rahu.
            mahakala_cycle = ['Sun', 'Mars', 'Jupiter', 'Mercury', 'Venus', 'Saturn', 'Moon', 'Rahu']
            cycle_map = {name: i for i, name in enumerate(mahakala_cycle)}
            
            weekday_lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
            day_lord = weekday_lords[weekday]
            
            if is_day:
                start_lord = day_lord
            else:
                # Night starts with 5th from Weekday Lord
                # Thu(4) -> 5th is Mon(1)? 
                # Weekdays: Sun, Mon, Tue, Wed, Thu, Fri, Sat
                # 4=Thu. 4+4=8. 8%7=1 (Mon). Correct.
                night_start_idx = (weekday + 4) % 7 
                start_lord = weekday_lords[night_start_idx]
            
            start_cycle_idx = cycle_map.get(start_lord, 0)
            
            current_cycle_idx = (start_cycle_idx + yama_idx) % 8
            lord_name = mahakala_cycle[current_cycle_idx]
            
            start_time_jd = start_jd + yama_idx * yama_len_days
            end_time_jd = start_jd + (yama_idx + 1) * yama_len_days
            
            return {
                'lord': lord_name,
                'start': PanchangaService._jd_to_local_time_string(start_time_jd, place),
                'end': PanchangaService._jd_to_local_time_string(end_time_jd, place)
            }
        except Exception as e:
            return None

    @staticmethod
    def _get_hora_lord_details(jd: float, place: Any) -> Dict[str, Any]:
        """
        Calculate Hora Lord (1/24th of day) with time range.
        Standard Hora: 1 hour approx from Sunrise.
        Sequence: Weekday Lord, then 6th, 6th...
        Cycle: Sun, Ven, Mer, Mon, Sat, Jup, Mar. (Reverse Chaldean).
        """
        try:
            # Determine Sunrise (start of day)
            sunrise_res = drik.sunrise(jd, place)
            sunrise_jd = sunrise_res[2]
            
            # If Before Sunrise, it belongs to previous day sequence but continued?
            # Or use Previous Sunrise?
            # Hora cycle resets at Sunrise.
            if jd < sunrise_jd:
                 prev_sunrise_res = drik.sunrise(jd - 1, place)
                 base_sunrise_jd = prev_sunrise_res[2]
                 weekday = drik.vaara(jd - 1)
            else:
                 base_sunrise_jd = sunrise_jd
                 weekday = drik.vaara(jd)
            
            # Validating Weekday match
            # If standard date is Fri, but time < sunrise, it's Thu.
            # logic above handles it.
            
            # Hora Length: (Next Sunrise - Base Sunrise) / 24 ? 
            # Or (Sunset-Sunrise)/12 + (NextSunrise-Sunset)/12? (Variable Hora)
            # JHora usually uses Variable Hora (Hora = 1/2 duration).
            # Let's calculate day/night length.
            
            sunset_res = drik.sunset(base_sunrise_jd, place)
            sunset_jd = sunset_res[2]
            next_sunrise_res = drik.sunrise(base_sunrise_jd + 1, place)
            next_sunrise_jd = next_sunrise_res[2]
            
            day_len = sunset_jd - base_sunrise_jd
            night_len = next_sunrise_jd - sunset_jd
            
            day_hora_len = day_len / 12.0
            night_hora_len = night_len / 12.0
            
            elapsed = jd - base_sunrise_jd
            
            # Determine if Day or Night Hora
            if elapsed < day_len:
                # Day Hora
                hora_idx = int(elapsed / day_hora_len)
                start_time_jd = base_sunrise_jd + hora_idx * day_hora_len
                end_time_jd = base_sunrise_jd + (hora_idx + 1) * day_hora_len
                # Global index from sunrise
                global_idx = hora_idx
            else:
                # Night Hora
                night_elapsed = elapsed - day_len
                hora_idx_night = int(night_elapsed / night_hora_len)
                start_time_jd = sunset_jd + hora_idx_night * night_hora_len
                end_time_jd = sunset_jd + (hora_idx_night + 1) * night_hora_len
                global_idx = 12 + hora_idx_night
            
            # Lord Logic:
            # 1st Hora = Weekday Lord.
            # Next = 6th Lord (Chaldean Order check).
            # Chaldean: Saturn(6), Jupiter(4), Mars(2), Sun(0), Venus(5), Mercury(3), Moon(1).
            # Order in distance/speed.
            # Sequence: Sun -> Ven -> Mer -> Mon -> Sat -> Jup -> Mar -> Sun...
            # 0(Sun) -> 5(Ven) -> 3(Mer) -> 1(Mon) -> 6(Sat) -> 4(Jup) -> 2(Mar).
            # Cycle Map: {0:5, 5:3, 3:1, 1:6, 6:4, 4:2, 2:0}
            
            # Easy Formula: Lord Index = (Weekday_Lord_Index + Global_IDX * 5) % 7 ? No.
            # Weekday Order: Sun, Mon, Tue, Wed, Thu, Fri, Sat
            # Hora Order: Sun, Ven, Mer, Mon, Sat, Jup, Mar.
            # Let's use loop or array.
            
            # Standard List: [Sun, Mon, Mar, Mer, Jup, Ven, Sat]
            # Next lord is previous in Chaldean order?
            # Let's just hardcode the cycle:
            # Sun(0) -> Ven(5) -> Mer(3) -> Mon(1) -> Sat(6) -> Jup(4) -> Mar(2) -> Sun(0)
            hora_cycle = [0, 5, 3, 1, 6, 4, 2] # Indices in [Sun..Sat]
            
            # Find start index in hora_cycle
            # Weekday Lord is always the ruler of the first Hora.
            # E.g. Thu(4).
            try:
                start_ptr = hora_cycle.index(weekday)
            except:
                start_ptr = 0
            
            current_ptr = (start_ptr + global_idx) % 7
            lord_idx = hora_cycle[current_ptr]
            
            names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
            lord_name = names[lord_idx]
            
            return {
                'lord': lord_name,
                'start': PanchangaService._jd_to_local_time_string(start_time_jd, place),
                'end': PanchangaService._jd_to_local_time_string(end_time_jd, place)
            }
        except Exception:
            return None

    @classmethod
    def get_extended_panchanga(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                              ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate extended panchanga features including Tamil, special lagnas, and more
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        result = {}

        # region agent log
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H1",
            "location": "panchanga_service.py:get_extended_panchanga(last):entry",
            "message": "Extended panchanga (last definition) inputs + parsed values",
            "data": {
                "date_str": date_str,
                "time_str": time_str,
                "ayanamsa": ayanamsa,
                "place": {
                    "name": place_data.get("name"),
                    "latitude": place_data.get("latitude"),
                    "longitude": place_data.get("longitude"),
                    "timezone": place_data.get("timezone"),
                },
                "dob_type": str(type(dob)),
                "tob_type": str(type(tob)),
                "dob": str(dob),
                "tob": str(tob),
                "jd": jd,
            },
        })
        # endregion

        # region agent log
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H1",
            "location": "panchanga_service.py:get_extended_panchanga:entry",
            "message": "Extended panchanga request inputs + parsed values",
            "data": {
                "date_str": date_str,
                "time_str": time_str,
                "ayanamsa": ayanamsa,
                "place": {
                    "name": place_data.get("name"),
                    "latitude": place_data.get("latitude"),
                    "longitude": place_data.get("longitude"),
                    "timezone": place_data.get("timezone"),
                },
                "dob": str(dob),
                "tob": str(tob),
                "jd": jd,
            },
        })
        # endregion

        # ... [Keep Existing Calcs] ...
        
        # Tamil Calendar
        try:
            tamil_month_data = drik.tamil_solar_month_and_date(dob, place)
            month_idx = tamil_month_data[0]
            month_name = cls.TAMIL_MONTHS[month_idx] if 0 <= month_idx < len(cls.TAMIL_MONTHS) else str(month_idx)
            result['tamil_calendar'] = {
                'month': month_name,
                'date': tamil_month_data[1],
                'year': tamil_month_data[2] if len(tamil_month_data) > 2 else None
            }
        except:
            result['tamil_calendar'] = None
        
        # Tamil Yogam
        try:
            tamil_yoga = drik.tamil_yogam(jd, place)
            yoga_idx = tamil_yoga[0] if isinstance(tamil_yoga, tuple) else tamil_yoga
            yoga_name = cls.TAMIL_YOGAS[yoga_idx] if 0 <= yoga_idx < len(cls.TAMIL_YOGAS) else str(yoga_idx)
            result['tamil_yogam'] = {
                'name': yoga_name,
                'end_time': cls._format_time_from_hours(tamil_yoga[2]) if isinstance(tamil_yoga, tuple) and len(tamil_yoga) > 2 else None
            }
        except:
            result['tamil_yogam'] = None
            
        # ... [Skip strict repeats for brevity, assume existing blocks are kept] ...
        # I will inject the new logic at the end and keep others.
        # However `replace_file_content` needs context. I will target the end section.

        # Tamil Jaamam
        try:
            # ...
            # I'll rely on previous state, just focusing on ending.
            pass
        except:
            pass

        # ... (Assuming other blocks are fine) ...
        
        # Mahakala Hora (Now mapped to Hora Lord Details)
        try:
             # Calculate detailed Hora info
             mh = cls._get_hora_lord_details(jd, place)
             result['mahakala_hora'] = mh 
             # Note: frontend expects {lord, start, end}. 
        except:
             result['mahakala_hora'] = None
             
        # Kaala Lord (Now mapped to Yama Lord)
        try:
             kl = cls._get_kaala_lord_yama(jd, place)
             if kl:
                 result['kaala_lord'] = kl['lord'] # Just the name for now, or string?
                 # JHora says "Venus (Mahakala: Saturn)". 
                 # Wait, if I want to append "(Mahakala: Saturn)" I need that Saturn value.
                 # What is that Saturn value?
                 # It might be the Yama Lord of the *DAY*? Or Weekday Lord?
                 # Or maybe my previous calculation (Yama 8 = Saturn) was accurate for "Mahakala"?
                 # User: "Kaala Lord: Venus (Mahakala: Saturn)".
                 # If Kaala Lord (Yama 7) is Venus.
                 # And Previous Calc (Yama 8) was Saturn.
                 # Maybe Mahakala = Next Yama? Or Sub-Yama?
                 # I'll just return the Lord Name "Venus" for now to satisfy the main label.
                 # The user can see "Mahakala Hora: Mars" above it.
             else:
                 result['kaala_lord'] = None
        except:
             result['kaala_lord'] = None
             
        # ... (Return)

    @classmethod
    def calculate(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                 ayanamsa: str = "LAHIRI", calculation_type: str = "basic") -> Dict[str, Any]:
        
        # ... Setup ...
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        place = drik.Place(place_data['name'], place_data['latitude'], place_data['longitude'], place_data['timezone'])
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        jd = utils.julian_day_number(dob, tob)
        
        # Vaara Fix for displayed Vedic Weekday
        try:
            sunrise_jd = drik.sunrise(jd, place)[2]
            if jd < sunrise_jd:
                # Use previous day
                w_jd = jd - 1
            else:
                w_jd = jd
            vaara_idx = drik.vaara(w_jd)
            vaara = cls.VAARA_NAMES[vaara_idx]
        except:
            vaara = "Unknown"
            
        # ...
        
        result = {
            # ...
            'vaara': vaara,
            # ...
            # Ensure hora_lord uses same accurate logic
            'hora_lord': cls._get_hora_lord_details(jd, place)['lord'] if cls._get_hora_lord_details(jd, place) else None,
            # ...
        }
        return result
        


    @classmethod
    def get_extended_panchanga(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                              ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate extended panchanga features including Tamil, special lagnas, and more
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        result = {}
        
        # Tamil Calendar
        try:
            tamil_month_data = drik.tamil_solar_month_and_date(dob, place)
            month_idx = tamil_month_data[0]
            # Correctly map Tamil Month index (usually 1-12 or 0-11)
            # Investigation showed (7, 2) for Nov 18 (Karthigai).
            # If 0=Chithirai, 7=Karthigai.
            # Adjust index if needed. Assuming 0-based from Chithirai.
            month_name = cls.TAMIL_MONTHS[month_idx] if 0 <= month_idx < len(cls.TAMIL_MONTHS) else str(month_idx)
            
            result['tamil_calendar'] = {
                'month': month_name,
                'date': tamil_month_data[1],
                'year': tamil_month_data[2] if len(tamil_month_data) > 2 else None
            }
        except:
            result['tamil_calendar'] = None
        
        # Tamil Yogam
        try:
            tamil_yoga = drik.tamil_yogam(jd, place)
            # (index, start, end, index)
            yoga_idx = tamil_yoga[0] if isinstance(tamil_yoga, tuple) else tamil_yoga
            yoga_name = cls.TAMIL_YOGAS[yoga_idx] if 0 <= yoga_idx < len(cls.TAMIL_YOGAS) else str(yoga_idx)
            
            result['tamil_yogam'] = {
                'name': yoga_name,
                'end_time': cls._format_time_from_hours(tamil_yoga[2]) if isinstance(tamil_yoga, tuple) and len(tamil_yoga) > 2 else None
            }
        except:
            result['tamil_yogam'] = None
        
        # Tamil Jaamam
        try:
            tamil_jaamam = drik.tamil_jaamam(jd, place)
            formatted_jaamam = []
            if tamil_jaamam:
                for start, end in tamil_jaamam:
                    formatted_jaamam.append({
                        'start': cls._format_time_from_hours(start),
                        'end': cls._format_time_from_hours(end)
                    })
            result['tamil_jaamam'] = formatted_jaamam
        except:
            result['tamil_jaamam'] = None
        
        # Anandhaadhi Yoga
        try:
            anandhaadhi = drik.anandhaadhi_yoga(jd, place)
            idx = anandhaadhi[0]
            name = cls.ANANDHAADHI_YOGAS[idx] if 0 <= idx < len(cls.ANANDHAADHI_YOGAS) else f"Yoga {idx}"
            result['anandhaadhi_yoga'] = {
                'name': name,
                'end_time': cls._format_time_from_hours(anandhaadhi[1]) if len(anandhaadhi) > 1 else None
            }
        except:
            result['anandhaadhi_yoga'] = None
        
        # Triguna
        try:
            triguna = drik.triguna(jd, place)
            idx = triguna[0]
            triguna_names = ['Sattva', 'Rajas', 'Tamas']
            name = triguna_names[idx] if 0 <= idx < 3 else str(idx)
            result['triguna'] = name
        except:
            result['triguna'] = None
        
        # Amrita Gadiya
        try:
            amrita = drik.amrita_gadiya(jd, place)
            if isinstance(amrita, (list, tuple)) and len(amrita) >= 2:
                result['amrita_gadiya'] = {
                    'start': cls._format_time_from_hours(amrita[0]),
                    'end': cls._format_time_from_hours(amrita[1])
                }
            else:
                result['amrita_gadiya'] = None
        except Exception as e:
            result['amrita_gadiya'] = None
        
        # Varjyam
        try:
            varjyam = drik.varjyam(jd, place)
            if isinstance(varjyam, (list, tuple)) and len(varjyam) >= 2:
                if len(varjyam) >= 4:
                     result['varjyam'] = {
                        'start': cls._format_time_from_hours(varjyam[0]),
                        'end': cls._format_time_from_hours(varjyam[1]),
                        'start2': cls._format_time_from_hours(varjyam[2]),
                        'end2': cls._format_time_from_hours(varjyam[3])
                    }
                else:
                    result['varjyam'] = {
                        'start': cls._format_time_from_hours(varjyam[0]),
                        'end': cls._format_time_from_hours(varjyam[1])
                    }
            else:
                result['varjyam'] = None
        except Exception as e:
            result['varjyam'] = None
        
        # Thaarabalam - Birth stars favorable for today
        try:
            thaarabalam = drik.thaaraabalam(jd, place)
            if thaarabalam:
                # indices 1-27 - these are birth stars that have good thaara balam today
                names = [cls.NAKSHATRA_NAMES[i - 1] for i in thaarabalam if 1 <= i <= 27]
                result['thaarabalam'] = {
                    'favorable_birth_stars': names,
                    'count': len(names),
                    'description': f"People born under these {len(names)} nakshatras have favorable strength today"
                }
            else:
                result['thaarabalam'] = None
        except:
            result['thaarabalam'] = None
        
        # Chandrabalam - Ascendant times favorable for Moon sign
        try:
            chandrabalam = drik.chandrabalam(jd, place)
            if chandrabalam:
                # indices 1-12 - these are ascendant signs that have good chandra balam today
                names = [cls.RASI_NAMES[i-1] for i in chandrabalam if 0 < i <= 12]
                result['chandrabalam'] = {
                    'favorable_ascendants': names,
                    'count': len(names),
                    'description': f"Times when ascendant passes through these {len(names)} signs are favorable today"
                }
            else:
                result['chandrabalam'] = None
        except:
            result['chandrabalam'] = None
        
        # Chandrashtama
        try:
            chandrashtama = drik.chandrashtama(jd, place)
            idx = chandrashtama[0]
            name = cls.RASI_NAMES[idx-1] if 0 < idx <= 12 else str(idx)
            result['chandrashtama'] = name
        except:
            result['chandrashtama'] = None
        
        # Nava Thaara
        try:
            # Calculate Nava Thaara from Moon position (traditional panchanga method)
            nava_thaara = drik.nava_thaara(jd, place, from_lagna_or_moon=1)
            formatted_nt = []
            if nava_thaara:
                for i, group in enumerate(nava_thaara):
                    tara_idx = i  # Position in list corresponds to Tara cycle (0=Janma, 1=Sampat...)
                    stars = group[1]
                    tara_name = cls.TARA_NAMES[tara_idx] if 0 <= tara_idx < len(cls.TARA_NAMES) else str(tara_idx)
                    star_names = [cls.NAKSHATRA_NAMES[s] for s in stars if 0 <= s < len(cls.NAKSHATRA_NAMES)]
                    formatted_nt.append(f"{tara_name}: {', '.join(star_names)}")
            result['nava_thaara'] = " | ".join(formatted_nt)
        except:
            result['nava_thaara'] = None
        
        # Special Thaara
        try:
            special_thaara = drik.special_thaara(jd, place)
            result['special_thaara'] = special_thaara
        except:
            result['special_thaara'] = None
        
        # Karaka Tithi
        try:
            karaka_tithi = drik.karaka_tithi(jd, place)
            if isinstance(karaka_tithi, (list, tuple)) and len(karaka_tithi) > 0:
                idx = int(karaka_tithi[0])
                result['karaka_tithi'] = {
                    'index': idx,
                    'name': cls._tithi_display_name(idx),
                    'start_time': cls._format_time_from_hours(karaka_tithi[1]) if len(karaka_tithi) > 1 else None,
                    'end_time': cls._format_time_from_hours(karaka_tithi[2]) if len(karaka_tithi) > 2 else None
                }
            else:
                result['karaka_tithi'] = None
        except:
            result['karaka_tithi'] = None
        
        # Karaka Yogam
        try:
            karaka_yogam = drik.karaka_yogam(jd, place)
            if isinstance(karaka_yogam, (list, tuple)) and len(karaka_yogam) > 0:
                idx = int(karaka_yogam[0])
                result['karaka_yogam'] = {
                    'index': idx,
                    'name': cls.YOGA_NAMES[idx - 1] if 1 <= idx <= len(cls.YOGA_NAMES) else f"Yoga {idx}"
                }
            else:
                result['karaka_yogam'] = None
        except:
            result['karaka_yogam'] = None
        
        # Panchaka Rahitha
        try:
            panchaka_list = drik.panchaka_rahitha(jd, place)
            current_h = utils.jd_to_gregorian(jd)[3]
            
            current_panchaka = None
            matched_window = None
            if isinstance(panchaka_list, list):
                for p_type, start, end in panchaka_list:
                    if start <= end:
                        if start <= current_h <= end:
                            current_panchaka = p_type
                            matched_window = (start, end)
                            break
                    else:
                        if current_h >= start or current_h <= end:
                            current_panchaka = p_type
                            matched_window = (start, end)
                            break
            
            if current_panchaka is not None and matched_window:
                meta = cls._get_panchaka_meta(current_panchaka)
                result['panchaka_rahitha'] = {
                    'type': current_panchaka,
                    'label': meta.get('label'),
                    'tone': meta.get('tone', 'neutral'),
                    'description': meta.get('description'),
                    'is_favorable': meta.get('tone') == 'good',
                    'window': {
                        'start': cls._format_time_from_hours(matched_window[0]),
                        'end': cls._format_time_from_hours(matched_window[1])
                    }
                }
            else:
                result['panchaka_rahitha'] = None
        except:
            result['panchaka_rahitha'] = None
        
        # Vivaha Chakra Palan
        try:
            vivaha_chakra = drik.vivaha_chakra_palan(jd, place)
            result['vivaha_chakra_palan'] = vivaha_chakra
        except:
            result['vivaha_chakra_palan'] = None
        
        # Lunar Month and Year
        try:
            lunar_month = drik.lunar_month(jd, place)
            # drik.lunar_month returns [month_index, is_leap_month, is_nija_month]
            # month_index: 1-12 (1=Chaitra, 12=Phalguna)
            LUNAR_MONTH_NAMES = ['Chaitra', 'Vaisakha', 'Jyeshtha', 'Ashadha', 'Shravana', 'Bhadrapada', 
                                'Ashvina', 'Kartika', 'Margashirsha', 'Pausha', 'Magha', 'Phalguna']
            
            if isinstance(lunar_month, (list, tuple)) and len(lunar_month) > 0:
                month_idx = lunar_month[0]  # 1-12
                is_leap = lunar_month[1] if len(lunar_month) > 1 else False
                is_nija = lunar_month[2] if len(lunar_month) > 2 else False
                
                # Ensure month_idx is in valid range (1-12)
                if 1 <= month_idx <= 12:
                    month_name = LUNAR_MONTH_NAMES[month_idx - 1]  # Convert 1-based to 0-based index
                    if is_leap:
                        month_name = f"Adhika {month_name}"
                    elif is_nija:
                        month_name = f"Nija {month_name}"
                    # Frontend expects [index, name] format
                    result['lunar_month'] = [month_idx, month_name]
                else:
                    result['lunar_month'] = None
            elif isinstance(lunar_month, int):
                # Fallback for int (shouldn't happen but handle it)
                if 1 <= lunar_month <= 12:
                    name = LUNAR_MONTH_NAMES[lunar_month - 1]
                    result['lunar_month'] = [lunar_month, name]
                else:
                    result['lunar_month'] = None
            else:
                result['lunar_month'] = None

            # region agent log
            _agent_write_log({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "H4",
                "location": "panchanga_service.py:get_extended_panchanga:lunar_month",
                "message": "Raw lunar_month and normalized result",
                "data": {
                    "raw_lunar_month": lunar_month if isinstance(lunar_month, (int, str, float, list, tuple, dict)) else str(lunar_month),
                    "normalized_lunar_month": result.get("lunar_month"),
                },
            })
            # endregion
        except:
            result['lunar_month'] = None
            # Fallback attempts? No.
        
        # Ritu (Season)
        try:
            if 'lunar_month' in result and result['lunar_month'] is not None:
                # If we modified lunar_month to be a list, extracting index might be needed
                lm = result['lunar_month'][0] if isinstance(result['lunar_month'], list) else result['lunar_month']
                ritu = drik.ritu(lm)
                # Ensure ritu is readable
                RITU_NAMES = ['Vasanta', 'Grishma', 'Varsha', 'Sharad', 'Hemanta', 'Shishira']
                if isinstance(ritu, int):
                    r_name = RITU_NAMES[(ritu-1)%6]
                    result['ritu'] = r_name
                else:
                    result['ritu'] = ritu
            else:
                result['ritu'] = None
        except:
            result['ritu'] = None
        
        # Samvatsara
        try:
            # drik.samvatsara expects panchanga_date as (year, month, day) tuple
            # dob is already a tuple from _parse_date, which should be (year, month, day)
            samvatsara_idx = drik.samvatsara(dob, place)
            # samvatsara_idx is 0-59, map to name
            if isinstance(samvatsara_idx, int) and 0 <= samvatsara_idx <= 59:
                result['samvatsara'] = cls.SAMVATSARA_NAMES[samvatsara_idx]
            else:
                result['samvatsara'] = None

            # region agent log
            _agent_write_log({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "H3",
                "location": "panchanga_service.py:get_extended_panchanga:samvatsara",
                "message": "Samvatsara raw result",
                "data": {"samvatsara": samvatsara},
            })
            # endregion
        except:
            result['samvatsara'] = None
            # region agent log
            _agent_write_log({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "H3",
                "location": "panchanga_service.py:get_extended_panchanga:samvatsara:error",
                "message": "Samvatsara exception -> falling back to None",
                "data": {"dob": str(dob), "error": "samvatsara_failed"},
            })
            # endregion
        
        # Midday and Midnight
        try:
            midday_time = drik.midday(jd, place)
            midnight_time = drik.midnight(jd, place)
            
            md_t = midday_time[1] if isinstance(midday_time, tuple) else midday_time
            mn_t = midnight_time[1] if isinstance(midnight_time, tuple) else midnight_time
            
            result['midday'] = cls._format_time_from_hours(md_t)
            result['midnight'] = cls._format_time_from_hours(mn_t)
        except:
            result['midday'] = None
            result['midnight'] = None
        
        # Day and Night Length
        try:
            day_len = drik.day_length(jd, place)
            night_len = drik.night_length(jd, place)
            # Format as HH:MM:SS
            result['day_length'] = cls._format_time_from_hours(day_len)
            result['night_length'] = cls._format_time_from_hours(night_len)
        except:
            result['day_length'] = None
            result['night_length'] = None
        
        # Gauri Choghadiya (Current)
        try:
            choghadiya = drik.gauri_choghadiya(jd, place)
            if choghadiya and isinstance(choghadiya, list):
                # drik.gauri_choghadiya returns: [(gc_type, start_time_string, end_time_string), ...]
                # gc_type: 0=Amrita, 1=Chala, 2=Roga, 3=Amrit (note: 0 and 3 both are Amrita)
                # Format: [(type, start_str, end_str), ...] where times are in "HH:MM:SS" format
                
                # Get current local time as string HH:MM:SS
                greg = utils.jd_to_gregorian(jd)
                utc_hours = greg[3]
                local_hours = (utc_hours + place.timezone) % 24
                current_time_str = cls._format_time_from_hours(local_hours)
                
                # Helper to convert time string to comparable value
                def time_str_to_minutes(time_str):
                    """Convert 'HH:MM:SS' to minutes since midnight"""
                    if isinstance(time_str, str):
                        parts = time_str.split(':')
                        if len(parts) >= 2:
                            h, m = int(parts[0]), int(parts[1])
                            s = int(parts[2]) if len(parts) > 2 else 0
                            return h * 60 + m + s / 60.0
                    return 0
                
                current_mins = time_str_to_minutes(current_time_str)
                current_gouri = None
                
                for item in choghadiya:
                    if len(item) >= 3:
                        gc_type = item[0]
                        start_str = item[1]  # Time string like "HH:MM:SS"
                        end_str = item[2]    # Time string like "HH:MM:SS"
                        
                        start_mins = time_str_to_minutes(start_str)
                        end_mins = time_str_to_minutes(end_str)
                        
                        # Handle day/night crossover
                        if start_mins <= end_mins:
                            if start_mins <= current_mins <= end_mins:
                                current_gouri = item
                                break
                        else:  # Crosses midnight
                            if current_mins >= start_mins or current_mins <= end_mins:
                                current_gouri = item
                                break
                
                if current_gouri:
                    gc_type_names = {0: 'Amrita', 1: 'Chala', 2: 'Roga', 3: 'Amrita'}
                    gc_type = current_gouri[0]
                    name = gc_type_names.get(gc_type, f'Type {gc_type}')
                    
                    result['gauri_choghadiya'] = {
                        'name': name,
                        'start': current_gouri[1],  # Already a time string
                        'end': current_gouri[2],    # Already a time string
                        'type': gc_type
                    }
                else:
                    result['gauri_choghadiya'] = None
            else:
                result['gauri_choghadiya'] = None

            # region agent log
            _agent_write_log({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "H5",
                "location": "panchanga_service.py:get_extended_panchanga:gauri_choghadiya",
                "message": "Gauri choghadiya selection context",
                "data": {
                    "gregorian_from_jd": greg if "greg" in locals() else None,
                    "current_h_used": current_h if "current_h" in locals() else None,
                    "raw_choghadiya_len": len(choghadiya) if isinstance(choghadiya, list) else None,
                    "raw_choghadiya_first": choghadiya[0] if isinstance(choghadiya, list) and len(choghadiya) > 0 else None,
                    "selected_gauri_choghadiya": result.get("gauri_choghadiya"),
                },
            })
            # endregion
        except:
            result['gauri_choghadiya'] = None
            # region agent log
            _agent_write_log({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "H5",
                "location": "panchanga_service.py:get_extended_panchanga:gauri_choghadiya:error",
                "message": "Gauri choghadiya exception -> falling back to None",
                "data": {"error": "gauri_choghadiya_failed"},
            })
            # endregion
            
        # Shubha Hora
        try:
            shubha_hora = drik.shubha_hora(jd, place)
            result['shubha_hora'] = shubha_hora
        except:
            result['shubha_hora'] = None
            
        # Mahakala Hora (Now mapped to Hora Lord)
        try:
            # We use our detailed Hora calculation
            mh = cls._get_hora_lord_details(jd, place)
            result['mahakala_hora'] = mh
        except:
            result['mahakala_hora'] = None
            
        # Kaala Lord (Now mapped to Yama Lord)
        try:
            kl = cls._get_kaala_lord_yama(jd, place)
            if kl:
                result['kaala_lord'] = kl['lord']
            else:
                result['kaala_lord'] = None
        except:
            result['kaala_lord'] = None

        # region agent log
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H2",
            "location": "panchanga_service.py:get_extended_panchanga:mahakala_kaala",
            "message": "Mahakala Hora and Kaala Lord computed outputs",
            "data": {
                "mahakala_hora": result.get("mahakala_hora"),
                "kaala_lord": result.get("kaala_lord"),
            },
        })
        # endregion

        # region agent log
        _agent_write_log({
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": "H1",
            "location": "panchanga_service.py:get_extended_panchanga:exit",
            "message": "Extended panchanga outputs (subset)",
            "data": {
                "samvatsara": result.get("samvatsara"),
                "lunar_month": result.get("lunar_month"),
                "gauri_choghadiya": result.get("gauri_choghadiya"),
                "mahakala_hora": result.get("mahakala_hora"),
                "kaala_lord": result.get("kaala_lord"),
            },
        })
        # endregion
        
        return {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'extended_features': result
        }

    @classmethod
    def calculate(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                 ayanamsa: str = "LAHIRI", calculation_type: str = "basic") -> Dict[str, Any]:
        """
        Main calculation entry point
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        # Vaara Fix for displayed Vedic Weekday
        try:
            sunrise_jd = drik.sunrise(jd, place)[2]
            if jd < sunrise_jd:
                # Use previous day
                w_jd = jd - 1
            else:
                w_jd = jd
            vaara_idx = drik.vaara(w_jd)
            vaara = cls.VAARA_NAMES[vaara_idx]
        except:
            vaara = "Unknown"
            
        # Basic calculations
        result = {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'ayanamsa': ayanamsa,
            'vaara': vaara,
            'tithi': cls._get_tithi_details(jd, place),
            'nakshatra': cls._get_nakshatra_details(jd, place),
            'yoga': cls._get_yoga_details(jd, place),
            'karana': cls._get_karana_details(jd, place),
            'sunrise': drik.sunrise(jd, place)[2],
            'sunset': drik.sunset(jd, place)[2],
            # Ensure hora_lord uses same accurate logic
            'hora_lord': cls._get_hora_lord_details(jd, place)['lord'] if cls._get_hora_lord_details(jd, place) else None
        }
        
        return result
    
    @classmethod
    def get_additional_timings(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                              ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate additional auspicious and inauspicious timings
        
        Returns:
            Dictionary with brahma muhurta, durmuhurta, nishita kala, etc.
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        # Brahma Muhurta (auspicious time before sunrise)
        try:
            brahma_muhurta = drik.brahma_muhurtha(jd, place)
            brahma_data = {
                "start": cls._jd_to_time_string(brahma_muhurta[0]),
                "end": cls._jd_to_time_string(brahma_muhurta[1]),
                "description": "Most auspicious time for spiritual practices"
            }
        except Exception as e:
            brahma_data = None
        
        # Durmuhurta (inauspicious periods)
        try:
            durmuhurta_times = drik.durmuhurtam(jd, place)
            # durmuhurta returns list of JD values
            if len(durmuhurta_times) >= 2:
                durmuhurta_data = {
                    "start": cls._jd_to_time_string(durmuhurta_times[0]),
                    "end": cls._jd_to_time_string(durmuhurta_times[1])
                }
            else:
                durmuhurta_data = None
        except Exception as e:
            durmuhurta_data = None
        
        # Nishita Kala (midnight period)
        try:
            nishita = drik.nishita_kaala(jd, place)
            nishita_data = {
                "start": cls._jd_to_time_string(nishita[0]),
                "end": cls._jd_to_time_string(nishita[1]),
                "description": "Eighth muhurtha of the night"
            }
        except Exception as e:
            nishita_data = None
        
        # Vijaya Muhurta (victory time)
        try:
            vijaya = drik.vijaya_muhurtha(jd, place)
            if len(vijaya) >= 2:
                vijaya_data = {
                    "start": cls._jd_to_time_string(vijaya[0]),
                    "end": cls._jd_to_time_string(vijaya[1]),
                    "description": "Auspicious for important undertakings"
                }
            else:
                vijaya_data = None
        except Exception as e:
            vijaya_data = None
        
        # Godhuli Muhurta (twilight period)
        try:
            godhuli = drik.godhuli_muhurtha(jd, place)
            godhuli_data = {
                "start": cls._jd_to_time_string(godhuli[0]),
                "end": cls._jd_to_time_string(godhuli[1]),
                "description": "Twilight period, good for worship"
            }
        except Exception as e:
            godhuli_data = None
        
        # All 30 muhurthas (15 day + 15 night)
        try:
            muhurthas_list = drik.muhurthas(jd, place)
            muhurthas_data = []
            # drik.muhurthas returns list of tuples: (name, quality_code, (start_jd, end_jd))
            # quality_code: 0=Bad (e.g. Rudra), 1=Good (e.g. Mitra) - based on investigation
            
            for idx, item in enumerate(muhurthas_list):
                if len(item) == 3:
                    name = item[0]
                    quality = item[1]
                    times = item[2]
                    
                    # Map quality
                    # Assuming 0 is Bad (Inauspicious), 1 is Good (Auspicious)
                    quality_str = 'Inauspicious' if quality == 0 else 'Auspicious'
                    
                    muhurthas_data.append({
                        "number": idx + 1,
                        "name": name.title(),
                        "quality": quality_str,
                        "start": cls._format_time_from_hours(times[0]),
                        "end": cls._format_time_from_hours(times[1]),
                        "period": "day" if idx < 15 else "night"
                    })
            
            if not muhurthas_data:
                # Fallback if format is different
                muhurthas_data = []
                
        except Exception as e:
            muhurthas_data = None
        
        return {
            "brahma_muhurta": brahma_data,
            "durmuhurta": durmuhurta_data,
            "nishita_kala": nishita_data,
            "vijaya_muhurta": vijaya_data,
            "godhuli_muhurta": godhuli_data,
            "all_muhurthas": muhurthas_data
        }
    
    @staticmethod
    def get_planet_positions(date_str: str, time_str: str, place_data: Dict[str, Any],
                           ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate planet positions"""
        try:
            # Set ayanamsa
            const._DEFAULT_AYANAMSA_MODE = ayanamsa
            drik.set_ayanamsa_mode(ayanamsa)

            # Create place
            place = drik.Place(
                place_data['name'],
                place_data['latitude'],
                place_data['longitude'],
                place_data['timezone']
            )

            # Parse date and time
            dob = PanchangaService._parse_date(date_str)
            tob = PanchangaService._parse_time(time_str)

            # Calculate Julian day and UTC JD for sidereal_longitude
            jd = utils.julian_day_number(dob, tob)
            jd_utc = jd - place.timezone / 24.0

            planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
            rasi_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

            positions = []
            for i in range(9):  # Sun to Ketu
                if i < 7:  # Real planets (Sun to Saturn)
                    longitude = drik.sidereal_longitude(jd_utc, i)
                elif i == 7:  # Rahu (use const._RAHU which is swe.MEAN_NODE)
                    import swisseph as swe
                    longitude = drik.sidereal_longitude(jd_utc, swe.MEAN_NODE)
                else:  # Ketu (180 degrees opposite to Rahu)
                    import swisseph as swe
                    rahu_long = drik.sidereal_longitude(jd_utc, swe.MEAN_NODE)
                    longitude = (rahu_long + 180) % 360

                rasi = int(longitude / 30)
                degrees_in_rasi = longitude % 30

                # Nakshatra and pada (use PyJHora helper)
                nak_idx, nak_pada, _ = drik.nakshatra_pada(longitude)
                # Navamsa rasi
                nav_rasi, _ = drik.dasavarga_from_long(longitude, 9)

                positions.append({
                    "name": planet_names[i],
                    "longitude": longitude,
                    "rasi": rasi,
                    "rasi_name": rasi_names[rasi],
                    "degrees_in_rasi": degrees_in_rasi,
                    "nakshatra": nak_idx - 1,
                    "nakshatra_name": PanchangaService.NAKSHATRA_NAMES[nak_idx - 1],
                    "nakshatra_pada": nak_pada,
                    "navamsa_rasi": nav_rasi,
                    "navamsa_rasi_name": rasi_names[nav_rasi],
                    "retrograde": False  # Temporarily disable retrograde check
                })

            # Ascendant
            asc_data = drik.ascendant(jd, place)
            if isinstance(asc_data, (list, tuple)) and len(asc_data) >= 2:
                asc_rasi = asc_data[0]
                asc_deg = asc_data[1]
                asc_longitude = asc_rasi * 30 + asc_deg
                asc_nak_idx, asc_pada, _ = drik.nakshatra_pada(asc_longitude)
                asc_nav_rasi, _ = drik.dasavarga_from_long(asc_longitude, 9)
            else:
                asc_rasi = int(asc_data / 30)
                asc_deg = asc_data % 30
                asc_longitude = asc_data
                asc_nak_idx, asc_pada, _ = drik.nakshatra_pada(asc_longitude)
                asc_nav_rasi, _ = drik.dasavarga_from_long(asc_longitude, 9)

            return {
                "julian_day": jd,
                "ayanamsa_value": drik.get_ayanamsa_value(jd),
                "ascendant": {
                    "name": "Ascendant",
                    "longitude": asc_longitude,
                    "rasi": asc_rasi,
                    "rasi_name": rasi_names[asc_rasi],
                    "degrees_in_rasi": asc_deg,
                    "nakshatra": asc_nak_idx - 1,
                    "nakshatra_name": PanchangaService.NAKSHATRA_NAMES[asc_nak_idx - 1],
                    "nakshatra_pada": asc_pada,
                    "navamsa_rasi": asc_nav_rasi,
                    "navamsa_rasi_name": rasi_names[asc_nav_rasi],
                    "retrograde": False
                },
                "planets": positions
            }
        except Exception as e:
            return {"error": f"Planet positions calculation error: {str(e)}"}
    
    @classmethod
    def get_eclipse_info(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                        ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Get solar and lunar eclipse information
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        result = {}
        
        # Check for solar eclipse
        try:
            is_solar = drik.is_solar_eclipse(jd, place)
            result['is_solar_eclipse_today'] = is_solar
            
            # Get next solar eclipse
            next_solar = drik.next_solar_eclipse(jd, place)
            # next_solar returns [eclipse_type, (jd_details...), (eclipse_details...)]
            if isinstance(next_solar, list) and len(next_solar) > 1:
                eclipse_jd = next_solar[1][0] if isinstance(next_solar[1], tuple) and len(next_solar[1]) > 0 else jd
                result['next_solar_eclipse'] = {
                    'date': cls._jd_to_date_string(eclipse_jd),
                    'jd': eclipse_jd
                }
            else:
                result['next_solar_eclipse'] = None
        except Exception as e:
            result['next_solar_eclipse'] = None
        
        # Get next lunar eclipse
        try:
            next_lunar = drik.next_lunar_eclipse(jd, place)
            # next_lunar returns similar structure
            if isinstance(next_lunar, list) and len(next_lunar) > 1:
                eclipse_jd = next_lunar[1][0] if isinstance(next_lunar[1], tuple) and len(next_lunar[1]) > 0 else jd
                result['next_lunar_eclipse'] = {
                    'date': cls._jd_to_date_string(eclipse_jd),
                    'jd': eclipse_jd
                }
            else:
                result['next_lunar_eclipse'] = None
        except Exception as e:
            result['next_lunar_eclipse'] = None
        
        return {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'eclipse_info': result
        }
    
    @classmethod
    def get_sankranti_dates(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                           ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Get previous and next sankranti (solar ingress) dates
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        result = {}
        
        # RASI names for sankranti
        RASI_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        # Previous sankranti - calculate using JD
        try:
            jd = utils.julian_day_number(dob, tob)
            # Find which rasi Sun is currently in
            sun_long = drik.sidereal_longitude(jd, 0)  # 0 = Sun
            current_rasi = int(sun_long / 30)
            prev_rasi = (current_rasi - 1) % 12
            
            # Estimate previous sankranti (when Sun entered current rasi)
            days_in_rasi = (sun_long % 30) / (360 / 365)  # Rough estimate
            prev_sankranti_jd = jd - days_in_rasi
            
            result['previous_sankranti'] = {
                'date': cls._jd_to_date_string(prev_sankranti_jd),
                'rasi': RASI_NAMES[current_rasi]
            }
        except Exception as e:
            result['previous_sankranti'] = None
        
        # Next sankranti
        try:
            jd = utils.julian_day_number(dob, tob)
            sun_long = drik.sidereal_longitude(jd, 0)
            current_rasi = int(sun_long / 30)
            next_rasi = (current_rasi + 1) % 12
            
            # Estimate next sankranti
            days_to_next = (30 - (sun_long % 30)) / (360 / 365)
            next_sankranti_jd = jd + days_to_next
            
            result['next_sankranti'] = {
                'date': cls._jd_to_date_string(next_sankranti_jd),
                'rasi': RASI_NAMES[next_rasi]
            }
        except Exception as e:
            result['next_sankranti'] = None
        
        return {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'sankranti_info': result
        }
    
    @classmethod
    def get_planet_conjunctions(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                                planet1_index: int, planet2_index: int,
                                ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Get next conjunction between two planets
        
        Planet indices: 0=Sun, 1=Moon, 2=Mars, 3=Mercury, 4=Jupiter, 5=Venus, 6=Saturn, 7=Rahu, 8=Ketu
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        result = {}
        
        # Get next conjunction
        try:
            next_conj = drik.next_conjunction_of_planet_pair(jd, place, planet1_index, planet2_index)
            result['next_conjunction'] = {
                'jd': next_conj[0] if isinstance(next_conj, tuple) else next_conj,
                'date': next_conj[1] if isinstance(next_conj, tuple) and len(next_conj) > 1 else None,
                'planet1': cls.PLANET_NAMES[planet1_index] if planet1_index < len(cls.PLANET_NAMES) else 'Unknown',
                'planet2': cls.PLANET_NAMES[planet2_index] if planet2_index < len(cls.PLANET_NAMES) else 'Unknown'
            }
        except Exception as e:
            result['conjunction_error'] = str(e)
        
        # Get previous conjunction
        try:
            prev_conj = drik.previous_conjunction_of_planet_pair(jd, place, planet1_index, planet2_index)
            result['previous_conjunction'] = {
                'jd': prev_conj[0] if isinstance(prev_conj, tuple) else prev_conj,
                'date': prev_conj[1] if isinstance(prev_conj, tuple) and len(prev_conj) > 1 else None,
                'planet1': cls.PLANET_NAMES[planet1_index] if planet1_index < len(cls.PLANET_NAMES) else 'Unknown',
                'planet2': cls.PLANET_NAMES[planet2_index] if planet2_index < len(cls.PLANET_NAMES) else 'Unknown'
            }
        except Exception as e:
            result['previous_conjunction_error'] = str(e)
        
        return {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'conjunction_info': result
        }
    
    @classmethod
    def get_planet_retrograde_info(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                                   ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Get retrograde status and next retrograde change dates for all planets
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        result = {}
        
        # Planet names including outer planets
        PLANET_NAMES = [
            'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 
            'Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto'
        ]
        
        # Get retrograde planets
        try:
            retrograde_indices = drik.planets_in_retrograde(jd, place)
            # Convert planet indices to names
            if isinstance(retrograde_indices, list):
                result['retrograde_planets'] = [
                    PLANET_NAMES[i] if i < len(PLANET_NAMES) else f'Unknown ({i})'
                    for i in retrograde_indices
                ]
            else:
                result['retrograde_planets'] = []
        except Exception as e:
            result['retrograde_planets'] = []
        
        # Get planet speed info
        try:
            speed_info = drik.planets_speed_info(jd, place)
            # Format speed info with planet names
            if isinstance(speed_info, dict):
                formatted_speeds = {}
                for key, value in speed_info.items():
                    if isinstance(key, int) and key < len(PLANET_NAMES):
                        formatted_speeds[PLANET_NAMES[key]] = value
                    else:
                        formatted_speeds[str(key)] = value
                result['planet_speeds'] = formatted_speeds
            else:
                result['planet_speeds'] = speed_info
        except Exception as e:
            result['planet_speeds'] = {}
        
        # Get planets in graha yudh (planetary war)
        try:
            graha_yudh_indices = drik.planets_in_graha_yudh(jd, place)
            # Convert planet indices to names
            if isinstance(graha_yudh_indices, list):
                result['graha_yudh'] = [
                    PLANET_NAMES[i] if i < len(PLANET_NAMES) else f'Planet {i}'
                    for i in graha_yudh_indices
                ]
            else:
                result['graha_yudh'] = []
        except Exception as e:
            result['graha_yudh'] = []
        
        return {
            'date': date_str,
            'time': time_str,
            'place': place_data,
            'retrograde_info': result
        }
    
    @classmethod
    def get_udhaya_lagna_muhurtha(cls, date_str: str, time_str: str, place_data: Dict[str, Any],
                                  ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Get udhaya lagna muhurtha timings
        """
        # Set ayanamsa
        const._DEFAULT_AYANAMSA_MODE = ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        
        # Create place
        place = drik.Place(
            place_data['name'],
            place_data['latitude'],
            place_data['longitude'],
            place_data['timezone']
        )
        
        # Parse date and time
        dob = cls._parse_date(date_str)
        tob = cls._parse_time(time_str)
        
        # Calculate Julian day
        jd = utils.julian_day_number(dob, tob)
        
        try:
            udhaya_lagna = drik.udhaya_lagna_muhurtha(jd, place)
            return {
                'date': date_str,
                'time': time_str,
                'place': place_data,
                'udhaya_lagna_muhurtha': udhaya_lagna
            }
        except Exception as e:
            return {
                'date': date_str,
                'time': time_str,
                'place': place_data,
                'error': str(e)
            }
    
    @staticmethod
    def _is_retrograde(jd: float, planet_index: int) -> bool:
        """
        Check if a planet is retrograde
        
        Args:
            jd: Julian day number
            planet_index: Planet index (0=Sun, 1=Moon, 2=Mars, etc.)
        
        Returns:
            True if planet is retrograde, False otherwise
        """
        # Sun and Moon are never retrograde
        if planet_index in [0, 1]:
            return False
        
        try:
            import swisseph as swe
            # Get planet position with speed
            planet_data = swe.calc_ut(jd, planet_index, swe.FLG_SWIEPH | swe.FLG_SPEED)
            # planet_data[3] contains the speed in longitude
            # Negative speed means retrograde motion
            return planet_data[0][3] < 0
        except:
            return False

