"""
Astrology Chart Examples and Usage Demonstrations

This module provides comprehensive examples of using the AstrologyChartGenerator
for various chart types and scenarios.
"""

from typing import Dict, Any
from app.services.astrology_chart_generator import AstrologyChartGenerator


class ChartExamples:
    """Collection of example chart configurations and usage patterns."""
    
    @staticmethod
    def lagna_chart_example() -> Dict[str, Any]:
        """
        Example: Lagna Chart (Birth Chart / D1)
        
        The most important chart in Vedic astrology showing planetary positions
        at the time of birth.
        """
        return {
            'name': 'Shyam Bhat',
            'chart_type': 'North',
            'chart_name': 'Lagna (D1)',
            'ascendant_sign': 'Capricorn',
            'is_full_chart': True,
            'planets': [
                {
                    'name': 'Sun',
                    'symbol': 'Su',
                    'house': 9,
                    'retrograde': False,
                    'color': '#ff6b35',
                    'aspect_symbol': '☉'
                },
                {
                    'name': 'Moon',
                    'symbol': 'Mo',
                    'house': 9,
                    'retrograde': False,
                    'color': '#e0e0e0',
                    'aspect_symbol': '☾'
                },
                {
                    'name': 'Mars',
                    'symbol': 'Ma',
                    'house': 10,
                    'retrograde': False,
                    'color': '#ef233c',
                    'aspect_symbol': '♂'
                },
                {
                    'name': 'Mercury',
                    'symbol': 'Me',
                    'house': 9,
                    'retrograde': False,
                    'color': '#06ffa5',
                    'aspect_symbol': '☿'
                },
                {
                    'name': 'Jupiter',
                    'symbol': 'Ju',
                    'house': 8,
                    'retrograde': True,  # Retrograde Jupiter
                    'color': '#ffd60a',
                    'aspect_symbol': '♃'
                },
                {
                    'name': 'Venus',
                    'symbol': 'Ve',
                    'house': 8,
                    'retrograde': False,
                    'color': '#ff006e',
                    'aspect_symbol': '♀'
                },
                {
                    'name': 'Saturn',
                    'symbol': 'Sa',
                    'house': 1,
                    'retrograde': False,
                    'color': '#4361ee',
                    'aspect_symbol': '♄'
                },
                {
                    'name': 'Rahu',
                    'symbol': 'Ra',
                    'house': 12,
                    'retrograde': True,  # Always retrograde
                    'color': '#9d4edd',
                    'aspect_symbol': '☊'
                },
                {
                    'name': 'Ketu',
                    'symbol': 'Ke',
                    'house': 6,
                    'retrograde': True,  # Always retrograde
                    'color': '#fb5607',
                    'aspect_symbol': '☋'
                }
            ],
            'chart_config': {
                'show_aspects': False,
                'background_color': '#1a1a1a',
                'line_color': '#ffd60a',
                'sign_color': '#06ffa5',
                'house_colors': ['black'] * 12
            }
        }
    
    @staticmethod
    def navamsa_chart_example() -> Dict[str, Any]:
        """
        Example: Navamsa Chart (D9)
        
        The second most important divisional chart, showing marriage,
        dharma, and inner strength.
        """
        return {
            'name': 'Deepa Saravi',
            'chart_type': 'South',
            'chart_name': 'Navamsa (D9)',
            'ascendant_sign': 'Aries',
            'is_full_chart': False,  # Partial chart
            'planets': [
                {'name': 'Sun', 'symbol': 'Su', 'house': 5, 'color': '#ff6b35'},
                {'name': 'Moon', 'symbol': 'Mo', 'house': 7, 'color': '#e0e0e0'},
                {'name': 'Venus', 'symbol': 'Ve', 'house': 7, 'color': '#ff006e'},
                {'name': 'Jupiter', 'symbol': 'Ju', 'house': 9, 'color': '#ffd60a'}
            ],
            'chart_config': {
                'show_aspects': False,
                'background_color': '#1a1a1a',
                'line_color': '#ffd60a',
                'sign_color': '#ff006e',
                'house_colors': ['black'] * 12
            }
        }
    
    @staticmethod
    def transit_chart_example() -> Dict[str, Any]:
        """
        Example: Transit Chart (Gochara)
        
        Shows current planetary positions for prediction purposes.
        """
        return {
            'name': 'Current Transits',
            'chart_type': 'North',
            'chart_name': 'Transit',
            'ascendant_sign': 'Leo',
            'is_full_chart': True,
            'planets': [
                {'name': 'Sun', 'symbol': 'Su', 'house': 6, 'color': '#ff6b35'},
                {'name': 'Moon', 'symbol': 'Mo', 'house': 3, 'color': '#e0e0e0'},
                {'name': 'Mars', 'symbol': 'Ma', 'house': 2, 'color': '#ef233c'},
                {'name': 'Mercury', 'symbol': 'Me', 'house': 6, 'color': '#06ffa5'},
                {'name': 'Jupiter', 'symbol': 'Ju', 'house': 10, 'color': '#ffd60a'},
                {'name': 'Venus', 'symbol': 'Ve', 'house': 5, 'color': '#ff006e'},
                {'name': 'Saturn', 'symbol': 'Sa', 'house': 7, 'color': '#4361ee'},
                {'name': 'Rahu', 'symbol': 'Ra', 'house': 8, 'color': '#9d4edd'},
                {'name': 'Ketu', 'symbol': 'Ke', 'house': 2, 'color': '#fb5607'}
            ],
            'chart_config': {
                'show_aspects': True,  # Show aspects for transit analysis
                'background_color': '#1a1a1a',
                'line_color': '#06ffa5',
                'sign_color': '#ffd60a',
                'house_colors': ['black'] * 12
            }
        }
    
    @staticmethod
    def custom_house_colors_example() -> Dict[str, Any]:
        """
        Example: Chart with Custom House Colors
        
        Demonstrates coloring houses based on their nature:
        - Trikona (1, 5, 9): Green (beneficial)
        - Dusthana (6, 8, 12): Red (challenging)
        - Kendra (1, 4, 7, 10): Blue (angular/powerful)
        """
        house_colors = ['black'] * 12
        
        # Trikona houses (1, 5, 9) - Green
        house_colors[0] = '#2d6a4f'   # 1st house
        house_colors[4] = '#2d6a4f'   # 5th house
        house_colors[8] = '#2d6a4f'   # 9th house
        
        # Dusthana houses (6, 8, 12) - Red
        house_colors[5] = '#6a040f'   # 6th house
        house_colors[7] = '#6a040f'   # 8th house
        house_colors[11] = '#6a040f'  # 12th house
        
        # Kendra houses (4, 7, 10) - Blue (1st already colored)
        house_colors[3] = '#1e3a8a'   # 4th house
        house_colors[6] = '#1e3a8a'   # 7th house
        house_colors[9] = '#1e3a8a'   # 10th house
        
        return {
            'name': 'Custom Colors',
            'chart_type': 'North',
            'chart_name': 'Lagna',
            'ascendant_sign': 'Gemini',
            'is_full_chart': True,
            'planets': [
                {'name': 'Sun', 'symbol': 'Su', 'house': 1, 'color': 'white'},
                {'name': 'Moon', 'symbol': 'Mo', 'house': 4, 'color': 'white'},
                {'name': 'Mars', 'symbol': 'Ma', 'house': 5, 'color': 'white'},
                {'name': 'Mercury', 'symbol': 'Me', 'house': 1, 'color': 'white'},
                {'name': 'Jupiter', 'symbol': 'Ju', 'house': 9, 'color': 'white'},
                {'name': 'Venus', 'symbol': 'Ve', 'house': 2, 'color': 'white'},
                {'name': 'Saturn', 'symbol': 'Sa', 'house': 8, 'color': 'white'},
                {'name': 'Rahu', 'symbol': 'Ra', 'house': 11, 'color': 'white'},
                {'name': 'Ketu', 'symbol': 'Ke', 'house': 5, 'color': 'white'}
            ],
            'chart_config': {
                'show_aspects': False,
                'background_color': 'black',
                'line_color': 'yellow',
                'sign_color': 'pink',
                'house_colors': house_colors
            }
        }


def demonstrate_basic_usage():
    """Demonstrate basic usage of the AstrologyChartGenerator."""
    
    print("=" * 80)
    print("ASTROLOGY CHART GENERATOR - BASIC USAGE EXAMPLES")
    print("=" * 80)
    
    # Initialize generator
    generator = AstrologyChartGenerator()
    
    # Example 1: Generate Lagna Chart (North Indian)
    print("\n1. Generating Lagna Chart (North Indian Style)...")
    lagna_data = ChartExamples.lagna_chart_example()
    
    success, svg_content, error = generator.generate_chart_svg(lagna_data)
    
    if success:
        print(f"   ✓ Success! Generated SVG ({len(svg_content)} bytes)")
        print(f"   Chart for: {lagna_data['name']}")
        print(f"   Ascendant: {lagna_data['ascendant_sign']}")
    else:
        print(f"   ✗ Error: {error}")
    
    # Example 2: Generate Navamsa Chart (South Indian)
    print("\n2. Generating Navamsa Chart (South Indian Style)...")
    navamsa_data = ChartExamples.navamsa_chart_example()
    
    success, svg_content, error = generator.generate_chart_svg(navamsa_data)
    
    if success:
        print(f"   ✓ Success! Generated SVG ({len(svg_content)} bytes)")
        print(f"   Chart for: {navamsa_data['name']}")
        print(f"   Type: {navamsa_data['chart_name']}")
    else:
        print(f"   ✗ Error: {error}")
    
    # Example 3: Save chart to file
    print("\n3. Saving Transit Chart to file...")
    transit_data = ChartExamples.transit_chart_example()
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        success, error = generator.generate_chart_to_file(
            transit_data,
            tmpdir,
            "transit_chart"
        )
        
        if success:
            print(f"   ✓ Success! Chart saved to: {tmpdir}/transit_chart.svg")
        else:
            print(f"   ✗ Error: {error}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_basic_usage()

