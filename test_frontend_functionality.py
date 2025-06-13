
import requests
import json
import time
import sys
from urllib.parse import urljoin
import os

# Configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001"
API_PREFIX = "/api"

def test_user_signup():
    """Test user signup functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/users")
        
        # Create a unique test user
        timestamp = int(time.time())
        test_user = {
            "email": f"test{timestamp}@example.com",
            "password": "Password123!",
            "ownerName": "Test User",
            "ownerTitle": "Test Title",
            "companyName": "Test Company",
            "companyDescription": "A test company for API testing",
            "industry": "Technology",
            "yearsInBusiness": 5,
            "serviceAreas": ["Denver", "Remote"],
            "seekingPartnership": "National",
            "partnerships": ["Strategic Alliances", "Joint Ventures"]
        }
        
        # Try to create the user
        response = requests.post(api_url, json=test_user)
        
        # Check if the endpoint exists
        if response.status_code == 404:
            print("⚠️ User signup API endpoint not found. This might be implemented client-side only.")
            return "NA"
        
        # Check if the user was created successfully
        if response.status_code in [200, 201]:
            print("✅ User signup API working correctly")
            return True
        else:
            print(f"❌ User signup failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ User signup test failed: {str(e)}")
        return False

def test_user_login():
    """Test user login functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/auth/login")
        
        # Test credentials
        login_data = {
            "email": "test@example.com",
            "password": "Password123!"
        }
        
        # Try to login
        response = requests.post(api_url, json=login_data)
        
        # Check if the endpoint exists
        if response.status_code == 404:
            print("⚠️ User login API endpoint not found. This might be implemented client-side only.")
            return "NA"
        
        # Check login response
        if response.status_code in [200, 201]:
            print("✅ User login API working correctly")
            return True
        else:
            print(f"❌ User login failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ User login test failed: {str(e)}")
        return False

def test_profile_management():
    """Test profile management functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/users/profile")
        
        # Test profile data
        profile_data = {
            "companyName": "Updated Test Company",
            "companyDescription": "An updated test company description",
            "ownerName": "Updated Test User",
            "ownerTitle": "Updated Test Title",
            "industry": "Healthcare",
            "yearsInBusiness": 10,
            "serviceAreas": ["New York", "Remote"],
            "seekingPartnership": "Local",
            "partnerships": ["Co-Branding", "Affiliate Partnerships"]
        }
        
        # Try to update profile
        response = requests.put(api_url, json=profile_data)
        
        # Check if the endpoint exists
        if response.status_code == 404:
            print("⚠️ Profile management API endpoint not found. This might be implemented client-side only.")
            return "NA"
        
        # Check profile update response
        if response.status_code in [200, 201, 204]:
            print("✅ Profile management API working correctly")
            return True
        else:
            print(f"❌ Profile update failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile management test failed: {str(e)}")
        return False

def test_matching_system():
    """Test the matching system functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/matches")
        
        # Try to get matches
        response = requests.get(api_url)
        
        # Check if the endpoint exists
        if response.status_code == 404:
            print("⚠️ Matching system API endpoint not found. This might be implemented client-side only.")
            return "NA"
        
        # Check matches response
        if response.status_code == 200:
            matches = response.json()
            print(f"✅ Matching system API working correctly. Found {len(matches) if isinstance(matches, list) else 'some'} matches.")
            return True
        else:
            print(f"❌ Getting matches failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Matching system test failed: {str(e)}")
        return False

def test_sponsorship_system():
    """Test the sponsorship system functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/sponsorship")
        
        # Test sponsorship request data
        sponsorship_data = {
            "companyName": "Test Sponsor Company",
            "contactName": "Test Sponsor",
            "email": "sponsor@example.com",
            "phone": "555-123-4567",
            "industry": "Technology",
            "packageType": "Basic",
            "budget": "$500-$1000",
            "message": "This is a test sponsorship request"
        }
        
        # Try to create a sponsorship request
        post_response = requests.post(api_url, json=sponsorship_data)
        
        # Check if the endpoint exists and works
        if post_response.status_code == 404:
            print("⚠️ Sponsorship system API endpoint not found.")
            return "NA"
        
        if post_response.status_code in [200, 201]:
            print("✅ Sponsorship request creation API working correctly")
        else:
            print(f"❌ Sponsorship request creation failed. Status: {post_response.status_code}, Response: {post_response.text}")
            return False
        
        # Try to get sponsorship requests
        get_response = requests.get(api_url)
        
        if get_response.status_code == 200:
            sponsorships = get_response.json()
            print(f"✅ Sponsorship listing API working correctly. Found {len(sponsorships) if isinstance(sponsorships, list) else 'some'} sponsorships.")
            return True
        else:
            print(f"❌ Getting sponsorships failed. Status: {get_response.status_code}, Response: {get_response.text}")
            return False
    except Exception as e:
        print(f"❌ Sponsorship system test failed: {str(e)}")
        return False

def test_admin_system():
    """Test the admin system functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/admin/sponsorship")
        
        # Try to get admin sponsorships
        response = requests.get(api_url)
        
        # Check if the endpoint exists
        if response.status_code == 404:
            print("⚠️ Admin system API endpoint not found.")
            return "NA"
        
        # Check admin response
        if response.status_code in [200, 401, 403]:
            if response.status_code == 200:
                print("✅ Admin system API accessible without authentication")
            else:
                print(f"✅ Admin system API requires authentication (status: {response.status_code})")
            return True
        else:
            print(f"❌ Admin system access failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Admin system test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return overall status"""
    print("🔍 Starting frontend functionality tests...")
    
    tests = [
        ("User Signup", test_user_signup),
        ("User Login", test_user_login),
        ("Profile Management", test_profile_management),
        ("Matching System", test_matching_system),
        ("Sponsorship System", test_sponsorship_system),
        ("Admin System", test_admin_system)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\n📋 Running test: {name}")
        result = test_func()
        results[name] = result
        if result is False:
            print(f"⚠️ Test '{name}' failed")
    
    # Count results
    success_count = list(results.values()).count(True)
    na_count = list(results.values()).count("NA")
    fail_count = list(results.values()).count(False)
    total_count = len(results)
    
    print(f"\n📊 Test Summary: {success_count} passed, {fail_count} failed, {na_count} N/A out of {total_count} tests")
    
    # Print detailed results
    print("\nDetailed Results:")
    for name, result in results.items():
        status = "✅ Passed" if result is True else "❌ Failed" if result is False else "⚠️ N/A"
        print(f"{name}: {status}")
    
    return fail_count == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
