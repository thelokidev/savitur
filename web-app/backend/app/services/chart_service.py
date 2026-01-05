"""
Chart calculation service
Handles all divisional charts, special lagnas, upagrahas, and arudhas
"""
import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora.horoscope.chart import charts, house, arudhas
from jhora import utils, const
import swisseph as swe
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime


class ChartService:
    """Service for all chart calculations"""
    
    PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    RASI_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 
                  'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    NAKSHATRA_NAMES = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    # Divisional chart names and their factors
    DIVISIONAL_CHARTS = {
        1: "Rasi (D-1)",
        2: "Hora (D-2)",
        3: "Drekkana (D-3)",
        4: "Chaturthamsa (D-4)",
        5: "Panchamsa (D-5)",
        6: "Shashthamsa (D-6)",
        7: "Saptamsa (D-7)",
        8: "Ashtamsa (D-8)",
        9: "Navamsa (D-9)",
        10: "Dasamsa (D-10)",
        11: "Rudramsa (D-11)",
        12: "Dwadasamsa (D-12)",
        16: "Shodasamsa (D-16)",
        20: "Vimsamsa (D-20)",
        24: "Chaturvimsamsa (D-24)",
        27: "Nakshatramsa (D-27)",
        30: "Trimsamsa (D-30)",
        40: "Khavedamsa (D-40)",
        45: "Akshavedamsa (D-45)",
        60: "Shashtyamsa (D-60)",
        81: "Nava-Navamsa (D-81)",
        108: "Ashtotharamsa (D-108)",
        144: "Dwadas-Dwadasamsa (D-144)",
    }
    
    def __init__(self):
        self.place_cache = {}
    
    def _parse_birth_details(self, birth_details: Dict[str, Any]) -> Tuple[Tuple, Tuple, Any]:
        """Parse birth details into format needed by PyJHora"""
        try:
            # Parse date
            date_str = birth_details['date']
            year, month, day = map(int, date_str.split('-'))
            dob = (year, month, day)
            
            # Parse time
            time_str = birth_details['time']
            hour, minute, second = map(int, time_str.split(':'))
            tob = (hour, minute, second)
            
            # Create place object
            place_info = birth_details['place']
            place = drik.Place(
                place_info['name'],
                place_info['latitude'],
                place_info['longitude'],
                place_info['timezone']
            )
            
            return dob, tob, place
        except Exception as e:
            raise ValueError(f"Error parsing birth details: {str(e)}")
    
    def _set_ayanamsa(self, ayanamsa: str = "LAHIRI"):
        """Set the ayanamsa mode"""
        drik.set_ayanamsa_mode(ayanamsa.upper())
    
    def get_rasi_chart(self, birth_details: Dict[str, Any], ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get Rasi chart (D-1) with all planet positions"""
        print(f"DEBUG: get_rasi_chart called with ayanamsa={ayanamsa}")
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get planet positions for Rasi chart (D-1)
        print(f"DEBUG: Calling charts.divisional_chart with ayanamsa_mode={ayanamsa}")
        planet_positions = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=1)
        
        # Get retrograde planets using drik function (recommended method)
        retrograde_planets = drik.planets_in_retrograde(jd, place)
        
        # Get ascendant (first element of planet_positions)
        asc_house = planet_positions[0][1]  # Format: ['L', (rasi, longitude)]
        
        # Get houses with planets
        houses = self._get_houses_with_planets(planet_positions, asc_house)
        
        # Format planet details (skip first element which is ascendant)
        planet_details = []
        for planet_data in planet_positions[1:10]:  # Elements 1-9 are planets
            planet_id, (rasi, longitude) = planet_data
            is_retrograde = planet_id in retrograde_planets
            abs_longitude = (rasi * 30) + longitude
            nak_idx, nak_pada, _ = drik.nakshatra_pada(abs_longitude)
            nav_rasi, _ = drik.dasavarga_from_long(abs_longitude, 9)
            planet_details.append({
                'name': self.PLANET_NAMES[planet_id],
                'rasi': rasi,
                'rasi_name': self.RASI_NAMES[rasi],
                'longitude': abs_longitude,
                'degrees_in_rasi': longitude,
                'nakshatra': nak_idx - 1,
                'nakshatra_name': self.NAKSHATRA_NAMES[nak_idx - 1],
                'nakshatra_pada': nak_pada,
                'navamsa_rasi': nav_rasi,
                'navamsa_rasi_name': self.RASI_NAMES[nav_rasi],
                'retrograde': is_retrograde
            })
        
        # Get special lagnas and upagrahas
        special_lagnas_data = self._get_special_lagnas_formatted(dob, tob, jd, place)
        upagrahas_data = self._get_upagrahas_formatted(dob, tob, place, ayanamsa)
        
        return {
            'chart_type': 'Rasi (D-1)',
            'divisional_factor': 1,
            'julian_day': jd,
            'ayanamsa': ayanamsa,
            'ascendant': {
                'rasi': asc_house[0],
                'rasi_name': self.RASI_NAMES[asc_house[0]],
                'longitude': (asc_house[0] * 30) + asc_house[1],
                'degrees_in_rasi': asc_house[1],
                'nakshatra': drik.nakshatra_pada((asc_house[0] * 30) + asc_house[1])[0] - 1,
                'nakshatra_name': self.NAKSHATRA_NAMES[drik.nakshatra_pada((asc_house[0] * 30) + asc_house[1])[0] - 1],
                'nakshatra_pada': drik.nakshatra_pada((asc_house[0] * 30) + asc_house[1])[1],
                'navamsa_rasi': drik.dasavarga_from_long((asc_house[0] * 30) + asc_house[1], 9)[0],
                'navamsa_rasi_name': self.RASI_NAMES[drik.dasavarga_from_long((asc_house[0] * 30) + asc_house[1], 9)[0]]
            },
            'planets': planet_details,
            'houses': houses,
            'special_lagnas': special_lagnas_data,
            'upagrahas': upagrahas_data
        }
    
    def get_divisional_chart(self, birth_details: Dict[str, Any], 
                            divisional_factor: int, 
                            ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get any divisional chart (D-n)"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get planet positions for divisional chart
        planet_positions = charts.divisional_chart(
            jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=divisional_factor
        )
        
        # Get ascendant for divisional chart (first element)
        asc_house = planet_positions[0][1]  # Format: ['L', (rasi, longitude)]
        
        # Get houses with planets
        houses = self._get_houses_with_planets(planet_positions, asc_house)
        
        # Format planet details (skip first element which is ascendant)
        planet_details = []
        for i, planet_data in enumerate(planet_positions[1:10]):  # Elements 1-9 are planets
            planet_id, (rasi, longitude) = planet_data  # Unpack: [planet_id, (rasi, longitude)]
            planet_details.append({
                'name': self.PLANET_NAMES[i],
                'rasi': rasi,
                'rasi_name': self.RASI_NAMES[rasi],
                'longitude': longitude,
                'degrees_in_rasi': longitude % 30,
            })
        
        chart_name = self.DIVISIONAL_CHARTS.get(divisional_factor, f"D-{divisional_factor}")
        
        return {
            'chart_type': chart_name,
            'divisional_factor': divisional_factor,
            'julian_day': jd,
            'ayanamsa': ayanamsa,
            'ascendant': {
                'rasi': asc_house[0],
                'rasi_name': self.RASI_NAMES[asc_house[0]],
                'longitude': asc_house[1],
                'degrees_in_rasi': asc_house[1] % 30
            },
            'planets': planet_details,
            'houses': houses
        }
    
    def get_all_divisional_charts(self, birth_details: Dict[str, Any], 
                                  ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get all standard divisional charts"""
        charts_data = {}
        
        for varga, name in self.DIVISIONAL_CHARTS.items():
            try:
                charts_data[f"D{varga}"] = self.get_divisional_chart(
                    birth_details, varga, ayanamsa
                )
            except Exception as e:
                charts_data[f"D{varga}"] = {'error': str(e)}
        
        return charts_data
    
    def get_special_lagnas(self, birth_details: Dict[str, Any], 
                          ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get all special lagnas"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get all special lagnas
        special_lagnas = {}
        
        try:
            # Bhava Lagna
            bhava_lagna = drik.bhava_lagna(jd, place)
            special_lagnas['bhava_lagna'] = self._format_longitude(bhava_lagna)
        except:
            pass
        
        try:
            # Hora Lagna
            hora_lagna = drik.hora_lagna(jd, place)
            special_lagnas['hora_lagna'] = self._format_longitude(hora_lagna)
        except:
            pass
        
        try:
            # Ghati Lagna
            ghati_lagna = drik.ghati_lagna(jd, place)
            special_lagnas['ghati_lagna'] = self._format_longitude(ghati_lagna)
        except:
            pass
        
        try:
            # Vighati Lagna
            vighati_lagna = drik.vighati_lagna(jd, place)
            special_lagnas['vighati_lagna'] = self._format_longitude(vighati_lagna)
        except:
            pass
        
        try:
            # Pranapada Lagna
            pranapada_lagna = drik.pranapada_lagna(jd, place)
            special_lagnas['pranapada_lagna'] = self._format_longitude(pranapada_lagna)
        except:
            pass
        
        try:
            # Indu Lagna
            indu_lagna = drik.indu_lagna(jd, place)
            special_lagnas['indu_lagna'] = self._format_longitude(indu_lagna)
        except:
            pass
        
        try:
            # Sree Lagna
            sree_lagna = drik.sree_lagna(jd, place)
            special_lagnas['sree_lagna'] = self._format_longitude(sree_lagna)
        except:
            pass
        
        return special_lagnas
    
    def get_upagrahas(self, birth_details: Dict[str, Any], 
                     ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get all upagrahas (sub-planets)"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        upagrahas = {}
        
        try:
            # Get all upagrahas
            dhuma = drik.dhuma(jd, place)
            upagrahas['dhuma'] = self._format_longitude(dhuma)
            
            vyatipaata = drik.vyatipaata(jd, place)
            upagrahas['vyatipaata'] = self._format_longitude(vyatipaata)
            
            parivesha = drik.parivesha(jd, place)
            upagrahas['parivesha'] = self._format_longitude(parivesha)
            
            indrachapa = drik.indrachapa(jd, place)
            upagrahas['indrachapa'] = self._format_longitude(indrachapa)
            
            upaketu = drik.upaketu(jd, place)
            upagrahas['upaketu'] = self._format_longitude(upaketu)
            
            kaala = drik.kaala(jd, place)
            upagrahas['kaala'] = self._format_longitude(kaala)
            
            mrityu = drik.mrityu(jd, place)
            upagrahas['mrityu'] = self._format_longitude(mrityu)
            
            artha_praharaka = drik.artha_praharaka(jd, place)
            upagrahas['artha_praharaka'] = self._format_longitude(artha_praharaka)
            
            yama_ghantaka = drik.yama_ghantaka(jd, place)
            upagrahas['yama_ghantaka'] = self._format_longitude(yama_ghantaka)
            
            gulika = drik.gulika(jd, place)
            upagrahas['gulika'] = self._format_longitude(gulika)
            
            maandi = drik.maandi(jd, place)
            upagrahas['maandi'] = self._format_longitude(maandi)
        except Exception as e:
            upagrahas['error'] = str(e)
        
        return upagrahas
    
    def get_arudha_padas(self, birth_details: Dict[str, Any], 
                        ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get all arudha padas"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get planet positions
        planet_positions = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=1)
        
        # Get arudha padas
        try:
            bhava_arudhas = arudhas.bhava_arudhas_from_planet_positions(planet_positions)
            
            arudha_data = {}
            for i, arudha_rasi in enumerate(bhava_arudhas, 1):
                arudha_data[f'A{i}'] = {
                    'house': i,
                    'arudha_rasi': arudha_rasi,
                    'arudha_rasi_name': self.RASI_NAMES[arudha_rasi]
                }
            
            return arudha_data
        except Exception as e:
            return {'error': str(e)}
    
    def _get_houses_with_planets(self, planet_positions: List[Tuple], 
                                 asc_house: Tuple) -> Dict[int, List[str]]:
        """Organize planets by house"""
        houses = {i: [] for i in range(12)}
        
        # Add planets to houses (skip first element which is ascendant)
        for planet_data in planet_positions[1:10]:
            planet_id, (rasi, _) = planet_data
            houses[rasi].append(self.PLANET_NAMES[planet_id])
        
        return houses
    
    def _format_longitude(self, longitude: float) -> Dict[str, Any]:
        """Format longitude into rasi and degrees"""
        rasi = int(longitude / 30)
        degrees = longitude % 30
        
        return {
            'longitude': longitude,
            'rasi': rasi,
            'rasi_name': self.RASI_NAMES[rasi],
            'degrees_in_rasi': degrees
        }
    
    def _get_special_lagnas_formatted(self, dob: Tuple, tob: Tuple, jd: float, place: Any) -> List[Dict[str, Any]]:
        """Get special lagnas formatted like planets"""
        special_lagnas_list = []
        
        # Define special lagnas to calculate - these return (rasi, degrees_in_rasi)
        lagnas_config = [
            ('Bhava Lagna', lambda j, p: drik.bhava_lagna(j, p)),
            ('Hora Lagna', lambda j, p: drik.hora_lagna(j, p)),
            ('Ghati Lagna', lambda j, p: drik.ghati_lagna(j, p)),
            ('Vighati Lagna', lambda j, p: drik.vighati_lagna(j, p)),
            ('Varnada Lagna', lambda j, p: charts.varnada_lagna(drik.Date(dob[0], dob[1], dob[2]), tob, p)),
            ('Sree Lagna', lambda j, p: drik.sree_lagna(j, p)),
            ('Pranapada Lagna', lambda j, p: drik.pranapada_lagna(j, p)),
            ('Indu Lagna', lambda j, p: drik.indu_lagna(j, p)),
        ]
        
        for name, func in lagnas_config:
            try:
                result = func(jd, place)
                # Result format: (rasi, degrees_in_rasi) or [rasi, degrees_in_rasi]
                if isinstance(result, (tuple, list)) and len(result) >= 2:
                    rasi, degrees_in_rasi = result[0], result[1]
                    longitude = (rasi * 30) + degrees_in_rasi
                    nak_idx, nak_pada, _ = drik.nakshatra_pada(longitude)
                    nav_rasi, _ = drik.dasavarga_from_long(longitude, 9)
                    
                    special_lagnas_list.append({
                        'name': name,
                        'rasi': rasi,
                        'rasi_name': self.RASI_NAMES[rasi],
                        'longitude': longitude,
                        'degrees_in_rasi': degrees_in_rasi,
                        'nakshatra': nak_idx - 1,
                        'nakshatra_name': self.NAKSHATRA_NAMES[nak_idx - 1],
                        'nakshatra_pada': nak_pada,
                        'navamsa_rasi': nav_rasi,
                        'navamsa_rasi_name': self.RASI_NAMES[nav_rasi],
                        'retrograde': False
                    })
            except Exception as e:
                print(f"Error calculating {name}: {str(e)}")
        
        return special_lagnas_list
    
    def _get_upagrahas_formatted(self, dob: Tuple, tob: Tuple, place: Any, ayanamsa: str = "LAHIRI") -> List[Dict[str, Any]]:
        """Get upagrahas formatted like planets - ordered to match screenshot"""
        from datetime import date as Date
        
        # Convert tuples to Date object for functions that need it
        dob_date = Date(dob[0], dob[1], dob[2])
        
        # Get sun longitude for solar upagrahas and jd for bhrigu bindu
        jd = utils.julian_day_number(dob, tob)
        planet_positions = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=1)
        sun_long = (planet_positions[1][1][0] * 30) + planet_positions[1][1][1]  # Sun is at index 1
        
        # Dictionary to store all upagrahas temporarily
        upagrahas_dict = {}
        
        # Time-based upagrahas (requires dob, tob, place)
        time_upagrahas = [
            ('Maandi', drik.maandi_longitude),
            ('Gulika', drik.gulika_longitude),
            ('Kaala', drik.kaala_longitude),
            ('Mrityu', drik.mrityu_longitude),
            ('Artha Prahara', drik.artha_praharaka_longitude),
            ('Yama Ghantaka', drik.yama_ghantaka_longitude),
        ]
        
        for name, func in time_upagrahas:
            try:
                result = func(dob_date, tob, place)
                # Result format: [rasi, degrees_in_rasi] as list
                if (isinstance(result, (tuple, list))) and len(result) >= 2:
                    rasi, degrees_in_rasi = result[0], result[1]
                    longitude = (rasi * 30) + degrees_in_rasi
                    nak_idx, nak_pada, _ = drik.nakshatra_pada(longitude)
                    nav_rasi, _ = drik.dasavarga_from_long(longitude, 9)
                    
                    upagrahas_dict[name] = {
                        'name': name,
                        'rasi': rasi,
                        'rasi_name': self.RASI_NAMES[rasi],
                        'longitude': longitude,
                        'degrees_in_rasi': degrees_in_rasi,
                        'nakshatra': nak_idx - 1,
                        'nakshatra_name': self.NAKSHATRA_NAMES[nak_idx - 1],
                        'nakshatra_pada': nak_pada,
                        'navamsa_rasi': nav_rasi,
                        'navamsa_rasi_name': self.RASI_NAMES[nav_rasi],
                        'retrograde': False
                    }
            except Exception as e:
                print(f"Error calculating {name}: {str(e)}")
        
        # Bhrigu Bindhu Lagna (uses jd, place)
        try:
            result = drik.bhrigu_bindhu_lagna(jd, place)
            if isinstance(result, (tuple, list)) and len(result) >= 2:
                rasi, degrees_in_rasi = result[0], result[1]
                longitude = (rasi * 30) + degrees_in_rasi
                nak_idx, nak_pada, _ = drik.nakshatra_pada(longitude)
                nav_rasi, _ = drik.dasavarga_from_long(longitude, 9)
                
                upagrahas_dict['Bhrigu Bindu'] = {
                    'name': 'Bhrigu Bindu',
                    'rasi': rasi,
                    'rasi_name': self.RASI_NAMES[rasi],
                    'longitude': longitude,
                    'degrees_in_rasi': degrees_in_rasi,
                    'nakshatra': nak_idx - 1,
                    'nakshatra_name': self.NAKSHATRA_NAMES[nak_idx - 1],
                    'nakshatra_pada': nak_pada,
                    'navamsa_rasi': nav_rasi,
                    'navamsa_rasi_name': self.RASI_NAMES[nav_rasi],
                    'retrograde': False
                }
        except Exception as e:
            print(f"Error calculating Bhrigu Bindu: {str(e)}")
        
        # Solar upagrahas (based on Sun's longitude)
        solar_upagrahas = [
            ('Dhooma', (sun_long + 133 + 20.0/60) % 360),
            ('Vyatipata', (360.0 - ((sun_long + 133 + 20.0/60) % 360)) % 360),
            ('Parivesha', ((360.0 - ((sun_long + 133 + 20.0/60) % 360)) % 360 + 180.0) % 360),
            ('Indra Chaapa', (360.0 - (((360.0 - ((sun_long + 133 + 20.0/60) % 360)) % 360 + 180.0) % 360)) % 360),
            ('Upaketu', (sun_long - 30.0) % 360),
        ]
        
        for name, longitude in solar_upagrahas:
            try:
                rasi = int(longitude / 30)
                degrees_in_rasi = longitude % 30
                nak_idx, nak_pada, _ = drik.nakshatra_pada(longitude)
                nav_rasi, _ = drik.dasavarga_from_long(longitude, 9)
                upagrahas_dict[name] = {
                    'name': name,
                    'rasi': rasi,
                    'rasi_name': self.RASI_NAMES[rasi],
                    'longitude': longitude,
                    'degrees_in_rasi': degrees_in_rasi,
                    'nakshatra': nak_idx - 1,
                    'nakshatra_name': self.NAKSHATRA_NAMES[nak_idx - 1],
                    'nakshatra_pada': nak_pada,
                    'navamsa_rasi': nav_rasi,
                    'navamsa_rasi_name': self.RASI_NAMES[nav_rasi],
                    'retrograde': False
                }
            except Exception as e:
                print(f"Error calculating {name}: {str(e)}")
        
        # Return in exact screenshot order
        ordered_names = [
            'Maandi', 'Gulika', 'Bhrigu Bindu', 'Dhooma', 'Vyatipata',
            'Parivesha', 'Indra Chaapa', 'Upaketu', 'Kaala', 'Mrityu',
            'Artha Prahara', 'Yama Ghantaka'
        ]
        
        upagrahas_list = []
        for name in ordered_names:
            if name in upagrahas_dict:
                upagrahas_list.append(upagrahas_dict[name])
        
        return upagrahas_list

