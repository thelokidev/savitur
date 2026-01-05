"""
Strength (Bala) calculation service
Handles Shadbala, Ashtakavarga, and other strength calculations
"""
import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora.horoscope.chart import charts, strength, ashtakavarga
from jhora import utils, const
from typing import Dict, List, Any


class StrengthService:
    """Service for all strength calculations"""
    
    PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    PLANET_NAMES_WITH_NODES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    
    def __init__(self):
        pass
    
    def _parse_birth_details(self, birth_details: Dict[str, Any]):
        """Parse birth details"""
        date_str = birth_details['date']
        year, month, day = map(int, date_str.split('-'))
        dob = (year, month, day)
        
        time_str = birth_details['time']
        hour, minute, second = map(int, time_str.split(':'))
        tob = (hour, minute, second)
        
        place_info = birth_details['place']
        place = drik.Place(
            place_info['name'],
            place_info['latitude'],
            place_info['longitude'],
            place_info['timezone']
        )
        
        return dob, tob, place
    
    def _set_ayanamsa(self, ayanamsa: str = "LAHIRI"):
        """Set ayanamsa mode"""
        drik.set_ayanamsa_mode(ayanamsa.upper())
    
    def get_shadbala(self, birth_details: Dict[str, Any],
                    ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Shadbala (six-fold strength) for all planets"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            # Get all six balas at once
            # Returns: [sthana, kaala, dig, cheshta, naisargika, drik, sum_virupas, sum_rupas, percent_strength]
            sb_data = strength.shad_bala(jd, place, ayanamsa_mode=ayanamsa.upper())
            
            print(f"DEBUG shad_bala type: {type(sb_data)}, length: {len(sb_data)}")
            
            sthana_bala = sb_data[0]
            kaala_bala = sb_data[1]
            dig_bala = sb_data[2]
            cheshta_bala = sb_data[3]
            naisargika_bala = sb_data[4]
            drik_bala = sb_data[5]
            total_virupas = sb_data[6]
            total_rupas = sb_data[7]
            percent_strength = sb_data[8]
            
            # Format results
            shadbala_values = {}
            for i, planet_name in enumerate(self.PLANET_NAMES):
                shadbala_values[planet_name] = {
                    'sthana_bala': round(float(sthana_bala[i]) / 60.0, 2),  # Convert to rupas
                    'dig_bala': round(float(dig_bala[i]) / 60.0, 2),
                    'kaala_bala': round(float(kaala_bala[i]) / 60.0, 2),
                    'cheshta_bala': round(float(cheshta_bala[i]) / 60.0, 2),
                    'naisargika_bala': round(float(naisargika_bala[i]) / 60.0, 2),
                    'drik_bala': round(float(drik_bala[i]) / 60.0, 2),
                    'total_shadbala': round(float(total_rupas[i]), 2),
                    'percent_strength': round(float(percent_strength[i]) * 100, 2)
                }
            
            print(f"DEBUG Shadbala values: {shadbala_values}")
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'calculation_type': 'Shadbala',
                'planets': shadbala_values
            }
        except Exception as e:
            print(f"ERROR in get_shadbala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Shadbala calculation error: {str(e)}'}
    
    def get_ashtakavarga(self, birth_details: Dict[str, Any],
                        ayanamsa: str = "LAHIRI",
                        chart_type: str = "rasi") -> Dict[str, Any]:
        """Calculate Ashtakavarga"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        divisional_factor = 1 if chart_type == "rasi" else 9  # D-1 or D-9
        
        try:
            # Get planet positions
            planet_positions = charts.divisional_chart(jd, place, divisional_chart_factor=divisional_factor)
            
            print(f"DEBUG: planet_positions type: {type(planet_positions)}")
            print(f"DEBUG: planet_positions: {planet_positions}")
            
            house_to_planet_list = utils.get_house_planet_list_from_planet_positions(planet_positions)
            print(f"DEBUG: house_to_planet_list: {house_to_planet_list}")
            p_to_h_debug = utils.get_planet_to_house_dict_from_chart(house_to_planet_list)
            print(f"DEBUG: p_to_h from chart: {p_to_h_debug}")
            
            bav, sav, pav = ashtakavarga.get_ashtaka_varga(house_to_planet_list)
            
            print(f"DEBUG: bav type: {type(bav)}, length: {len(bav) if hasattr(bav, '__len__') else 'N/A'}")
            print(f"DEBUG: sav type: {type(sav)}, length: {len(sav) if hasattr(sav, '__len__') else 'N/A'}")
            print(f"DEBUG: sav value: {sav}")
            print(f"DEBUG: pav type: {type(pav)}, length: {len(pav) if hasattr(pav, '__len__') else 'N/A'}")
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'chart_type': f'D-{divisional_factor}',
                'bhinnashtakavarga': self._format_bav(bav),
                'prastarashtakavarga': self._format_pav(pav),
                'sarvashtakavarga': sav
            }
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR in get_ashtakavarga: {error_details}")
            return {'error': f'Ashtakavarga calculation error: {str(e)}'}
    
    def get_shodhaya_pinda(self, birth_details: Dict[str, Any],
                          ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Shodhaya Pinda"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            # Get planet positions for Rasi and Navamsa
            rasi_positions = charts.divisional_chart(jd, place, divisional_chart_factor=1)
            navamsa_positions = charts.divisional_chart(jd, place, divisional_chart_factor=9)
            
            # Calculate Shodhaya Pinda
            rasi_pinda = ashtakavarga.get_shodhaya_pinda(rasi_positions, 'rasi')
            graha_pinda = ashtakavarga.get_shodhaya_pinda(rasi_positions, 'graha')
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'rasi_pinda': rasi_pinda,
                'graha_pinda': graha_pinda,
                'shodhaya_pinda': {
                    planet: rasi_pinda.get(planet, 0) + graha_pinda.get(planet, 0)
                    for planet in self.PLANET_NAMES
                }
            }
        except Exception as e:
            return {'error': f'Shodhaya Pinda calculation error: {str(e)}'}
    
    def get_bhava_bala(self, birth_details: Dict[str, Any],
                      ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Bhava Bala (house strength)"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            # Use the combined bhava_bala function from PyJHora
            # Returns: [bb_virupas, bb_rupas, bb_strength] for 12 houses
            bb_data = strength.bhava_bala(jd, place)
            
            bb_virupas = bb_data[0]  # Total bhava bala in virupas
            bb_rupas = bb_data[1]    # Total in rupas
            bb_strength = bb_data[2] # Strength percentage
            
            # Get individual components using internal functions
            adhipathi_bala = strength._bhava_adhipathi_bala(jd, place)
            dig_bala = strength._bhava_dig_bala(jd, place)
            drik_bala = strength._bhava_drik_bala(jd, place)
            
            bhava_balas = {}
            for house in range(12):
                bhava_balas[f'House_{house + 1}'] = {
                    'adhipathi_bala': round(float(adhipathi_bala[house]), 2),
                    'dig_bala': round(float(dig_bala[house]), 2),
                    'drik_bala': round(float(drik_bala[house]), 2),
                    'total_bhava_bala': round(float(bb_virupas[house]), 2),
                    'total_rupas': round(float(bb_rupas[house]), 2),
                    'strength_percent': round(float(bb_strength[house]) * 100, 2)
                }
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'houses': bhava_balas
            }
        except Exception as e:
            print(f"ERROR in get_bhava_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Bhava Bala calculation error: {str(e)}'}
    
    def _format_bav(self, bav: List[List[int]]) -> Dict[str, Any]:
        """Format BAV keyed by planet name."""
        try:
            planets = self.PLANET_NAMES + ['Lagnam']
            return {planets[i]: {f'rasi_{j+1}': v for j, v in enumerate(row)} for i, row in enumerate(bav)}
        except Exception:
            return {}

    def _format_pav(self, pav: List[List[List[int]]]) -> Dict[str, Any]:
        """Format PAV nested by planet name and contributor."""
        try:
            planets = self.PLANET_NAMES + ['Lagnam']
            contributors = self.PLANET_NAMES + ['Lagnam', 'Total']
            formatted: Dict[str, Any] = {}
            for i, planet_block in enumerate(pav):
                planet_name = planets[i]
                formatted[planet_name] = {}
                for j, contrib_row in enumerate(planet_block):
                    contrib_name = contributors[j] if j < len(contributors) else f'contrib_{j}'
                    formatted[planet_name][contrib_name] = {f'rasi_{k+1}': v for k, v in enumerate(contrib_row)}
            return formatted
        except Exception:
            return {}
    
    def get_vimsopaka_bala(self, birth_details: Dict[str, Any],
                          ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Vimsopaka Bala (all 4 variants)"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            from jhora.horoscope.chart import charts
            
            # Get all 4 Vimsopaka variants (returns dicts with integer keys)
            shadvarga = charts.vimsopaka_shadvarga_of_planets(jd, place)
            sapthavarga = charts.vimsopaka_sapthavarga_of_planets(jd, place)
            dhasavarga = charts.vimsopaka_dhasavarga_of_planets(jd, place)
            shodhasavarga = charts.vimsopaka_shodhasavarga_of_planets(jd, place)
            
            print(f"DEBUG dhasavarga type: {type(dhasavarga)}, value: {dhasavarga}")
            
            # Format results - these return dicts with integer keys (0..8 = Sun..Saturn, Rahu, Ketu)
            def format_vimsopaka(varga_dict):
                result = {}
                for i in range(9):  # Sun through Saturn, Rahu, Ketu
                    if i in varga_dict:
                        value = varga_dict[i]
                        # value is [score, description, numeric_value]
                        if isinstance(value, (list, tuple)) and len(value) >= 3:
                            result[self.PLANET_NAMES_WITH_NODES[i]] = round(float(value[2]), 2)
                        elif isinstance(value, (int, float)):
                            result[self.PLANET_NAMES_WITH_NODES[i]] = round(float(value), 2)
                        else:
                            result[self.PLANET_NAMES_WITH_NODES[i]] = 0.0
                    else:
                        result[self.PLANET_NAMES_WITH_NODES[i]] = 0.0
                return result
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'shadvarga': format_vimsopaka(shadvarga),
                'sapthavarga': format_vimsopaka(sapthavarga),
                'dhasavarga': format_vimsopaka(dhasavarga),
                'shodhasavarga': format_vimsopaka(shodhasavarga)
            }
        except Exception as e:
            print(f"ERROR in get_vimsopaka_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Vimsopaka Bala calculation error: {str(e)}'}
    
    def get_pancha_vargeeya_bala(self, birth_details: Dict[str, Any],
                                 ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Pancha Vargeeya Bala"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            pvb = strength.pancha_vargeeya_bala(jd, place)
            
            print(f"DEBUG pancha_vargeeya_bala type: {type(pvb)}, value: {pvb}")
            
            # pancha_vargeeya_bala returns a dict with integer keys
            result = {}
            for i in range(7):
                if i in pvb:
                    result[self.PLANET_NAMES[i]] = round(float(pvb[i]), 2)
                else:
                    result[self.PLANET_NAMES[i]] = 0.0
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'planets': result
            }
        except Exception as e:
            print(f"ERROR in get_pancha_vargeeya_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Pancha Vargeeya Bala calculation error: {str(e)}'}
    
    def get_dwadasa_vargeeya_bala(self, birth_details: Dict[str, Any],
                                  ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Dwadasa Vargeeya Bala"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            dvb = strength.dwadhasa_vargeeya_bala(jd, place)
            
            print(f"DEBUG dwadhasa_vargeeya_bala type: {type(dvb)}, value: {dvb}")
            
            # dwadhasa_vargeeya_bala returns a dict with integer keys
            result = {}
            for i in range(7):
                if i in dvb:
                    result[self.PLANET_NAMES[i]] = float(dvb[i])
                else:
                    result[self.PLANET_NAMES[i]] = 0.0
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'planets': result
            }
        except Exception as e:
            print(f"ERROR in get_dwadasa_vargeeya_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Dwadasa Vargeeya Bala calculation error: {str(e)}'}
    
    def get_harsha_bala(self, birth_details: Dict[str, Any],
                       ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Harsha Bala"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        
        try:
            hb = strength.harsha_bala(dob, tob, place)
            
            print(f"DEBUG harsha_bala type: {type(hb)}, value: {hb}")
            
            # harsha_bala returns a dict with integer keys
            result = {}
            for i in range(7):
                if i in hb:
                    result[self.PLANET_NAMES[i]] = float(hb[i])
                else:
                    result[self.PLANET_NAMES[i]] = 0.0
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'planets': result
            }
        except Exception as e:
            print(f"ERROR in get_harsha_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Harsha Bala calculation error: {str(e)}'}
    
    def get_ishta_kashta_phala(self, birth_details: Dict[str, Any],
                               ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate Ishta Phala and Kashta Phala"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        try:
            # Get Ishta Phala (returns a list)
            ishta_phala = strength._ishta_phala(jd, place)
            
            print(f"DEBUG ishta_phala type: {type(ishta_phala)}, value: {ishta_phala}")
            
            # Kashta Phala is (60 - Ishta Phala)
            kashta_phala = [60 - ip for ip in ishta_phala]
            
            # Format as dicts with planet names
            ishta_dict = {}
            kashta_dict = {}
            for i in range(7):
                if i < len(ishta_phala):
                    ishta_dict[self.PLANET_NAMES[i]] = round(float(ishta_phala[i]), 2)
                    kashta_dict[self.PLANET_NAMES[i]] = round(float(kashta_phala[i]), 2)
                else:
                    ishta_dict[self.PLANET_NAMES[i]] = 0.0
                    kashta_dict[self.PLANET_NAMES[i]] = 0.0
            
            return {
                'birth_date': birth_details['date'],
                'birth_time': birth_details['time'],
                'ishta_phala': ishta_dict,
                'kashta_phala': kashta_dict
            }
        except Exception as e:
            print(f"ERROR in get_ishta_kashta_phala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': f'Ishta/Kashta Phala calculation error: {str(e)}'}


