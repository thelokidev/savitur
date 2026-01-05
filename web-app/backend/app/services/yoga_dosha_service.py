"""
Enhanced Yoga and Dosha calculation service
Handles 100+ Yogas and 8 types of Doshas with categorization
"""
import sys
import os

# Add PyJHora to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../PyJHora/src'))

from jhora.panchanga import drik
from jhora.horoscope.chart import charts, yoga, dosha, raja_yoga
from jhora import utils, const
from typing import Dict, List, Any
from app.services import yoga_calculator


class YogaDoshaService:
    """Service for Yoga and Dosha calculations with categorization"""
    
    # Yoga Classification
    EXCELLENT_YOGAS = [
        'Hamsa Yoga', 'Ruchaka Yoga', 'Bhadra Yoga', 'Maalavya Yoga', 'Sasa Yoga',
        'Gaja Kesari Yoga', 'Dharma Karmadhipati Raja Yoga', 'Neecha Bhanga Raja Yoga',
        'Lakshmi Yoga', 'Saraswathi Yoga', 'Brahma Yoga', 'Vishnu Yoga', 'Siva Yoga',
        'Parvata Yoga', 'Kaahala Yoga', 'Chaamara Yoga', 'Sankha Yoga'
    ]
    
    GOOD_YOGAS = [
        'Adhi Yoga', 'Vesi Yoga', 'Vosi Yoga', 'Ubhayachara Yoga',
        'Sunaphaa Yoga', 'Anaphaa Yoga', 'Duradhara Yoga',
        'Chandra Mangala Yoga', 'Guru Mangala Yoga', 'Amala Yoga',
        'Budha Aaditya Yoga', 'Nipuna Yoga', 'Vipareetha Raja Yoga',
        'Bheri Yoga', 'Mridanga Yoga', 'Sreenaatha Yoga', 'Matsya Yoga',
        'Koorma Yoga', 'Khadga Yoga', 'Kusuma Yoga', 'Kalaanidhi Yoga',
        'Kalpadruma Yoga', 'Lagnaadhi Yoga', 'Hari Yoga', 'Hara Yoga',
        'Gouri Yoga', 'Chandikaa Yoga', 'Saarada Yoga', 'Bhaarathi Yoga',
        'Amsaavatara Yoga', 'Devendra Yoga', 'Indra Yoga', 'Ravi Yoga',
        'Bhaaskara Yoga', 'Kulavardhana Yoga', 'Vasumati Yoga', 'Gandharva Yoga',
        'Go Yoga', 'Vidyut Yoga', 'Chapa Yoga', 'Pushkala Yoga',
        'Makuta Yoga', 'Jaya Yoga', 'Harsha Yoga', 'Sarala Yoga', 'Vimala Yoga',
        'Subha Yoga', 'Maalaa Yoga', 'Kamala Yoga', 'Trilochana Yoga'
    ]
    
    NEUTRAL_YOGAS = [
        'Rajju Yoga', 'Musala Yoga', 'Nala Yoga', 'Gadaa Yoga',
        'Sakata Yoga', 'Vihanga Yoga', 'Sringaataka Yoga', 'Hala Yoga',
        'Vajra Yoga', 'Yava Yoga', 'Vaapi Yoga', 'Yoopa Yoga',
        'Sara Yoga', 'Sakti Yoga', 'Danda Yoga', 'Naukaa Yoga',
        'Koota Yoga', 'Chatra Yoga', 'Chaapa Yoga', 'Ardha Chandra Yoga',
        'Chakra Yoga', 'Samudra Yoga', 'Veenaa Yoga', 'Daama Yoga',
        'Paasa Yoga', 'Kedaara Yoga'
    ]
    
    INAUSPICIOUS_YOGAS = [
        'Kemadruma Yoga', 'Sarpa Yoga', 'Asubha Yoga',
        'Soola Yoga', 'Yuga Yoga', 'Gola Yoga'
    ]
    
    def __init__(self):
        pass
    
    def _classify_yoga(self, yoga_name: str) -> Dict[str, Any]:
        """Classify yoga as excellent, good, neutral, or inauspicious"""
        if yoga_name in self.EXCELLENT_YOGAS:
            return {
                'quality': 'Excellent',
                'strength': 'Very Strong',
                'impact': 'Highly Beneficial',
                'score': 10
            }
        elif yoga_name in self.GOOD_YOGAS:
            return {
                'quality': 'Good',
                'strength': 'Strong',
                'impact': 'Beneficial',
                'score': 7
            }
        elif yoga_name in self.NEUTRAL_YOGAS:
            return {
                'quality': 'Neutral',
                'strength': 'Moderate',
                'impact': 'Mixed Results',
                'score': 5
            }
        elif yoga_name in self.INAUSPICIOUS_YOGAS:
            return {
                'quality': 'Inauspicious',
                'strength': 'Challenging',
                'impact': 'Requires Remedies',
                'score': 3
            }
        else:
            return {
                'quality': 'Unknown',
                'strength': 'Moderate',
                'impact': 'Requires Analysis',
                'score': 5
            }
    
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
    
    def get_all_yogas(self, birth_details: Dict[str, Any],
                     ayanamsa: str = "LAHIRI", divisional_chart_factor: int = 1) -> Dict[str, Any]:
        """Calculate all yogas present in the chart with classification"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get planet positions for the specified divisional chart
        planet_positions = charts.divisional_chart(jd, place, ayanamsa_mode=ayanamsa, divisional_chart_factor=divisional_chart_factor)
        
        # Use our local yoga calculator for reliable detection
        detected_yogas = yoga_calculator.calculate_all_yogas(planet_positions)
        
        # Build all_yogas_list from detected yogas
        all_yogas_list = []
        for yoga_item in detected_yogas:
            yoga_entry = {
                'name': yoga_item['name'],
                'category': yoga_item['category'],
                'description': yoga_item['description'],
                'divisional_chart': f'D-{divisional_chart_factor}'
            }
            # Add classification
            classification = self._classify_yoga(yoga_item['name'])
            yoga_entry.update(classification)
            all_yogas_list.append(yoga_entry)
        
        # Get Raja Yogas separately
        raja_yogas = self._get_raja_yogas(jd, place, planet_positions)
        
        # Categorize yogas
        excellent_yogas = [y for y in all_yogas_list if y.get('quality') == 'Excellent']
        good_yogas = [y for y in all_yogas_list if y.get('quality') == 'Good']
        neutral_yogas = [y for y in all_yogas_list if y.get('quality') == 'Neutral']
        inauspicious_yogas = [y for y in all_yogas_list if y.get('quality') == 'Inauspicious']
        unknown_yogas = [y for y in all_yogas_list if y.get('quality') == 'Unknown']
        
        # Calculate overall chart strength
        total_score = sum(y.get('score', 5) for y in all_yogas_list)
        avg_score = total_score / len(all_yogas_list) if all_yogas_list else 0
        
        return {
            'birth_date': birth_details['date'],
            'birth_time': birth_details['time'],
            'divisional_chart': f'D-{divisional_chart_factor}',
            'total_yogas': len(all_yogas_list),
            'yoga_summary': {
                'excellent': len(excellent_yogas),
                'good': len(good_yogas),
                'neutral': len(neutral_yogas),
                'inauspicious': len(inauspicious_yogas)
            },
            'chart_strength': {
                'total_score': total_score,
                'average_score': round(avg_score, 2),
                'rating': self._get_chart_rating(avg_score)
            },
            'yogas_by_category': {
                'excellent': excellent_yogas,
                'good': good_yogas + unknown_yogas,  # Unknown yogas are generally positive
                'neutral': neutral_yogas,
                'inauspicious': inauspicious_yogas
            },
            'all_yogas': all_yogas_list,
            'raja_yogas': raja_yogas,
            'doshas': []  # Will be populated by get_all_doshas
        }
    
    def _categorize_yoga_type(self, yoga_name: str) -> str:
        """Categorize yoga by its type based on name"""
        yoga_lower = yoga_name.lower()
        if 'raja' in yoga_lower:
            return 'Raja Yoga'
        elif any(x in yoga_lower for x in ['dhana', 'lakshmi', 'vasumati']):
            return 'Wealth Yoga'
        elif any(x in yoga_lower for x in ['ruchaka', 'bhadra', 'hamsa', 'maalavya', 'sasa']):
            return 'Pancha Mahapurusha'
        elif any(x in yoga_lower for x in ['sun', 'vesi', 'vosi', 'ubhaya', 'nipuna', 'budha_aaditya']):
            return 'Sun Yoga'
        elif any(x in yoga_lower for x in ['moon', 'chandra', 'sunaphaa', 'anaphaa', 'duradhara', 'kemadruma', 'gaja_kesari']):
            return 'Moon Yoga'
        elif any(x in yoga_lower for x in ['naabhasa', 'rajju', 'musala', 'nala', 'kedaara']):
            return 'Naabhasa Yoga'
        else:
            return 'Auspicious Yoga'
    
    def _get_chart_rating(self, avg_score: float) -> str:
        """Get overall chart rating based on average score"""
        if avg_score >= 8.5:
            return "Exceptional"
        elif avg_score >= 7.0:
            return "Very Good"
        elif avg_score >= 5.5:
            return "Good"
        elif avg_score >= 4.0:
            return "Average"
        else:
            return "Needs Attention"
    
    def _get_pancha_mahapurusha_yogas(self, planet_positions) -> List[Dict[str, Any]]:
        """Get Pancha Mahapurusha Yogas"""
        yogas_found = []
        
        # Ruchaka Yoga (Mars)
        try:
            if yoga.ruchaka_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Ruchaka Yoga',
                    'planet': 'Mars',
                    'category': 'Pancha Mahapurusha',
                    'description': 'Mars in own sign or exaltation in a kendra - grants courage, leadership, and victory'
                })
        except Exception:
            pass
        
        # Bhadra Yoga (Mercury)
        try:
            if yoga.bhadra_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Bhadra Yoga',
                    'planet': 'Mercury',
                    'category': 'Pancha Mahapurusha',
                    'description': 'Mercury in own sign or exaltation in a kendra - grants intelligence and eloquence'
                })
        except Exception:
            pass
        
        # Hamsa Yoga (Jupiter)
        try:
            if yoga.hamsa_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Hamsa Yoga',
                    'planet': 'Jupiter',
                    'category': 'Pancha Mahapurusha',
                    'description': 'Jupiter in own sign or exaltation in a kendra - grants wisdom and prosperity'
                })
        except Exception:
            pass
        
        # Maalavya Yoga (Venus)
        try:
            if yoga.maalavya_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Maalavya Yoga',
                    'planet': 'Venus',
                    'category': 'Pancha Mahapurusha',
                    'description': 'Venus in own sign or exaltation in a kendra - grants luxury and comfort'
                })
        except Exception:
            pass
        
        # Sasa Yoga (Saturn)
        try:
            if yoga.sasa_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Sasa Yoga',
                    'planet': 'Saturn',
                    'category': 'Pancha Mahapurusha',
                    'description': 'Saturn in own sign or exaltation in a kendra - grants authority and discipline'
                })
        except Exception:
            pass
        
        return yogas_found
    
    def _get_moon_yogas(self, planet_positions) -> List[Dict[str, Any]]:
        """Get Moon-based yogas"""
        yogas_found = []
        
        # Sunaphaa Yoga
        try:
            if yoga.sunaphaa_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Sunaphaa Yoga',
                    'planet': 'Moon',
                    'category': 'Moon Yoga',
                    'description': 'Planet in 2nd house from Moon - grants wealth through self-effort'
                })
        except Exception:
            pass
        
        # Anaphaa Yoga
        try:
            if yoga.anaphaa_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Anaphaa Yoga',
                    'planet': 'Moon',
                    'category': 'Moon Yoga',
                    'description': 'Planet in 12th house from Moon - grants fame and refinement'
                })
        except Exception:
            pass
        
        # Duradhara Yoga
        try:
            if yoga.duradhara_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Duradhara Yoga',
                    'planet': 'Moon',
                    'category': 'Moon Yoga',
                    'description': 'Planets in 2nd and 12th houses from Moon - grants comfort and vehicles'
                })
        except Exception:
            pass
        
        # Kemadruma Yoga
        try:
            if yoga.kemadruma_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Kemadruma Yoga',
                    'planet': 'Moon',
                    'category': 'Moon Yoga',
                    'description': 'No planets adjacent to Moon - causes financial struggles (inauspicious)'
                })
        except Exception:
            pass
        
        return yogas_found
    
    def _get_sun_yogas(self, planet_positions) -> List[Dict[str, Any]]:
        """Get Sun-based yogas"""
        yogas_found = []
        
        # Vesi Yoga
        try:
            if yoga.vesi_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Vesi Yoga',
                    'planet': 'Sun',
                    'category': 'Sun Yoga',
                    'description': 'Planet in 2nd house from Sun - grants balanced nature and prosperity'
                })
        except Exception:
            pass
        
        # Vosi Yoga
        try:
            if yoga.vosi_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Vosi Yoga',
                    'planet': 'Sun',
                    'category': 'Sun Yoga',
                    'description': 'Planet in 12th house from Sun - grants skills and good companionship'
                })
        except Exception:
            pass
        
        # Ubhayachara Yoga
        try:
            if yoga.ubhayachara_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Ubhayachara Yoga',
                    'planet': 'Sun',
                    'category': 'Sun Yoga',
                    'description': 'Planets in 2nd and 12th houses from Sun - grants royal qualities'
                })
        except Exception:
            pass
        
        return yogas_found
    
    def _get_other_yogas(self, jd, place, planet_positions) -> List[Dict[str, Any]]:
        """Get other important yogas"""
        yogas_found = []
        
        # Gaja Kesari Yoga
        try:
            if yoga.gaja_kesari_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Gaja Kesari Yoga',
                    'planets': ['Jupiter', 'Moon'],
                    'category': 'Major Yoga',
                    'description': 'Jupiter in kendra from Moon - gives wealth, wisdom, and fame'
                })
        except Exception:
            pass
        
        # Adhi Yoga
        try:
            if yoga.adhi_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Adhi Yoga',
                    'planets': ['Benefics', 'Moon'],
                    'category': 'Major Yoga',
                    'description': 'Benefics in 6th, 7th, 8th from Moon - grants power and prosperity'
                })
        except Exception:
            pass
        
        # Chandra Mangala Yoga
        try:
            if yoga.chandra_mangala_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Chandra Mangala Yoga',
                    'planets': ['Moon', 'Mars'],
                    'category': 'Wealth Yoga',
                    'description': 'Moon and Mars together - grants wealth and resourcefulness'
                })
        except Exception:
            pass
        
        # Guru Mangala Yoga
        try:
            if yoga.guru_mangala_yoga_from_planet_positions(planet_positions):
                yogas_found.append({
                    'name': 'Guru Mangala Yoga',
                    'planets': ['Jupiter', 'Mars'],
                    'category': 'Wealth Yoga',
                    'description': 'Jupiter and Mars together - grants technical skills and prosperity'
                })
        except Exception:
            pass
        
        # Amala Yoga
        try:
            if yoga.amala_yoga(planet_positions):
                yogas_found.append({
                    'name': 'Amala Yoga',
                    'planets': ['Benefics'],
                    'category': 'Auspicious Yoga',
                    'description': 'Benefics in 10th from Lagna or Moon - grants spotless reputation'
                })
        except Exception:
            pass
        
        return yogas_found
    
    def _get_raja_yogas(self, jd, place, planet_positions) -> List[Dict[str, Any]]:
        """Get Raja Yogas with classification"""
        yogas_found = []
        
        # Dharma Karmadhipati Raja Yoga
        try:
            if raja_yoga.dharma_karmadhipati_raja_yoga(planet_positions):
                yoga_data = {
                    'name': 'Dharma Karmadhipati Raja Yoga',
                    'category': 'Raja Yoga',
                    'description': 'Lords of 9th and 10th houses together - brings power and authority'
                }
                classification = self._classify_yoga(yoga_data['name'])
                yoga_data.update(classification)
                yogas_found.append(yoga_data)
        except Exception:
            pass
        
        # Vipareetha Raja Yoga
        try:
            vipareetha_yogas = raja_yoga.vipareetha_raja_yoga(planet_positions)
            if vipareetha_yogas:
                yoga_data = {
                    'name': 'Vipareetha Raja Yoga',
                    'category': 'Raja Yoga',
                    'description': 'Lords of dusthanas in dusthanas - brings success from adversity',
                    'sub_types': vipareetha_yogas
                }
                classification = self._classify_yoga(yoga_data['name'])
                yoga_data.update(classification)
                yogas_found.append(yoga_data)
        except Exception:
            pass
        
        # Neecha Bhanga Raja Yoga
        try:
            nbry = raja_yoga.neecha_bhanga_raja_yoga(planet_positions)
            if nbry:
                yoga_data = {
                    'name': 'Neecha Bhanga Raja Yoga',
                    'category': 'Raja Yoga',
                    'description': 'Cancellation of debilitation - creates powerful upliftment'
                }
                classification = self._classify_yoga(yoga_data['name'])
                yoga_data.update(classification)
                yogas_found.append(yoga_data)
        except Exception:
            pass
        
        return yogas_found
    
    def get_all_doshas(self, birth_details: Dict[str, Any],
                      ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        """Calculate all doshas with severity ratings"""
        self._set_ayanamsa(ayanamsa)
        dob, tob, place = self._parse_birth_details(birth_details)
        jd = utils.julian_day_number(dob, tob)
        
        # Get planet positions
        planet_positions = charts.divisional_chart(jd, place)
        
        doshas = {
            'kala_sarpa_dosha': self._check_kala_sarpa_dosha(planet_positions),
            'manglik_dosha': self._check_manglik_dosha(planet_positions),
            'pitru_dosha': self._check_pitru_dosha(planet_positions),
            'guru_chandala_dosha': self._check_guru_chandala_dosha(planet_positions),
            'ganda_moola_dosha': self._check_ganda_moola_dosha(jd, place),
            'kalathra_dosha': self._check_kalathra_dosha(planet_positions),
            'ghata_dosha': self._check_ghata_dosha(planet_positions),
            'shrapit_dosha': self._check_shrapit_dosha(planet_positions)
        }
        
        # Count active doshas by severity
        high_severity = sum(1 for d in doshas.values() if d.get('present') and d.get('severity') == 'High')
        medium_severity = sum(1 for d in doshas.values() if d.get('present') and d.get('severity') == 'Medium')
        low_severity = sum(1 for d in doshas.values() if d.get('present') and d.get('severity') == 'Low')
        total_active = high_severity + medium_severity + low_severity
        
        return {
            'birth_date': birth_details['date'],
            'birth_time': birth_details['time'],
            'dosha_summary': {
                'total_doshas': total_active,
                'high_severity': high_severity,
                'medium_severity': medium_severity,
                'low_severity': low_severity
            },
            'overall_dosha_impact': self._get_dosha_impact_rating(high_severity, medium_severity, low_severity),
            'doshas': doshas
        }
    
    def _get_dosha_impact_rating(self, high: int, medium: int, low: int) -> str:
        """Calculate overall dosha impact"""
        impact_score = (high * 3) + (medium * 2) + (low * 1)
        
        if impact_score == 0:
            return "No Significant Doshas"
        elif impact_score <= 2:
            return "Minimal Impact"
        elif impact_score <= 5:
            return "Moderate Impact - Remedies Recommended"
        elif impact_score <= 8:
            return "Significant Impact - Remedies Essential"
        else:
            return "High Impact - Strong Remedies Required"
    
    def _check_kala_sarpa_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Kala Sarpa Dosha"""
        try:
            result = dosha.kala_sarpa_dosha(planet_positions)
            return {
                'present': result[0] if isinstance(result, tuple) else result,
                'type': result[1] if isinstance(result, tuple) and len(result) > 1 else None,
                'description': 'All planets hemmed between Rahu and Ketu - causes obstacles',
                'severity': 'High' if result else 'None',
                'remedies': ['Rahu-Ketu puja', 'Naga Dosha remedies', 'Sarpa Samskara'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_manglik_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Manglik/Sevvay Dosha"""
        try:
            result = dosha.manglik_dosha(planet_positions)
            return {
                'present': bool(result),
                'houses': result if result else [],
                'description': 'Mars in 1st, 4th, 7th, 8th, or 12th house - affects marriage',
                'severity': 'High' if result else 'None',
                'remedies': ['Mangal puja', 'Hanuman worship', 'Red coral gemstone'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_pitru_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Pitru Dosha"""
        try:
            result = dosha.pitru_dosha(planet_positions)
            return {
                'present': bool(result),
                'description': 'Sun-Rahu or Sun-Saturn affliction - ancestral karma',
                'severity': 'Medium' if result else 'None',
                'remedies': ['Pitru Tarpan', 'Shraddha rituals', 'Charity'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_guru_chandala_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Guru Chandala Dosha"""
        try:
            result = dosha.guru_chandala_dosha(planet_positions)
            return {
                'present': bool(result),
                'description': 'Jupiter-Rahu conjunction - affects wisdom and judgment',
                'severity': 'Medium' if result else 'None',
                'remedies': ['Jupiter strengthening', 'Guru mantra', 'Yellow sapphire'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_ganda_moola_dosha(self, jd, place) -> Dict[str, Any]:
        """Check for Ganda Moola Dosha"""
        try:
            result = dosha.ganda_moola_dosha(jd, place)
            return {
                'present': bool(result),
                'description': 'Birth in Ganda Moola Nakshatras - requires shanti',
                'severity': 'Low' if result else 'None',
                'remedies': ['Ganda Moola Shanti', 'Nakshatra puja'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_kalathra_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Kalathra Dosha"""
        try:
            result = dosha.kalathra_dosha(planet_positions)
            return {
                'present': bool(result),
                'description': 'Affliction to 7th house - affects spouse and marriage',
                'severity': 'Medium' if result else 'None',
                'remedies': ['Venus strengthening', 'Kalathra puja', 'Diamond gemstone'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_ghata_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Ghata Dosha"""
        try:
            result = dosha.ghata_dosha(planet_positions)
            return {
                'present': bool(result),
                'description': 'Mars-Saturn conjunction - causes delays and obstacles',
                'severity': 'Low' if result else 'None',
                'remedies': ['Shani puja', 'Mangal puja', 'Blue sapphire caution'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}
    
    def _check_shrapit_dosha(self, planet_positions) -> Dict[str, Any]:
        """Check for Shrapit Dosha"""
        try:
            result = dosha.shrapit_dosha(planet_positions)
            return {
                'present': bool(result),
                'description': 'Saturn-Rahu conjunction - ancestral curses effect',
                'severity': 'High' if result else 'None',
                'remedies': ['Shani-Rahu puja', 'Saturn propitiation', 'Service to elderly'] if result else []
            }
        except:
            return {'present': False, 'error': 'Could not calculate'}