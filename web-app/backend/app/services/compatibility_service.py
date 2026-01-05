"""
Marriage Compatibility calculation service
Handles North Indian (Ashta Koota) and South Indian (10 Porutham) methods
"""
import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora.horoscope.chart import charts
from jhora.horoscope.match import compatibility
from jhora import utils, const
from typing import Dict, List, Any


class CompatibilityService:
    """Service for marriage compatibility calculations"""
    
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
    
    def get_north_indian_compatibility(self, boy_details: Dict[str, Any],
                                      girl_details: Dict[str, Any],
                                      ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate North Indian compatibility (Ashta Koota - 8 factors, 36 points)
        """
        self._set_ayanamsa(ayanamsa)
        
        # Parse boy's details
        boy_dob, boy_tob, boy_place = self._parse_birth_details(boy_details)
        boy_jd = utils.julian_day_number(boy_dob, boy_tob)
        boy_planet_positions = charts.divisional_chart(boy_jd, boy_place)
        boy_moon_nakshatra = drik.nakshatra(boy_jd, boy_place)
        
        # Parse girl's details
        girl_dob, girl_tob, girl_place = self._parse_birth_details(girl_details)
        girl_jd = utils.julian_day_number(girl_dob, girl_tob)
        girl_planet_positions = charts.divisional_chart(girl_jd, girl_place)
        girl_moon_nakshatra = drik.nakshatra(girl_jd, girl_place)
        
        try:
            # Calculate all 8 kootas
            match_result = compatibility.ashta_koota_compatibility(
                boy_moon_nakshatra[0], boy_planet_positions,
                girl_moon_nakshatra[0], girl_planet_positions
            )
            
            # Format results
            factors = []
            total_score = 0
            max_score = 36
            
            # Varna Koota (1 point)
            if 'varna' in match_result:
                factors.append({
                    'name': 'Varna Koota',
                    'description': 'Spiritual compatibility based on caste',
                    'score': match_result['varna'],
                    'max_score': 1,
                    'compatible': match_result['varna'] > 0
                })
                total_score += match_result['varna']
            
            # Vashya Koota (2 points)
            if 'vashya' in match_result:
                factors.append({
                    'name': 'Vashya Koota',
                    'description': 'Mutual attraction and control',
                    'score': match_result['vashya'],
                    'max_score': 2,
                    'compatible': match_result['vashya'] > 0
                })
                total_score += match_result['vashya']
            
            # Tara Koota (3 points)
            if 'tara' in match_result:
                factors.append({
                    'name': 'Tara Koota',
                    'description': 'Birth star compatibility',
                    'score': match_result['tara'],
                    'max_score': 3,
                    'compatible': match_result['tara'] > 1
                })
                total_score += match_result['tara']
            
            # Yoni Koota (4 points)
            if 'yoni' in match_result:
                factors.append({
                    'name': 'Yoni Koota',
                    'description': 'Sexual and biological compatibility',
                    'score': match_result['yoni'],
                    'max_score': 4,
                    'compatible': match_result['yoni'] > 2
                })
                total_score += match_result['yoni']
            
            # Graha Maitri Koota (5 points)
            if 'graha_maitri' in match_result:
                factors.append({
                    'name': 'Graha Maitri Koota',
                    'description': 'Mental and intellectual compatibility',
                    'score': match_result['graha_maitri'],
                    'max_score': 5,
                    'compatible': match_result['graha_maitri'] > 2
                })
                total_score += match_result['graha_maitri']
            
            # Gana Koota (6 points)
            if 'gana' in match_result:
                factors.append({
                    'name': 'Gana Koota',
                    'description': 'Temperament compatibility',
                    'score': match_result['gana'],
                    'max_score': 6,
                    'compatible': match_result['gana'] > 3
                })
                total_score += match_result['gana']
            
            # Rasi/Bhakoot Koota (7 points)
            if 'rasi' in match_result:
                factors.append({
                    'name': 'Rasi Koota',
                    'description': 'Moon sign compatibility',
                    'score': match_result['rasi'],
                    'max_score': 7,
                    'compatible': match_result['rasi'] > 3
                })
                total_score += match_result['rasi']
            
            # Nadi Koota (8 points) - Most important
            if 'nadi' in match_result:
                factors.append({
                    'name': 'Nadi Koota',
                    'description': 'Health and progeny compatibility (most important)',
                    'score': match_result['nadi'],
                    'max_score': 8,
                    'compatible': match_result['nadi'] > 0
                })
                total_score += match_result['nadi']
            
            # Overall compatibility
            percentage = (total_score / max_score) * 100
            compatible = total_score >= 18  # Minimum 18 points required
            
            if total_score >= 28:
                recommendation = "Excellent match - highly compatible"
            elif total_score >= 24:
                recommendation = "Very good match - compatible"
            elif total_score >= 18:
                recommendation = "Good match - acceptable"
            else:
                recommendation = "Below minimum score - not recommended"
            
            return {
                'method': 'North Indian (Ashta Koota)',
                'boy': boy_details,
                'girl': girl_details,
                'total_score': total_score,
                'max_score': max_score,
                'percentage': round(percentage, 2),
                'compatible': compatible,
                'factors': factors,
                'recommendation': recommendation
            }
        
        except Exception as e:
            return {
                'error': f'North Indian compatibility calculation error: {str(e)}',
                'method': 'North Indian (Ashta Koota)'
            }
    
    def get_south_indian_compatibility(self, boy_details: Dict[str, Any],
                                      girl_details: Dict[str, Any],
                                      ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """
        Calculate South Indian compatibility (10 Porutham)
        """
        self._set_ayanamsa(ayanamsa)
        
        # Parse boy's details
        boy_dob, boy_tob, boy_place = self._parse_birth_details(boy_details)
        boy_jd = utils.julian_day_number(boy_dob, boy_tob)
        boy_planet_positions = charts.divisional_chart(boy_jd, boy_place)
        boy_moon_nakshatra = drik.nakshatra(boy_jd, boy_place)
        
        # Parse girl's details
        girl_dob, girl_tob, girl_place = self._parse_birth_details(girl_details)
        girl_jd = utils.julian_day_number(girl_dob, girl_tob)
        girl_planet_positions = charts.divisional_chart(girl_jd, girl_place)
        girl_moon_nakshatra = drik.nakshatra(girl_jd, girl_place)
        
        try:
            # Calculate Tamil 10 Porutham
            match_result = compatibility.south_indian_compatibility(
                boy_moon_nakshatra[0], boy_planet_positions,
                girl_moon_nakshatra[0], girl_planet_positions
            )
            
            factors = []
            compatible_count = 0
            total_factors = 10
            
            # The 10 Poruthams
            porutham_names = [
                ('dina', 'Dina Porutham', 'Birth star compatibility'),
                ('gana', 'Gana Porutham', 'Nature/character compatibility'),
                ('yoni', 'Yoni Porutham', 'Sexual compatibility'),
                ('rasi', 'Rasi Porutham', 'Moon sign compatibility'),
                ('rasi_adhipati', 'Rasi Adhipati Porutham', 'Moon sign lord compatibility'),
                ('vasya', 'Vasya Porutham', 'Mutual attraction'),
                ('rajju', 'Rajju Porutham', 'Longevity compatibility'),
                ('vedha', 'Vedha Porutham', 'Affliction check'),
                ('mahendra', 'Mahendra Porutham', 'Progeny and prosperity'),
                ('stree_deergha', 'Stree Deergha Porutham', 'Prosperity for woman')
            ]
            
            for key, name, desc in porutham_names:
                if key in match_result:
                    is_compatible = bool(match_result[key])
                    factors.append({
                        'name': name,
                        'description': desc,
                        'compatible': is_compatible,
                        'score': 1 if is_compatible else 0
                    })
                    if is_compatible:
                        compatible_count += 1
            
            # Overall compatibility
            percentage = (compatible_count / total_factors) * 100
            compatible = compatible_count >= 6  # Minimum 6 out of 10 required
            
            if compatible_count >= 9:
                recommendation = "Excellent match - 9-10 poruthams"
            elif compatible_count >= 7:
                recommendation = "Very good match - 7-8 poruthams"
            elif compatible_count >= 6:
                recommendation = "Good match - 6 poruthams (acceptable)"
            else:
                recommendation = f"Below minimum - only {compatible_count} poruthams (not recommended)"
            
            return {
                'method': 'South Indian (10 Porutham)',
                'boy': boy_details,
                'girl': girl_details,
                'total_score': compatible_count,
                'max_score': total_factors,
                'percentage': round(percentage, 2),
                'compatible': compatible,
                'factors': factors,
                'recommendation': recommendation
            }
        
        except Exception as e:
            return {
                'error': f'South Indian compatibility calculation error: {str(e)}',
                'method': 'South Indian (10 Porutham)'
            }
    
    def get_both_compatibilities(self, boy_details: Dict[str, Any],
                                girl_details: Dict[str, Any],
                                ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Get both North and South Indian compatibility"""
        north = self.get_north_indian_compatibility(boy_details, girl_details, ayanamsa)
        south = self.get_south_indian_compatibility(boy_details, girl_details, ayanamsa)
        
        return {
            'boy': boy_details,
            'girl': girl_details,
            'north_indian': north,
            'south_indian': south,
            'overall_compatible': north.get('compatible', False) and south.get('compatible', False)
        }

