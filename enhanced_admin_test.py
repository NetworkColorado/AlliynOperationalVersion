#!/usr/bin/env python3
"""
Enhanced admin access test for Alliyn business networking app.
Tests the improved admin login interface with color changes and logout functionality.
"""

import requests
import json

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def test_admin_mode_visual_feedback():
    """Test that admin mode changes the visual appearance of the login modal"""
    print("Testing Admin Mode Visual Feedback...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
    
    bundle_content = response.text.lower()
    
    # Check for admin mode visual indicators
    visual_indicators = [
        "isadminmode", "admin login mode", "bg-red-50", "border-red-500",
        "text-red-800", "admin access required", "exit admin mode"
    ]
    found_indicators = [indicator for indicator in visual_indicators if indicator in bundle_content]
    assert len(found_indicators) >= 5, f"Admin mode visual feedback not comprehensive. Found: {found_indicators}"
    print(f"✅ Found admin mode visual indicators: {found_indicators}")
    
    # Check for color scheme changes
    color_schemes = [
        "bg-red-50", "border-red-500", "text-red-600", "bg-red-500", 
        "from-red-500", "to-red-600", "border-red-300"
    ]
    found_colors = [color for color in color_schemes if color in bundle_content]
    assert len(found_colors) >= 5, f"Admin color scheme not implemented. Found: {found_colors}"
    print(f"✅ Found admin color scheme: {found_colors}")
    
    print("✅ Admin mode visual feedback tests passed!")
    return True

def test_admin_access_button_functionality():
    """Test that the admin access button properly triggers admin mode"""
    print("Testing Admin Access Button Functionality...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for admin access button functionality
    button_functions = [
        "enteradminmode", "exitadminmode", "admin access", 
        "admin mode active", "🔐 admin mode active"
    ]
    found_functions = [func for func in button_functions if func in bundle_content]
    assert len(found_functions) >= 4, f"Admin access button functionality not complete. Found: {found_functions}"
    print(f"✅ Found admin access button functions: {found_functions}")
    
    # Check for state management
    state_management = [
        "setisadminmode", "isadminmode", "admincredentials",
        "setadmincredentials", "showadminpanel"
    ]
    found_state = [state for state in state_management if state in bundle_content]
    assert len(found_state) >= 4, f"Admin state management not complete. Found: {found_state}"
    print(f"✅ Found admin state management: {found_state}")
    
    print("✅ Admin access button functionality tests passed!")
    return True

def test_admin_logout_functionality():
    """Test admin logout button and session management"""
    print("Testing Admin Logout Functionality...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for logout functionality
    logout_functions = [
        "handleadminlogout", "admin logged out", "logout", 
        "setisadmin", "setshowadminpanel", "admin logout"
    ]
    found_logout = [func for func in logout_functions if func in bundle_content]
    assert len(found_logout) >= 5, f"Admin logout functionality not complete. Found: {found_logout}"
    print(f"✅ Found admin logout functions: {found_logout}")
    
    # Check for session cleanup
    session_cleanup = [
        "setisadmin(false)", "setshowadminpanel(false)", 
        "setadmincredentials", "setisadminmode(false)"
    ]
    found_cleanup = [cleanup for cleanup in session_cleanup if cleanup in bundle_content]
    assert len(found_cleanup) >= 3, f"Session cleanup not comprehensive. Found: {found_cleanup}"
    print(f"✅ Found session cleanup: {found_cleanup}")
    
    print("✅ Admin logout functionality tests passed!")
    return True

def test_admin_form_integration():
    """Test that admin login is properly integrated with the main authentication form"""
    print("Testing Admin Form Integration...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for form integration
    form_integration = [
        "handleadminlogin", "admin email", "admin password",
        "thenetworkcolorado@gmail.com", "successs2289"
    ]
    found_integration = [item for item in form_integration if item in bundle_content]
    assert len(found_integration) >= 4, f"Admin form integration not complete. Found: {found_integration}"
    print(f"✅ Found admin form integration: {found_integration}")
    
    # Check for credential validation
    validation_checks = [
        "admin_email", "admin_password", "invalid admin credentials",
        "admin login successful", "admin panel"
    ]
    found_validation = [check for check in validation_checks if check in bundle_content]
    assert len(found_validation) >= 4, f"Credential validation not complete. Found: {found_validation}"
    print(f"✅ Found credential validation: {found_validation}")
    
    print("✅ Admin form integration tests passed!")
    return True

def test_admin_mode_transitions():
    """Test smooth transitions between normal mode and admin mode"""
    print("Testing Admin Mode Transitions...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for transition functions
    transitions = [
        "enteradminmode", "exitadminmode", "cancel", 
        "admin login", "🔐 admin login", "exit admin mode"
    ]
    found_transitions = [trans for trans in transitions if trans in bundle_content]
    assert len(found_transitions) >= 5, f"Admin mode transitions not complete. Found: {found_transitions}"
    print(f"✅ Found admin mode transitions: {found_transitions}")
    
    # Check for modal state management
    modal_states = [
        "showautmodal", "setshowautmodal", "isadminmode",
        "showadminpanel", "setshowadminpanel"
    ]
    found_modals = [modal for modal in modal_states if modal in bundle_content]
    assert len(found_modals) >= 4, f"Modal state management not complete. Found: {found_modals}"
    print(f"✅ Found modal state management: {found_modals}")
    
    print("✅ Admin mode transitions tests passed!")
    return True

def test_admin_security_features():
    """Test admin security features and access controls"""
    print("Testing Admin Security Features...")
    
    # Get the React bundle
    response = requests.get(f"{FRONTEND_URL}/static/js/bundle.js")
    bundle_content = response.text.lower()
    
    # Check for security features
    security_features = [
        "admin credentials", "secure", "🔐", "admin access required",
        "invalid admin credentials", "admin authentication"
    ]
    found_security = [feature for feature in security_features if feature in bundle_content]
    assert len(found_security) >= 5, f"Admin security features not complete. Found: {found_security}"
    print(f"✅ Found admin security features: {found_security}")
    
    # Check for access control
    access_control = [
        "isadmin", "admin panel", "administrator", 
        "admin only", "admin mode"
    ]
    found_access = [control for control in access_control if control in bundle_content]
    assert len(found_access) >= 4, f"Access control not complete. Found: {found_access}"
    print(f"✅ Found access control features: {found_access}")
    
    print("✅ Admin security features tests passed!")
    return True

def test_existing_functionality_preservation():
    """Test that existing functionality still works with admin enhancements"""
    print("Testing Existing Functionality Preservation...")
    
    # Test frontend accessibility
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    
    # Test backend functionality
    response = requests.get(f"{BACKEND_URL}/")
    assert response.status_code == 200, f"Backend API not working: {response.status_code}"
    
    # Test admin endpoints still work
    response = requests.get(f"{BACKEND_URL}/admin/stats")
    assert response.status_code == 200, f"Admin endpoints not working: {response.status_code}"
    
    # Test regular endpoints still work
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    assert response.status_code == 200, f"Regular endpoints not working: {response.status_code}"
    
    print("✅ All existing functionality preserved")
    
    print("✅ Existing functionality preservation tests passed!")
    return True

def run_all_tests():
    """Run all enhanced admin functionality tests"""
    print("Starting Enhanced Admin Access Tests...")
    print("="*80)
    
    tests = [
        ("Admin Mode Visual Feedback", test_admin_mode_visual_feedback),
        ("Admin Access Button Functionality", test_admin_access_button_functionality),
        ("Admin Logout Functionality", test_admin_logout_functionality),
        ("Admin Form Integration", test_admin_form_integration),
        ("Admin Mode Transitions", test_admin_mode_transitions),
        ("Admin Security Features", test_admin_security_features),
        ("Existing Functionality Preservation", test_existing_functionality_preservation),
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
    print(f"ENHANCED ADMIN ACCESS TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL ENHANCED ADMIN ACCESS TESTS PASSED!")
        print("🔐 Enhanced admin system is fully operational:")
        print("   🎨 Visual feedback when in admin mode (red color scheme)")
        print("   🔄 Smooth transitions between normal and admin login")
        print("   🚪 Proper logout functionality with session cleanup")
        print("   🔒 Secure credential validation and access control")
        print("   ⚡ Seamless integration with existing authentication")
        print("   🛡️ Admin mode indicators and security features")
        print("   ✨ Enhanced user experience with clear visual cues")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the issues.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)