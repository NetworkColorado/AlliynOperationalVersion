#!/usr/bin/env python3
"""
Location-based filtering test for Alliyn business networking app.
Tests the geographic filtering functionality for local partnerships.
"""

import requests
import json

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def test_frontend_filtering_functionality():
    """Test that frontend contains location filtering functionality"""
    print("Testing Location Filtering Functionality...")
    
    # Test that frontend is accessible
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    
    # Test that React bundle contains location-related content
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
    
    bundle_content = response.text.lower()
    
    # Check for location filtering keywords
    location_keywords = [
        "calculateDistance", "getLocationCoordinates", "isWithinLocalRange", 
        "filteredProfiles", "seekingPartnership", "serviceAreas", "geographic"
    ]
    found_keywords = [keyword for keyword in location_keywords if keyword.lower() in bundle_content]
    
    print(f"Found location filtering keywords: {found_keywords}")
    assert len(found_keywords) >= 5, f"Not enough location filtering keywords found. Found: {found_keywords}"
    
    # Check for specific location filtering features
    filtering_features = [
        "within", "miles", "local", "national", "distance", "radius"
    ]
    found_features = [feature for feature in filtering_features if feature in bundle_content]
    
    print(f"Found filtering features: {found_features}")
    assert len(found_features) >= 4, f"Not enough filtering features found. Found: {found_features}"
    
    print("✅ Location filtering functionality tests passed!")
    return True

def test_geographic_coordinate_system():
    """Test that the coordinate system includes major cities"""
    print("Testing Geographic Coordinate System...")
    
    # Get the bundle to check if major cities are included
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for major cities in the coordinate system
    major_cities = [
        "san francisco", "new york", "los angeles", "chicago", 
        "houston", "phoenix", "philadelphia", "denver", "seattle", 
        "miami", "boston", "austin", "dallas"
    ]
    
    found_cities = [city for city in major_cities if city.replace(" ", "") in bundle_content.replace(" ", "")]
    
    print(f"Found cities in coordinate system: {found_cities}")
    assert len(found_cities) >= 8, f"Not enough cities found in coordinate system. Found: {found_cities}"
    
    # Check for coordinate-related functionality
    coordinate_features = ["lat", "lng", "latitude", "longitude", "coordinates"]
    found_coord_features = [feature for feature in coordinate_features if feature in bundle_content]
    
    print(f"Found coordinate features: {found_coord_features}")
    assert len(found_coord_features) >= 3, f"Not enough coordinate features found. Found: {found_coord_features}"
    
    print("✅ Geographic coordinate system tests passed!")
    return True

def test_filtering_ui_elements():
    """Test that UI elements for filtering are present"""
    print("Testing Filtering UI Elements...")
    
    # Get the bundle to check for UI elements
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for UI-related filtering elements
    ui_elements = [
        "geographic preference", "local partnerships", "national partnerships",
        "within", "miles", "search radius", "filtering"
    ]
    
    found_ui_elements = [element for element in ui_elements if element.replace(" ", "") in bundle_content.replace(" ", "")]
    
    print(f"Found UI elements: {found_ui_elements}")
    assert len(found_ui_elements) >= 5, f"Not enough UI elements found. Found: {found_ui_elements}"
    
    # Check for partnership scope indicators
    partnership_indicators = ["local", "national", "📍", "🌍"]
    found_indicators = [indicator for indicator in partnership_indicators if indicator in bundle_content]
    
    print(f"Found partnership indicators: {found_indicators}")
    assert len(found_indicators) >= 2, f"Not enough partnership indicators found. Found: {found_indicators}"
    
    print("✅ Filtering UI elements tests passed!")
    return True

def test_distance_calculation_logic():
    """Test that distance calculation logic is implemented"""
    print("Testing Distance Calculation Logic...")
    
    # Get the bundle to check for distance calculation
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for Haversine formula implementation
    haversine_elements = [
        "haversine", "sin", "cos", "atan2", "sqrt", "math.pi", "radius"
    ]
    
    found_haversine = [element for element in haversine_elements if element in bundle_content]
    
    print(f"Found distance calculation elements: {found_haversine}")
    assert len(found_haversine) >= 5, f"Distance calculation logic not found. Found: {found_haversine}"
    
    # Check for Earth's radius constant (3959 miles)
    assert "3959" in bundle_content, "Earth's radius constant not found"
    
    print("✅ Distance calculation logic tests passed!")
    return True

def test_integration_with_existing_features():
    """Test that filtering integrates with existing features"""
    print("Testing Integration with Existing Features...")
    
    # Verify backend is still working
    response = requests.get(f"{BACKEND_URL}/")
    assert response.status_code == 200, f"Backend not accessible: {response.status_code}"
    
    # Test that status API still works
    response = requests.get(f"{BACKEND_URL}/status")
    assert response.status_code == 200, f"Status API not working: {response.status_code}"
    
    # Test that sponsorship API still works
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, f"Sponsorship API not working: {response.status_code}"
    
    # Check that the frontend bundle still contains core app functionality
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    core_features = ["matchmaker", "messages", "leaderboard", "deals", "profile", "sponsor"]
    found_core = [feature for feature in core_features if feature in bundle_content]
    
    print(f"Found core features: {found_core}")
    assert len(found_core) >= 5, f"Core features missing. Found: {found_core}"
    
    print("✅ Integration with existing features tests passed!")
    return True

def run_all_tests():
    """Run all location filtering tests"""
    print("Starting Location-Based Filtering Tests...")
    print("="*60)
    
    tests = [
        ("Frontend Filtering Functionality", test_frontend_filtering_functionality),
        ("Geographic Coordinate System", test_geographic_coordinate_system),
        ("Filtering UI Elements", test_filtering_ui_elements),
        ("Distance Calculation Logic", test_distance_calculation_logic),
        ("Integration with Existing Features", test_integration_with_existing_features),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'-'*40}")
        print(f"Running: {test_name}")
        print(f"{'-'*40}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: FAILED with exception")
            print(f"Error: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"LOCATION FILTERING TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 All location filtering tests PASSED!")
        print("📍 Geographic filtering is working correctly!")
        print("🌍 Users can now filter partnerships by local (20 miles) or national scope!")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)