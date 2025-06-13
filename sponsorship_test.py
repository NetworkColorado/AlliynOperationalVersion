#!/usr/bin/env python3
"""
Sponsorship system test for Alliyn business networking app.
Tests the complete sponsorship functionality including frontend and backend.
"""

import requests
import json
import uuid

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def test_sponsorship_api():
    """Test sponsorship API endpoints"""
    print("Testing Sponsorship API...")
    
    # Test getting initial stats (should be empty or have previous data)
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, f"Failed to get stats: {response.status_code}"
    
    stats = response.json()
    print(f"Initial stats: {stats}")
    
    # Test creating a sponsorship request
    sponsor_data = {
        "company_name": f"Test Sponsor {uuid.uuid4()}",
        "contact_name": "John Doe",
        "email": "john@testsponsor.com",
        "phone": "(555) 123-4567",
        "website": "https://testsponsor.com",
        "industry": "Technology",
        "package_type": "Premium - $1,500/month",
        "budget": "$1,000 - $2,500",
        "goals": "Increase brand awareness and generate high-quality leads",
        "additional_info": "We're particularly interested in reaching C-level executives"
    }
    
    response = requests.post(f"{BACKEND_URL}/sponsorship", json=sponsor_data)
    assert response.status_code == 200, f"Failed to create sponsorship: {response.status_code}"
    
    created_sponsor = response.json()
    print(f"Created sponsorship request: {created_sponsor['company_name']}")
    print(f"Estimated quote: ${created_sponsor['estimated_quote']}")
    
    # Verify the quote calculation (Technology industry with Premium package)
    # Should be $1,500 * 1.2 = $1,800
    expected_quote = 1800
    assert created_sponsor['estimated_quote'] == expected_quote, f"Expected quote ${expected_quote}, got ${created_sponsor['estimated_quote']}"
    
    # Test retrieving sponsorship requests
    response = requests.get(f"{BACKEND_URL}/sponsorship")
    assert response.status_code == 200, f"Failed to get sponsorships: {response.status_code}"
    
    sponsorships = response.json()
    assert len(sponsorships) > 0, "No sponsorships found"
    
    # Verify our created sponsorship is in the list
    found_sponsor = None
    for sponsor in sponsorships:
        if sponsor['id'] == created_sponsor['id']:
            found_sponsor = sponsor
            break
    
    assert found_sponsor is not None, "Created sponsorship not found in list"
    print(f"Retrieved sponsorship: {found_sponsor['company_name']}")
    
    # Test updated stats
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, f"Failed to get updated stats: {response.status_code}"
    
    updated_stats = response.json()
    assert updated_stats['total_requests'] > stats['total_requests'], "Stats not updated"
    print(f"Updated stats: {updated_stats}")
    
    print("✅ Sponsorship API tests passed!")
    return True

def test_quote_calculation():
    """Test quote calculation for different packages and industries"""
    print("Testing Quote Calculation...")
    
    test_cases = [
        # (package_type, industry, expected_quote)
        ("Basic - $500/month", "Technology", 600),  # $500 * 1.2
        ("Premium - $1,500/month", "Financial Services", 1950),  # $1,500 * 1.3
        ("Enterprise - Custom", "Healthcare", 3300),  # $3,000 * 1.1
        ("Basic - $500/month", "Other", 500),  # $500 * 1.0
    ]
    
    for package_type, industry, expected_quote in test_cases:
        sponsor_data = {
            "company_name": f"Quote Test {uuid.uuid4()}",
            "contact_name": "Quote Tester",
            "email": "quote@test.com",
            "industry": industry,
            "package_type": package_type,
            "goals": "Testing quote calculation"
        }
        
        response = requests.post(f"{BACKEND_URL}/sponsorship", json=sponsor_data)
        assert response.status_code == 200, f"Failed to create test sponsorship: {response.status_code}"
        
        result = response.json()
        actual_quote = result['estimated_quote']
        
        print(f"Package: {package_type}, Industry: {industry}")
        print(f"Expected: ${expected_quote}, Actual: ${actual_quote}")
        
        assert actual_quote == expected_quote, f"Quote mismatch for {package_type} + {industry}: expected ${expected_quote}, got ${actual_quote}"
    
    print("✅ Quote calculation tests passed!")
    return True

def test_frontend_integration():
    """Test that frontend can access sponsorship functionality"""
    print("Testing Frontend Integration...")
    
    # Test that frontend is accessible
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    
    # Test that React bundle contains sponsorship-related content
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
    
    bundle_content = response.text.lower()
    
    # Check for sponsorship-related keywords
    sponsorship_keywords = ["sponsor", "quote", "package", "advertising"]
    found_keywords = [keyword for keyword in sponsorship_keywords if keyword in bundle_content]
    
    assert len(found_keywords) >= 3, f"Not enough sponsorship keywords found in bundle. Found: {found_keywords}"
    print(f"Found sponsorship keywords in bundle: {found_keywords}")
    
    print("✅ Frontend integration tests passed!")
    return True

def run_all_tests():
    """Run all sponsorship system tests"""
    print("Starting Sponsorship System Tests...")
    print("="*60)
    
    tests = [
        ("Sponsorship API", test_sponsorship_api),
        ("Quote Calculation", test_quote_calculation),
        ("Frontend Integration", test_frontend_integration),
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
    print(f"SPONSORSHIP SYSTEM TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 All sponsorship system tests PASSED!")
        print("The advertising/sponsorship platform is ready for business!")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)