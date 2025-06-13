
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

def test_frontend_accessibility():
    """Test if the frontend is accessible"""
    try:
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200, f"Frontend not accessible. Status code: {response.status_code}"
        assert "<!doctype html>" in response.text.lower(), "Frontend response is not HTML"
        assert '<div id="root"></div>' in response.text, "React root element not found"
        print("✅ Frontend is accessible and serving React content")
        return True
    except Exception as e:
        print(f"❌ Frontend accessibility test failed: {str(e)}")
        return False

def test_backend_api_health():
    """Test if the backend API is accessible"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/")
        response = requests.get(api_url)
        assert response.status_code == 200, f"Backend API not accessible. Status code: {response.status_code}"
        print("✅ Backend API is accessible")
        return True
    except Exception as e:
        print(f"❌ Backend API health test failed: {str(e)}")
        return False

def test_sponsorship_api():
    """Test the sponsorship API endpoints"""
    try:
        # Test GET sponsorship endpoint
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/sponsorship")
        response = requests.get(api_url)
        assert response.status_code == 200, f"GET sponsorship failed. Status code: {response.status_code}"
        print("✅ GET sponsorship endpoint is working")
        
        # Test POST sponsorship endpoint
        test_data = {
            "companyName": "Test Company",
            "contactName": "John Tester",
            "email": "test@example.com",
            "phone": "555-123-4567",
            "industry": "Technology",
            "packageType": "Basic",
            "budget": "$500-$1000",
            "message": "This is a test sponsorship request"
        }
        
        response = requests.post(api_url, json=test_data)
        assert response.status_code in [200, 201], f"POST sponsorship failed. Status code: {response.status_code}"
        print("✅ POST sponsorship endpoint is working")
        
        return True
    except Exception as e:
        print(f"❌ Sponsorship API test failed: {str(e)}")
        return False

def test_admin_api():
    """Test the admin API endpoints"""
    try:
        # Test GET admin sponsorship endpoint
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/admin/sponsorship")
        response = requests.get(api_url)
        # Even if it requires authentication, it should return 401 not 404
        assert response.status_code in [200, 401, 403], f"GET admin sponsorship failed. Status code: {response.status_code}"
        print(f"✅ GET admin sponsorship endpoint is accessible (status: {response.status_code})")
        
        return True
    except Exception as e:
        print(f"❌ Admin API test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return overall status"""
    print("🔍 Starting frontend integration tests...")
    
    tests = [
        ("Frontend Accessibility", test_frontend_accessibility),
        ("Backend API Health", test_backend_api_health),
        ("Sponsorship API", test_sponsorship_api),
        ("Admin API", test_admin_api)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Running test: {name}")
        result = test_func()
        results.append(result)
        if not result:
            print(f"⚠️ Test '{name}' failed")
    
    success_count = results.count(True)
    total_count = len(results)
    
    print(f"\n📊 Test Summary: {success_count}/{total_count} tests passed")
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
