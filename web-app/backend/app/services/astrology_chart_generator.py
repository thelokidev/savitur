"""
Astrology Chart Generator Service
A comprehensive wrapper for the JyotiChart library to generate Vedic astrology charts.

This module provides a robust, production-ready implementation for generating
both North Indian and South Indian style Vedic astrology charts.
"""

import os
import sys
import tempfile
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Add jyotichart to path
JYOTICHART_PATH = Path(__file__).parent.parent.parent / 'temp_jyotichart'
if str(JYOTICHART_PATH) not in sys.path:
    sys.path.insert(0, str(JYOTICHART_PATH))

try:
    import jyotichart as chart
except ImportError:
    raise ImportError(
        "JyotiChart library not found. Please ensure it's installed in the correct location."
    )


class AstrologyChartGenerator:
    """
    Comprehensive wrapper class for JyotiChart library.
    
    Provides simplified interface for generating Vedic astrology charts
    with full validation, error handling, and customization support.
    """
    
    # Planet Constants Mapping
    PLANET_CONSTANTS = {
        'Sun': chart.SUN,
        'Moon': chart.MOON,
        'Mars': chart.MARS,
        'Mercury': chart.MERCURY,
        'Jupiter': chart.JUPITER,
        'Venus': chart.VENUS,
        'Saturn': chart.SATURN,
        'Rahu': chart.RAHU,
        'Ketu': chart.KETU
    }
    
    # Valid Zodiac Signs (case-sensitive as per JyotiChart requirements)
    ZODIAC_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Saggitarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    # Default Aspect Symbols
    DEFAULT_ASPECT_SYMBOLS = {
        'Sun': '☉',
        'Moon': '☾',
        'Mars': '♂',
        'Mercury': '☿',
        'Jupiter': '♃',
        'Venus': '♀',
        'Saturn': '♄',
        'Rahu': '☊',
        'Ketu': '☋'
    }
    
    # Valid Chart Types
    CHART_TYPES = ['North', 'South']
    
    def __init__(self):
        """Initialize the Astrology Chart Generator."""
        self.last_error = None
    
    def validate_input_data(self, birth_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate all input parameters for chart generation.
        
        Args:
            birth_data: Dictionary containing all chart generation parameters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate required top-level keys
        required_keys = ['name', 'chart_type', 'chart_name', 'ascendant_sign', 'planets']
        for key in required_keys:
            if key not in birth_data:
                return False, f"Missing required field: {key}"
        
        # Validate chart type
        if birth_data['chart_type'] not in self.CHART_TYPES:
            return False, f"Invalid chart_type. Must be one of: {', '.join(self.CHART_TYPES)}"
        
        # Validate ascendant sign
        if birth_data['ascendant_sign'] not in self.ZODIAC_SIGNS:
            return False, (
                f"Invalid ascendant_sign: '{birth_data['ascendant_sign']}'. "
                f"Must be one of: {', '.join(self.ZODIAC_SIGNS)} (case-sensitive)"
            )
        
        # Validate planets
        if not isinstance(birth_data['planets'], list):
            return False, "planets must be a list"
        
        for idx, planet in enumerate(birth_data['planets']):
            # Validate planet structure
            if not isinstance(planet, dict):
                return False, f"Planet at index {idx} must be a dictionary"
            
            # Validate required planet fields
            required_planet_keys = ['name', 'symbol', 'house']
            for key in required_planet_keys:
                if key not in planet:
                    return False, f"Planet at index {idx} missing required field: {key}"
            
            # Validate planet name
            if planet['name'] not in self.PLANET_CONSTANTS:
                return False, (
                    f"Invalid planet name: '{planet['name']}'. "
                    f"Must be one of: {', '.join(self.PLANET_CONSTANTS.keys())}"
                )
            
            # Validate house number
            house = planet['house']
            if not isinstance(house, int) or house < 1 or house > 12:
                return False, f"Planet '{planet['name']}' has invalid house: {house}. Must be 1-12"
            
            # Validate symbol is string
            if not isinstance(planet['symbol'], str):
                return False, f"Planet '{planet['name']}' symbol must be a string"
        
        # Validate output configuration if provided
        if 'output' in birth_data:
            output = birth_data['output']
            if 'location' in output:
                location = Path(output['location'])
                if not location.exists():
                    return False, f"Output location does not exist: {output['location']}"
                if not os.access(output['location'], os.W_OK):
                    return False, f"No write permission for output location: {output['location']}"
            
            if 'filename' not in output:
                return False, "Output configuration missing 'filename'"
        
        return True, None
    
    def create_chart_object(
        self,
        chart_type: str,
        chart_name: str,
        person_name: str,
        is_full_chart: bool = False
    ):
        """
        Create a JyotiChart chart object.

        Args:
            chart_type: 'North' or 'South'
            chart_name: Name/identifier for the chart (e.g., 'Lagna', 'Navamsa')
            person_name: Name of the person
            is_full_chart: Whether all planets must be provided

        Returns:
            Chart object (NorthChart or SouthChart)
        """
        try:
            if chart_type == 'North':
                chart_obj = chart.NorthChart(chart_name, person_name, IsFullChart=is_full_chart)
            elif chart_type == 'South':
                chart_obj = chart.SouthChart(chart_name, person_name, IsFullChart=is_full_chart)
            else:
                raise ValueError(f"Invalid chart_type: {chart_type}")

            # Reset planet states (workaround for class-level planet dictionary)
            self._reset_planet_states(chart_obj)

            return chart_obj
        except Exception as e:
            self.last_error = f"Failed to create chart object: {str(e)}"
            raise

    def _reset_planet_states(self, chart_obj):
        """
        Reset planet states in chart object.

        Workaround for JyotiChart's class-level planet dictionary
        that persists state between instances.
        """
        for planet_name in self.PLANET_CONSTANTS.keys():
            if hasattr(chart_obj, 'planets') and planet_name in chart_obj.planets:
                chart_obj.planets[planet_name]['isUpdated'] = False
                chart_obj.planets[planet_name]['symbol'] = ''
                chart_obj.planets[planet_name]['house_num'] = 0

    def _read_svg_file(self, svg_path: str) -> str:
        """
        Read SVG file with proper encoding handling.

        Tries multiple encodings to handle different file formats.

        Args:
            svg_path: Path to SVG file

        Returns:
            SVG content as string
        """
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(svg_path, 'r', encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, LookupError):
                continue

        # If all encodings fail, try binary mode and decode with errors='ignore'
        try:
            with open(svg_path, 'rb') as f:
                content = f.read()
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            raise IOError(f"Failed to read SVG file {svg_path}: {str(e)}")
    
    def add_planets_to_chart(
        self, 
        chart_obj, 
        planets_data: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """
        Add all planets to the chart with validation.
        
        Args:
            chart_obj: JyotiChart chart object
            planets_data: List of planet dictionaries
            
        Returns:
            Tuple of (success, list_of_errors)
        """
        errors = []
        
        for planet in planets_data:
            try:
                planet_name = planet['name']
                planet_constant = self.PLANET_CONSTANTS[planet_name]
                symbol = planet['symbol']
                house = planet['house']
                
                # Optional parameters
                retrograde = planet.get('retrograde', False)
                color = planet.get('color', 'white')
                aspect_symbol = planet.get(
                    'aspect_symbol', 
                    self.DEFAULT_ASPECT_SYMBOLS.get(planet_name, 'Default')
                )
                
                # Add planet to chart
                result = chart_obj.add_planet(
                    planet_constant,
                    symbol,
                    house,
                    retrograde=retrograde,
                    aspectsymbol=aspect_symbol,
                    colour=color
                )
                
                # Check if addition was successful
                if result != "Success":
                    errors.append(f"Failed to add {planet_name}: {result}")
                    
            except Exception as e:
                errors.append(f"Error adding planet {planet.get('name', 'Unknown')}: {str(e)}")
        
        return len(errors) == 0, errors
    
    def configure_chart_appearance(
        self,
        chart_obj,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Apply visual configurations to the chart.

        Args:
            chart_obj: JyotiChart chart object
            config: Configuration dictionary with appearance settings
        """
        if config is None:
            config = {}

        # Extract configuration with defaults
        show_aspects = config.get('show_aspects', False)
        background_color = config.get('background_color', 'black')
        line_color = config.get('line_color', 'yellow')
        sign_color = config.get('sign_color', 'pink')
        house_colors = config.get('house_colors', ['black'] * 12)

        # Ensure house_colors has exactly 12 elements
        if len(house_colors) != 12:
            house_colors = house_colors[:12] + ['black'] * (12 - len(house_colors))

        # Apply configuration
        # Detect chart type by class name
        try:
            chart_class_name = chart_obj.__class__.__name__

            if chart_class_name == 'SouthChart':
                # South Indian chart uses clr_Asc and clr_inbox
                chart_obj.updatechartcfg(
                    aspect=show_aspects,
                    clr_background=background_color,
                    clr_line=line_color,
                    clr_Asc=sign_color,
                    clr_houses=house_colors
                )
            else:
                # North Indian chart uses clr_sign
                chart_obj.updatechartcfg(
                    aspect=show_aspects,
                    clr_background=background_color,
                    clr_line=line_color,
                    clr_sign=sign_color,
                    clr_houses=house_colors
                )
        except Exception as e:
            self.last_error = f"Failed to configure chart appearance: {str(e)}"
            raise

    def generate_chart_svg(self, birth_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Complete chart generation pipeline.

        Args:
            birth_data: Complete birth data dictionary

        Returns:
            Tuple of (success, svg_content_or_filepath, error_message)
        """
        try:
            # Step 1: Validate input data
            is_valid, error_msg = self.validate_input_data(birth_data)
            if not is_valid:
                return False, None, error_msg

            # Step 2: Create chart object
            chart_obj = self.create_chart_object(
                chart_type=birth_data['chart_type'],
                chart_name=birth_data['chart_name'],
                person_name=birth_data['name'],
                is_full_chart=birth_data.get('is_full_chart', False)
            )

            # Step 3: Set ascendant sign
            result = chart_obj.set_ascendantsign(birth_data['ascendant_sign'])
            if result != "Success":
                return False, None, f"Failed to set ascendant: {result}"

            # Step 4: Add planets
            success, errors = self.add_planets_to_chart(chart_obj, birth_data['planets'])
            if not success:
                return False, None, f"Planet addition errors: {'; '.join(errors)}"

            # Step 5: Configure appearance
            if 'chart_config' in birth_data:
                self.configure_chart_appearance(chart_obj, birth_data['chart_config'])

            # Step 6: Generate SVG
            output_config = birth_data.get('output', {})

            if 'location' in output_config and 'filename' in output_config:
                # Save to specified location
                location = output_config['location']
                filename = output_config['filename']

                chart_obj.draw(location, filename)

                svg_path = os.path.join(location, f"{filename}.svg")

                # Read and return SVG content (try different encodings)
                svg_content = self._read_svg_file(svg_path)

                return True, svg_content, None
            else:
                # Use temporary directory
                with tempfile.TemporaryDirectory() as tmpdir:
                    filename = f"chart_{birth_data['chart_name']}"
                    chart_obj.draw(tmpdir, filename)

                    svg_path = os.path.join(tmpdir, f"{filename}.svg")

                    # Read and return SVG content (try different encodings)
                    svg_content = self._read_svg_file(svg_path)

                return True, svg_content, None

        except Exception as e:
            error_msg = f"Chart generation failed: {str(e)}"
            self.last_error = error_msg
            return False, None, error_msg

    def generate_chart_to_file(
        self,
        birth_data: Dict[str, Any],
        output_path: str,
        filename: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Generate chart and save to specific file location.

        Args:
            birth_data: Birth data dictionary
            output_path: Directory path for output
            filename: Filename without extension

        Returns:
            Tuple of (success, error_message)
        """
        # Add output configuration to birth_data
        birth_data['output'] = {
            'location': output_path,
            'filename': filename
        }

        success, svg_content, error = self.generate_chart_svg(birth_data)

        if success:
            return True, None
        else:
            return False, error

    @staticmethod
    def get_house_from_rasi(planet_rasi: str, ascendant_rasi: str) -> int:
        """
        Calculate house number from rasi names.

        Args:
            planet_rasi: Rasi name where planet is located
            ascendant_rasi: Ascendant rasi name

        Returns:
            House number (1-12)
        """
        rasi_list = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]

        try:
            planet_idx = rasi_list.index(planet_rasi)
            asc_idx = rasi_list.index(ascendant_rasi)
            house = ((planet_idx - asc_idx) % 12) + 1
            return house
        except ValueError:
            return 1  # Default to first house if error

    @staticmethod
    def create_sample_birth_data(
        name: str = "Sample Person",
        chart_type: str = "North",
        chart_name: str = "Lagna"
    ) -> Dict[str, Any]:
        """
        Create sample birth data for testing.

        Args:
            name: Person's name
            chart_type: 'North' or 'South'
            chart_name: Chart identifier

        Returns:
            Sample birth data dictionary
        """
        return {
            'name': name,
            'chart_type': chart_type,
            'chart_name': chart_name,
            'ascendant_sign': 'Capricorn',
            'planets': [
                {'name': 'Sun', 'symbol': 'Su', 'house': 9, 'color': 'orange'},
                {'name': 'Moon', 'symbol': 'Mo', 'house': 9, 'color': 'white'},
                {'name': 'Mars', 'symbol': 'Ma', 'house': 10, 'color': 'red'},
                {'name': 'Mercury', 'symbol': 'Me', 'house': 9, 'color': 'green'},
                {'name': 'Jupiter', 'symbol': 'Ju', 'house': 8, 'color': 'yellow', 'retrograde': True},
                {'name': 'Venus', 'symbol': 'Ve', 'house': 8, 'color': 'pink'},
                {'name': 'Saturn', 'symbol': 'Sa', 'house': 1, 'color': 'blue'},
                {'name': 'Rahu', 'symbol': 'Ra', 'house': 12, 'color': 'purple'},
                {'name': 'Ketu', 'symbol': 'Ke', 'house': 6, 'color': 'brown'}
            ],
            'chart_config': {
                'show_aspects': False,
                'background_color': 'black',
                'line_color': 'yellow',
                'sign_color': 'pink',
                'house_colors': ['black'] * 12
            }
        }

