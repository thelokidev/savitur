"""
JyotiChart Integration Service

Bridges the gap between our existing chart calculation service and the
JyotiChart rendering library. Converts our chart data format to JyotiChart format.
"""

from typing import Dict, Any, List, Optional
from app.services.astrology_chart_generator import AstrologyChartGenerator


class JyotiChartIntegration:
    """
    Integration layer between our chart service and JyotiChart library.
    
    Converts our internal chart data format to JyotiChart-compatible format
    and handles chart generation.
    """
    
    # Mapping of our rasi names to JyotiChart zodiac signs
    RASI_TO_ZODIAC = {
        'Aries': 'Aries',
        'Taurus': 'Taurus',
        'Gemini': 'Gemini',
        'Cancer': 'Cancer',
        'Leo': 'Leo',
        'Virgo': 'Virgo',
        'Libra': 'Libra',
        'Scorpio': 'Scorpio',
        'Sagittarius': 'Saggitarius',  # Note: JyotiChart uses 'Saggitarius'
        'Capricorn': 'Capricorn',
        'Aquarius': 'Aquarius',
        'Pisces': 'Pisces'
    }
    
    # Planet symbol mapping
    PLANET_SYMBOLS = {
        'Sun': 'Su',
        'Moon': 'Mo',
        'Mars': 'Ma',
        'Mercury': 'Me',
        'Jupiter': 'Ju',
        'Venus': 'Ve',
        'Saturn': 'Sa',
        'Rahu': 'Ra',
        'Ketu': 'Ke'
    }
    
    # Planet colors for visual appeal
    PLANET_COLORS = {
        'Sun': '#ff6b35',
        'Moon': '#e0e0e0',
        'Mars': '#ef233c',
        'Mercury': '#06ffa5',
        'Jupiter': '#ffd60a',
        'Venus': '#ff006e',
        'Saturn': '#4361ee',
        'Rahu': '#9d4edd',
        'Ketu': '#fb5607'
    }
    
    def __init__(self):
        """Initialize the integration service."""
        self.generator = AstrologyChartGenerator()
    
    def convert_chart_data_to_jyoti_format(
        self,
        chart_data: Dict[str, Any],
        chart_type: str = 'North',
        chart_name: str = 'D1',
        person_name: str = 'Native'
    ) -> Dict[str, Any]:
        """
        Convert our internal chart data format to JyotiChart format.
        
        Args:
            chart_data: Our internal chart data with planets and ascendant
            chart_type: 'North' or 'South'
            chart_name: Name of the chart (e.g., 'D1', 'D9', etc.)
            person_name: Name of the person
            
        Returns:
            JyotiChart-compatible birth data dictionary
        """
        # Extract ascendant
        ascendant = chart_data.get('ascendant', {})
        ascendant_rasi = ascendant.get('rasi_name', 'Aries')
        
        # Convert to JyotiChart zodiac sign format
        ascendant_sign = self.RASI_TO_ZODIAC.get(ascendant_rasi, 'Aries')
        
        # Convert planets
        planets_list = []
        for planet in chart_data.get('planets', []):
            planet_name = planet.get('name', '')
            planet_rasi = planet.get('rasi_name', 'Aries')
            
            # Skip if planet name not recognized
            if planet_name not in self.PLANET_SYMBOLS:
                continue
            
            # Calculate house number from rasi
            house_num = self._calculate_house_number(planet_rasi, ascendant_rasi)
            
            # Check if retrograde
            is_retrograde = planet.get('is_retrograde', False)
            
            # Rahu and Ketu are always retrograde
            if planet_name in ['Rahu', 'Ketu']:
                is_retrograde = True
            
            planet_entry = {
                'name': planet_name,
                'symbol': self.PLANET_SYMBOLS[planet_name],
                'house': house_num,
                'retrograde': is_retrograde,
                'color': self.PLANET_COLORS.get(planet_name, 'white')
            }
            
            planets_list.append(planet_entry)
        
        # Build JyotiChart birth data
        jyoti_data = {
            'name': person_name,
            'chart_type': chart_type,
            'chart_name': chart_name,
            'ascendant_sign': ascendant_sign,
            'is_full_chart': False,  # Allow partial charts
            'planets': planets_list,
            'chart_config': {
                'show_aspects': False,
                'background_color': '#1a1a1a',
                'line_color': '#ffd60a',
                'sign_color': '#06ffa5',
                'house_colors': ['black'] * 12
            }
        }
        
        return jyoti_data
    
    def _calculate_house_number(self, planet_rasi: str, ascendant_rasi: str) -> int:
        """
        Calculate house number from rasi names.
        
        Args:
            planet_rasi: Rasi where planet is located
            ascendant_rasi: Ascendant rasi
            
        Returns:
            House number (1-12)
        """
        rasi_order = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        try:
            planet_idx = rasi_order.index(planet_rasi)
            asc_idx = rasi_order.index(ascendant_rasi)
            house = ((planet_idx - asc_idx) % 12) + 1
            return house
        except ValueError:
            # If rasi not found, default to house 1
            return 1
    
    def generate_chart_svg(
        self,
        chart_data: Dict[str, Any],
        chart_style: str = 'north',
        chart_name: str = 'D1',
        person_name: str = 'Native',
        custom_config: Optional[Dict[str, Any]] = None
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Generate chart SVG from our internal chart data.
        
        Args:
            chart_data: Our internal chart data
            chart_style: 'north', 'south', or 'east'
            chart_name: Chart identifier
            person_name: Person's name
            custom_config: Optional custom chart configuration
            
        Returns:
            Tuple of (success, svg_content, error_message)
        """
        # Map chart style to JyotiChart type
        chart_type_map = {
            'north': 'North',
            'south': 'South',
            'east': 'South'  # Use South for East (JyotiChart doesn't have East)
        }
        
        chart_type = chart_type_map.get(chart_style.lower(), 'North')
        
        # Convert to JyotiChart format
        jyoti_data = self.convert_chart_data_to_jyoti_format(
            chart_data,
            chart_type=chart_type,
            chart_name=chart_name,
            person_name=person_name
        )
        
        # Apply custom configuration if provided
        if custom_config:
            jyoti_data['chart_config'].update(custom_config)
        
        # Generate chart
        return self.generator.generate_chart_svg(jyoti_data)
    
    def generate_divisional_chart(
        self,
        chart_data: Dict[str, Any],
        division: str,
        chart_style: str = 'north',
        person_name: str = 'Native'
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Generate divisional chart (Varga chart).
        
        Args:
            chart_data: Chart data for the specific division
            division: Division name (e.g., 'D1', 'D9', 'D10')
            chart_style: Chart rendering style
            person_name: Person's name
            
        Returns:
            Tuple of (success, svg_content, error_message)
        """
        division_names = {
            'D1': 'Rasi (D1)',
            'D2': 'Hora (D2)',
            'D3': 'Drekkana (D3)',
            'D4': 'Chaturthamsa (D4)',
            'D7': 'Saptamsa (D7)',
            'D9': 'Navamsa (D9)',
            'D10': 'Dasamsa (D10)',
            'D12': 'Dwadasamsa (D12)',
            'D16': 'Shodasamsa (D16)',
            'D20': 'Vimsamsa (D20)',
            'D24': 'Chaturvimsamsa (D24)',
            'D27': 'Nakshatramsa (D27)',
            'D30': 'Trimsamsa (D30)',
            'D40': 'Khavedamsa (D40)',
            'D45': 'Akshavedamsa (D45)',
            'D60': 'Shashtiamsa (D60)'
        }
        
        chart_name = division_names.get(division, division)
        
        return self.generate_chart_svg(
            chart_data,
            chart_style=chart_style,
            chart_name=chart_name,
            person_name=person_name
        )
    
    def generate_comparison_charts(
        self,
        chart_data_1: Dict[str, Any],
        chart_data_2: Dict[str, Any],
        person_name_1: str = 'Person 1',
        person_name_2: str = 'Person 2',
        chart_style: str = 'north'
    ) -> tuple[bool, Optional[List[str]], Optional[str]]:
        """
        Generate two charts for comparison (e.g., synastry).
        
        Args:
            chart_data_1: First person's chart data
            chart_data_2: Second person's chart data
            person_name_1: First person's name
            person_name_2: Second person's name
            chart_style: Chart rendering style
            
        Returns:
            Tuple of (success, [svg1, svg2], error_message)
        """
        # Generate first chart
        success1, svg1, error1 = self.generate_chart_svg(
            chart_data_1,
            chart_style=chart_style,
            chart_name='Chart 1',
            person_name=person_name_1
        )
        
        if not success1:
            return False, None, f"Chart 1 error: {error1}"
        
        # Generate second chart
        success2, svg2, error2 = self.generate_chart_svg(
            chart_data_2,
            chart_style=chart_style,
            chart_name='Chart 2',
            person_name=person_name_2
        )
        
        if not success2:
            return False, None, f"Chart 2 error: {error2}"
        
        return True, [svg1, svg2], None
    
    def get_supported_chart_types(self) -> List[str]:
        """Get list of supported chart types."""
        return ['north', 'south']
    
    def get_supported_divisions(self) -> List[str]:
        """Get list of supported divisional charts."""
        return [
            'D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12',
            'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'
        ]

