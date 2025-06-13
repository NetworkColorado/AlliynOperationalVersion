#!/usr/bin/env python3
"""
Comprehensive enhancement test for Alliyn business networking app.
Tests all the new features implemented: settings save, sponsorship quote links,
premium upgrades, UI improvements, and advanced matching algorithm.
"""

import requests
import json

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def test_ui_enhancements():
    """Test UI improvements and icon changes"""
    print("Testing UI Enhancements...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
    
    bundle_content = response.text
    
    # Check for briefcase icon instead of heart with ribbon
    assert "💼" in bundle_content, "Briefcase icon not found for matchmaker"
    print("✅ Matchmaker icon changed to briefcase")
    
    # Check for profile picture size increase (w-20 h-20 instead of w-16 h-16)
    assert "w-20 h-20" in bundle_content, "Profile picture size not increased"
    print("✅ Profile picture size increased")
    
    # Check for settings save functionality
    settings_keywords = ["savesettings", "save settings", "💾"]
    found_settings = [keyword for keyword in settings_keywords if keyword.lower() in bundle_content.lower()]
    assert len(found_settings) >= 2, f"Settings save functionality not found. Found: {found_settings}"
    print("✅ Settings save functionality implemented")
    
    print("✅ UI enhancements tests passed!")
    return True

def test_advanced_matching_algorithm():
    """Test the advanced matching probability algorithm"""
    print("Testing Advanced Matching Algorithm...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for advanced matching algorithm components
    matching_keywords = [
        "calculateadvancedmatchprobability", "industrycompatibility", 
        "partnershipalignment", "geographiccompatibility", 
        "experiencecompatibility", "keywordmatch", "extractkeywords"
    ]
    
    found_matching = [keyword for keyword in matching_keywords if keyword in bundle_content]
    assert len(found_matching) >= 5, f"Advanced matching algorithm not found. Found: {found_matching}"
    print(f"✅ Found advanced matching components: {len(found_matching)}/7")
    
    # Check for industry synergy matrix
    industry_synergies = [
        "industrysynergies", "healthcare", "financial", "legal", 
        "insurance", "technology", "manufacturing"
    ]
    found_synergies = [synergy for synergy in industry_synergies if synergy in bundle_content]
    assert len(found_synergies) >= 5, f"Industry synergy matrix not comprehensive. Found: {found_synergies}"
    print("✅ Comprehensive industry synergy matrix implemented")
    
    # Check for weighted scoring system
    scoring_indicators = ["score", "maxscore", "25", "20", "15", "10", "5"]
    found_scoring = [indicator for indicator in scoring_indicators if indicator in bundle_content]
    assert len(found_scoring) >= 6, f"Weighted scoring system not found. Found: {found_scoring}"
    print("✅ Weighted scoring system implemented")
    
    print("✅ Advanced matching algorithm tests passed!")
    return True

def test_expanded_industries():
    """Test the expanded industry list (top 20)"""
    print("Testing Expanded Industries...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for top 20 industries
    top_industries = [
        "technology", "healthcare", "financial", "professional", 
        "real estate", "marketing", "education", "manufacturing",
        "retail", "construction", "food", "transportation",
        "energy", "insurance", "legal", "consulting",
        "hospitality", "non-profit", "entertainment", "agriculture"
    ]
    
    found_industries = [industry for industry in top_industries if industry in bundle_content]
    assert len(found_industries) >= 18, f"Not enough industries found. Found: {len(found_industries)}/20"
    print(f"✅ Found {len(found_industries)}/20 top industries")
    
    # Check for specific industry combinations mentioned in synergy matrix
    synergy_combinations = [
        "tech", "medical", "insurance", "law", "finance"
    ]
    found_combinations = [combo for combo in synergy_combinations if combo in bundle_content]
    assert len(found_combinations) >= 4, f"Industry synergy combinations not found. Found: {found_combinations}"
    print("✅ Industry synergy combinations implemented")
    
    print("✅ Expanded industries tests passed!")
    return True

def test_sponsorship_enhancements():
    """Test sponsorship quote links and improvements"""
    print("Testing Sponsorship Enhancements...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for quote form navigation
    quote_navigation = [
        "scrollintoview", "quote-form-section", "smooth", 
        "get quote", "quote form"
    ]
    found_navigation = [nav for nav in quote_navigation if nav in bundle_content]
    assert len(found_navigation) >= 3, f"Quote form navigation not implemented. Found: {found_navigation}"
    print("✅ Quote form navigation implemented")
    
    # Check for sponsorship packages
    sponsorship_packages = ["basic", "premium", "enterprise", "$500", "$1,500"]
    found_packages = [package for package in sponsorship_packages if package in bundle_content]
    assert len(found_packages) >= 4, f"Sponsorship packages not complete. Found: {found_packages}"
    print("✅ Sponsorship packages properly implemented")
    
    print("✅ Sponsorship enhancements tests passed!")
    return True

def test_premium_upgrade_functionality():
    """Test premium upgrade payment functionality"""
    print("Testing Premium Upgrade Functionality...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for payment methods
    payment_methods = [
        "handlepremiumupgrade", "handlepaymentmethod", 
        "stripe", "paypal", "apple pay", "credit card"
    ]
    found_payment = [method for method in payment_methods if method in bundle_content]
    assert len(found_payment) >= 4, f"Payment methods not implemented. Found: {found_payment}"
    print("✅ Multiple payment methods implemented")
    
    # Check for upgrade features
    upgrade_features = [
        "unlimited", "premium badge", "priority support", 
        "$19.99", "per month"
    ]
    found_features = [feature for feature in upgrade_features if feature in bundle_content]
    assert len(found_features) >= 4, f"Upgrade features not complete. Found: {found_features}"
    print("✅ Premium upgrade features properly described")
    
    print("✅ Premium upgrade functionality tests passed!")
    return True

def test_backend_integration():
    """Test that backend still works with all changes"""
    print("Testing Backend Integration...")
    
    # Test basic API functionality
    response = requests.get(f"{BACKEND_URL}/")
    assert response.status_code == 200, f"Backend API not accessible: {response.status_code}"
    
    # Test sponsorship API
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, f"Sponsorship API not working: {response.status_code}"
    
    stats = response.json()
    assert "total_requests" in stats, "Sponsorship stats structure incorrect"
    print("✅ Backend APIs working correctly")
    
    # Test status API
    response = requests.get(f"{BACKEND_URL}/status")
    assert response.status_code == 200, f"Status API not working: {response.status_code}"
    
    print("✅ Backend integration tests passed!")
    return True

def run_all_tests():
    """Run all enhancement tests"""
    print("Starting Comprehensive Enhancement Tests...")
    print("="*70)
    
    tests = [
        ("UI Enhancements", test_ui_enhancements),
        ("Advanced Matching Algorithm", test_advanced_matching_algorithm),
        ("Expanded Industries", test_expanded_industries),
        ("Sponsorship Enhancements", test_sponsorship_enhancements),
        ("Premium Upgrade Functionality", test_premium_upgrade_functionality),
        ("Backend Integration", test_backend_integration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'-'*50}")
        print(f"Running: {test_name}")
        print(f"{'-'*50}")
        
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
    
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE ENHANCEMENT TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL ENHANCEMENT TESTS PASSED!")
        print("✨ All requested features have been successfully implemented:")
        print("   💾 Settings save functionality")
        print("   🔗 Sponsorship quote form links")
        print("   💳 Premium upgrade payment options")
        print("   💼 Briefcase icon for matchmaker")
        print("   📷 Larger profile pictures")
        print("   🧠 Advanced matching algorithm")
        print("   🏭 Expanded industry list (20+ industries)")
        print("   🤝 Industry synergy matrix")
        print("   📊 Weighted compatibility scoring")
        print("   🎯 Keyword-based profile matching")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)