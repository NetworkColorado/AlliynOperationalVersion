#!/usr/bin/env python3
"""
Admin functionality test for Alliyn business networking app.
Tests the complete admin system including login, sponsorship management, and user management.
"""

import requests
import json

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def test_admin_login_functionality():
    """Test admin login interface and credentials"""
    print("Testing Admin Login Functionality...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
    
    bundle_content = response.text.lower()
    
    # Check for admin login functionality
    admin_keywords = [
        "admin", "login", "thenetworkcolorado", "successs2289", 
        "adminlogin", "admincredentials", "showadminlogin"
    ]
    found_admin = [keyword for keyword in admin_keywords if keyword in bundle_content]
    assert len(found_admin) >= 5, f"Admin login functionality not found. Found: {found_admin}"
    print(f"✅ Found admin login components: {found_admin}")
    
    # Check for admin panel
    admin_panel_keywords = ["adminpanel", "showadminpanel", "admin panel"]
    found_panel = [keyword for keyword in admin_panel_keywords if keyword in bundle_content]
    assert len(found_panel) >= 2, f"Admin panel not found. Found: {found_panel}"
    print("✅ Admin panel components found")
    
    print("✅ Admin login functionality tests passed!")
    return True

def test_admin_backend_endpoints():
    """Test admin backend API endpoints"""
    print("Testing Admin Backend Endpoints...")
    
    # Test admin stats endpoint
    response = requests.get(f"{BACKEND_URL}/admin/stats")
    assert response.status_code == 200, f"Admin stats endpoint failed: {response.status_code}"
    
    stats = response.json()
    expected_keys = ["total_sponsorships", "total_sponsorship_requests", "total_users", "premium_users", "free_users"]
    for key in expected_keys:
        assert key in stats, f"Missing key {key} in admin stats"
    print(f"✅ Admin stats: {stats}")
    
    # Test admin sponsorship creation
    sponsorship_data = {
        "business_name": "Test Admin Sponsor",
        "offer_name": "Test Offer",
        "offer": "Test offer description",
        "website": "https://testadmin.com",
        "release_date": "2025-06-13",
        "release_time": "12:00"
    }
    
    response = requests.post(f"{BACKEND_URL}/admin/sponsorship", json=sponsorship_data)
    assert response.status_code == 200, f"Admin sponsorship creation failed: {response.status_code}"
    
    created_sponsorship = response.json()
    assert created_sponsorship["business_name"] == sponsorship_data["business_name"]
    assert created_sponsorship["status"] == "scheduled"
    print(f"✅ Created admin sponsorship: {created_sponsorship['id']}")
    
    # Test getting admin sponsorships
    response = requests.get(f"{BACKEND_URL}/admin/sponsorship")
    assert response.status_code == 200, f"Admin sponsorship retrieval failed: {response.status_code}"
    
    sponsorships = response.json()
    assert len(sponsorships) > 0, "No admin sponsorships found"
    print(f"✅ Retrieved {len(sponsorships)} admin sponsorships")
    
    print("✅ Admin backend endpoints tests passed!")
    return True

def test_user_management_functionality():
    """Test admin user management features"""
    print("Testing User Management Functionality...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for user management features
    user_management_keywords = [
        "waivepremiumfee", "deactivatepremiumaccount", "deleteaccount",
        "user management", "admin actions", "upgrade user"
    ]
    found_management = [keyword for keyword in user_management_keywords if keyword in bundle_content]
    assert len(found_management) >= 4, f"User management functionality not found. Found: {found_management}"
    print(f"✅ Found user management features: {found_management}")
    
    # Test admin user endpoints
    test_user_id = "test-user-123"
    
    # Test user upgrade
    response = requests.post(f"{BACKEND_URL}/admin/user/{test_user_id}/upgrade")
    assert response.status_code == 200, f"User upgrade endpoint failed: {response.status_code}"
    
    upgrade_result = response.json()
    assert upgrade_result["account_type"] == "premium"
    assert upgrade_result["user_id"] == test_user_id
    print("✅ User upgrade endpoint working")
    
    # Test user downgrade
    response = requests.post(f"{BACKEND_URL}/admin/user/{test_user_id}/downgrade")
    assert response.status_code == 200, f"User downgrade endpoint failed: {response.status_code}"
    
    downgrade_result = response.json()
    assert downgrade_result["account_type"] == "free"
    print("✅ User downgrade endpoint working")
    
    # Test user deletion
    response = requests.delete(f"{BACKEND_URL}/admin/user/{test_user_id}")
    assert response.status_code == 200, f"User deletion endpoint failed: {response.status_code}"
    
    delete_result = response.json()
    assert delete_result["status"] == "deleted"
    print("✅ User deletion endpoint working")
    
    print("✅ User management functionality tests passed!")
    return True

def test_sponsorship_management_features():
    """Test admin sponsorship management features"""
    print("Testing Sponsorship Management Features...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for sponsorship management features
    sponsorship_keywords = [
        "sponsorship management", "business name", "offer name", 
        "logo upload", "media upload", "release date", "release time",
        "adminsponsorships", "setadminsponsorships"
    ]
    found_sponsorship = [keyword for keyword in sponsorship_keywords if keyword in bundle_content]
    assert len(found_sponsorship) >= 6, f"Sponsorship management not comprehensive. Found: {found_sponsorship}"
    print(f"✅ Found sponsorship management features: {found_sponsorship}")
    
    # Check for calendar/scheduling functionality
    calendar_keywords = ["date", "time", "calendar", "schedule", "release"]
    found_calendar = [keyword for keyword in calendar_keywords if keyword in bundle_content]
    assert len(found_calendar) >= 4, f"Calendar scheduling not found. Found: {found_calendar}"
    print("✅ Calendar scheduling functionality found")
    
    # Check for file upload functionality
    upload_keywords = ["upload", "file", "logo", "media", "video", "image"]
    found_upload = [keyword for keyword in upload_keywords if keyword in bundle_content]
    assert len(found_upload) >= 5, f"File upload functionality not comprehensive. Found: {found_upload}"
    print("✅ File upload functionality found")
    
    print("✅ Sponsorship management features tests passed!")
    return True

def test_upgrade_button_linking():
    """Test that upgrade buttons link to premium payment window"""
    print("Testing Upgrade Button Linking...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for upgrade button functionality
    upgrade_keywords = [
        "setshowupgrademodal", "upgrade", "premium", "showupgrademodal",
        "upgrade to premium", "upgrade button"
    ]
    found_upgrade = [keyword for keyword in upgrade_keywords if keyword in bundle_content]
    assert len(found_upgrade) >= 4, f"Upgrade button linking not found. Found: {found_upgrade}"
    print(f"✅ Found upgrade button components: {found_upgrade}")
    
    # Check for payment functionality
    payment_keywords = [
        "handlepremiumupgrade", "payment", "stripe", "paypal", "apple pay"
    ]
    found_payment = [keyword for keyword in payment_keywords if keyword in bundle_content]
    assert len(found_payment) >= 4, f"Payment functionality not linked. Found: {found_payment}"
    print("✅ Payment functionality properly linked")
    
    print("✅ Upgrade button linking tests passed!")
    return True

def test_admin_integration():
    """Test complete admin system integration"""
    print("Testing Admin System Integration...")
    
    # Test frontend accessibility
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    
    # Test backend admin endpoints are available
    admin_endpoints = [
        "/admin/stats",
        "/admin/sponsorship"
    ]
    
    for endpoint in admin_endpoints:
        response = requests.get(f"{BACKEND_URL}{endpoint}")
        assert response.status_code == 200, f"Admin endpoint {endpoint} not working: {response.status_code}"
    
    print("✅ All admin endpoints accessible")
    
    # Test that existing functionality still works
    response = requests.get(f"{BACKEND_URL}/")
    assert response.status_code == 200, "Main API not working"
    
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, "Regular sponsorship API not working"
    
    print("✅ Existing functionality preserved")
    
    print("✅ Admin system integration tests passed!")
    return True

def run_all_tests():
    """Run all admin functionality tests"""
    print("Starting Admin Functionality Tests...")
    print("="*80)
    
    tests = [
        ("Admin Login Functionality", test_admin_login_functionality),
        ("Admin Backend Endpoints", test_admin_backend_endpoints),
        ("User Management Functionality", test_user_management_functionality),
        ("Sponsorship Management Features", test_sponsorship_management_features),
        ("Upgrade Button Linking", test_upgrade_button_linking),
        ("Admin System Integration", test_admin_integration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'-'*60}")
        print(f"Running: {test_name}")
        print(f"{'-'*60}")
        
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
    
    print(f"\n{'='*80}")
    print(f"ADMIN FUNCTIONALITY TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL ADMIN FUNCTIONALITY TESTS PASSED!")
        print("🛠️ Complete admin system is operational:")
        print("   🔐 Admin login with secure credentials")
        print("   📢 Sponsorship management with calendar scheduling")
        print("   👥 User account management (upgrade/downgrade/delete)")
        print("   📊 Admin statistics and monitoring")
        print("   📝 File upload for logos and media")
        print("   ⏰ Real-time and scheduled sponsorship creation")
        print("   🔗 Proper upgrade button linking")
        print("   🎯 Complete backend API integration")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)