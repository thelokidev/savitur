"""
Test script for JyotiChart integration

This script tests the complete JyotiChart integration pipeline:
1. Chart data generation
2. Format conversion
3. SVG generation
"""

import sys
from pathlib import Path

# Add app to path
app_path = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_path))

from services.astrology_chart_generator import AstrologyChartGenerator
from services.chart_examples import ChartExamples
from services.jyotichart_integration import JyotiChartIntegration


def test_basic_chart_generation():
    """Test basic chart generation with AstrologyChartGenerator."""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Chart Generation")
    print("=" * 80)
    
    generator = AstrologyChartGenerator()
    
    # Test with sample data
    sample_data = generator.create_sample_birth_data(
        name="Test Person",
        chart_type="North",
        chart_name="Test Chart"
    )
    
    print("\n📋 Input Data:")
    print(f"   Name: {sample_data['name']}")
    print(f"   Chart Type: {sample_data['chart_type']}")
    print(f"   Ascendant: {sample_data['ascendant_sign']}")
    print(f"   Planets: {len(sample_data['planets'])}")
    
    # Validate
    is_valid, error = generator.validate_input_data(sample_data)
    print(f"\n✓ Validation: {'PASSED' if is_valid else 'FAILED'}")
    if error:
        print(f"   Error: {error}")
        return False
    
    # Generate
    print("\n🎨 Generating chart...")
    success, svg_content, error = generator.generate_chart_svg(sample_data)
    
    if success:
        print(f"✓ SUCCESS! Generated SVG ({len(svg_content)} bytes)")
        
        # Save to file for inspection
        output_file = Path(__file__).parent / "test_output_basic.svg"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"   Saved to: {output_file}")
        return True
    else:
        print(f"✗ FAILED: {error}")
        return False


def test_chart_examples():
    """Test predefined chart examples."""
    print("\n" + "=" * 80)
    print("TEST 2: Chart Examples")
    print("=" * 80)
    
    generator = AstrologyChartGenerator()
    examples = [
        ("Lagna Chart", ChartExamples.lagna_chart_example()),
        ("Navamsa Chart", ChartExamples.navamsa_chart_example()),
        ("Transit Chart", ChartExamples.transit_chart_example()),
        ("Custom Colors", ChartExamples.custom_house_colors_example())
    ]
    
    results = []
    
    for name, example_data in examples:
        print(f"\n📊 Testing: {name}")
        print(f"   Type: {example_data['chart_type']}")
        print(f"   Ascendant: {example_data['ascendant_sign']}")
        
        success, svg_content, error = generator.generate_chart_svg(example_data)
        
        if success:
            print(f"   ✓ SUCCESS ({len(svg_content)} bytes)")
            
            # Save to file
            filename = name.lower().replace(' ', '_').replace('(', '').replace(')', '')
            output_file = Path(__file__).parent / f"test_output_{filename}.svg"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"   Saved to: {output_file}")
            results.append(True)
        else:
            print(f"   ✗ FAILED: {error}")
            results.append(False)
    
    success_count = sum(results)
    total_count = len(results)
    print(f"\n📈 Results: {success_count}/{total_count} tests passed")
    
    return all(results)


def test_integration_service():
    """Test JyotiChartIntegration service."""
    print("\n" + "=" * 80)
    print("TEST 3: Integration Service")
    print("=" * 80)
    
    integration = JyotiChartIntegration()
    
    # Create mock chart data (simulating our internal format)
    mock_chart_data = {
        'ascendant': {
            'rasi_name': 'Capricorn',
            'degree': 15.5
        },
        'planets': [
            {'name': 'Sun', 'rasi_name': 'Virgo', 'degree': 10.5, 'is_retrograde': False},
            {'name': 'Moon', 'rasi_name': 'Virgo', 'degree': 20.3, 'is_retrograde': False},
            {'name': 'Mars', 'rasi_name': 'Libra', 'degree': 5.2, 'is_retrograde': False},
            {'name': 'Mercury', 'rasi_name': 'Virgo', 'degree': 15.8, 'is_retrograde': False},
            {'name': 'Jupiter', 'rasi_name': 'Leo', 'degree': 25.1, 'is_retrograde': True},
            {'name': 'Venus', 'rasi_name': 'Leo', 'degree': 12.4, 'is_retrograde': False},
            {'name': 'Saturn', 'rasi_name': 'Capricorn', 'degree': 8.9, 'is_retrograde': False},
            {'name': 'Rahu', 'rasi_name': 'Sagittarius', 'degree': 18.7, 'is_retrograde': True},
            {'name': 'Ketu', 'rasi_name': 'Gemini', 'degree': 18.7, 'is_retrograde': True}
        ]
    }
    
    print("\n📋 Mock Chart Data:")
    print(f"   Ascendant: {mock_chart_data['ascendant']['rasi_name']}")
    print(f"   Planets: {len(mock_chart_data['planets'])}")
    
    # Test conversion
    print("\n🔄 Converting to JyotiChart format...")
    jyoti_data = integration.convert_chart_data_to_jyoti_format(
        mock_chart_data,
        chart_type='North',
        chart_name='D1',
        person_name='Integration Test'
    )
    
    print(f"   ✓ Converted successfully")
    print(f"   Ascendant Sign: {jyoti_data['ascendant_sign']}")
    print(f"   Planets: {len(jyoti_data['planets'])}")
    
    # Test generation
    print("\n🎨 Generating chart from converted data...")
    success, svg_content, error = integration.generate_chart_svg(
        mock_chart_data,
        chart_style='north',
        chart_name='D1',
        person_name='Integration Test'
    )
    
    if success:
        print(f"   ✓ SUCCESS ({len(svg_content)} bytes)")
        
        # Save to file
        output_file = Path(__file__).parent / "test_output_integration.svg"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"   Saved to: {output_file}")
        return True
    else:
        print(f"   ✗ FAILED: {error}")
        return False


def test_validation():
    """Test input validation."""
    print("\n" + "=" * 80)
    print("TEST 4: Input Validation")
    print("=" * 80)
    
    generator = AstrologyChartGenerator()
    
    test_cases = [
        {
            'name': 'Missing required field',
            'data': {'name': 'Test'},
            'should_fail': True
        },
        {
            'name': 'Invalid chart type',
            'data': {
                'name': 'Test',
                'chart_type': 'Invalid',
                'chart_name': 'D1',
                'ascendant_sign': 'Aries',
                'planets': []
            },
            'should_fail': True
        },
        {
            'name': 'Invalid ascendant sign',
            'data': {
                'name': 'Test',
                'chart_type': 'North',
                'chart_name': 'D1',
                'ascendant_sign': 'InvalidSign',
                'planets': []
            },
            'should_fail': True
        },
        {
            'name': 'Invalid house number',
            'data': {
                'name': 'Test',
                'chart_type': 'North',
                'chart_name': 'D1',
                'ascendant_sign': 'Aries',
                'planets': [
                    {'name': 'Sun', 'symbol': 'Su', 'house': 13}  # Invalid
                ]
            },
            'should_fail': True
        },
        {
            'name': 'Valid data',
            'data': {
                'name': 'Test',
                'chart_type': 'North',
                'chart_name': 'D1',
                'ascendant_sign': 'Aries',
                'planets': [
                    {'name': 'Sun', 'symbol': 'Su', 'house': 1}
                ]
            },
            'should_fail': False
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🧪 Test: {test_case['name']}")
        is_valid, error = generator.validate_input_data(test_case['data'])
        
        expected_result = not test_case['should_fail']
        actual_result = is_valid
        
        if expected_result == actual_result:
            print(f"   ✓ PASSED (Expected: {expected_result}, Got: {actual_result})")
            if error:
                print(f"   Error message: {error}")
            results.append(True)
        else:
            print(f"   ✗ FAILED (Expected: {expected_result}, Got: {actual_result})")
            results.append(False)
    
    success_count = sum(results)
    total_count = len(results)
    print(f"\n📈 Validation Tests: {success_count}/{total_count} passed")
    
    return all(results)


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🚀 JYOTICHART INTEGRATION TEST SUITE")
    print("=" * 80)
    
    tests = [
        ("Basic Chart Generation", test_basic_chart_generation),
        ("Chart Examples", test_chart_examples),
        ("Integration Service", test_integration_service),
        ("Input Validation", test_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} test suites passed")
    print("=" * 80)
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

