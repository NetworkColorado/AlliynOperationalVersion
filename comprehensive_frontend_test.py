
import requests
import json
import time
import sys
from urllib.parse import urljoin
import os
import re
from bs4 import BeautifulSoup

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

def test_react_bundle_loading():
    """Test if the React bundle is properly loaded"""
    try:
        response = requests.get(FRONTEND_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for script tags that load the React bundle
        script_tags = soup.find_all('script')
        bundle_loaded = any('chunk' in script.get('src', '') for script in script_tags if script.get('src'))
        
        assert bundle_loaded, "React bundle scripts not found"
        
        # Check for app-specific content
        app_content = re.search(r'(alliyn|business|network|match)', response.text.lower())
        assert app_content, "App-specific content not found in the HTML"
        
        print("✅ React bundle is properly loaded with app-specific content")
        return True
    except Exception as e:
        print(f"❌ React bundle loading test failed: {str(e)}")
        return False

def test_backend_api_integration():
    """Test if the frontend can integrate with the backend API"""
    try:
        # Test CORS headers from backend
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/")
        response = requests.options(api_url)
        
        assert 'Access-Control-Allow-Origin' in response.headers, "CORS headers not set"
        assert 'Access-Control-Allow-Credentials' in response.headers or 'Access-Control-Allow-Methods' in response.headers, "CORS credentials not allowed"
        
        print("✅ Backend API has proper CORS configuration for frontend integration")
        return True
    except Exception as e:
        print(f"❌ Backend API integration test failed: {str(e)}")
        return False

def test_status_api():
    """Test the status API endpoint"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/status")
        
        # Create a test status
        test_data = {
            "message": "Test status from frontend integration test",
            "timestamp": int(time.time())
        }
        
        post_response = requests.post(api_url, json=test_data)
        assert post_response.status_code in [200, 201], f"POST status failed. Status code: {post_response.status_code}"
        
        # Get all statuses
        get_response = requests.get(api_url)
        assert get_response.status_code == 200, f"GET status failed. Status code: {get_response.status_code}"
        
        statuses = get_response.json()
        assert isinstance(statuses, list), "Response is not a list of statuses"
        
        # Check if our test status was saved
        found = any(s.get('message') == test_data['message'] for s in statuses)
        assert found, "Test status not found in the response"
        
        print("✅ Status API is working correctly with proper data persistence")
        return True
    except Exception as e:
        print(f"❌ Status API test failed: {str(e)}")
        return False

def test_environment_configuration():
    """Test if the environment variables are properly configured"""
    try:
        # Check if the frontend is using the correct backend URL
        response = requests.get(FRONTEND_URL)
        
        # Look for the backend URL in the HTML (it might be embedded in the JS bundle)
        backend_url_pattern = re.compile(r'(http://localhost:8001)')
        match = backend_url_pattern.search(response.text)
        
        # This is a best-effort check, as the URL might be in a bundled JS file
        if match:
            print("✅ Frontend is configured with the correct backend URL")
        else:
            print("⚠️ Could not verify backend URL in frontend HTML (might be in bundled JS)")
        
        # Check if the backend is accessible from the frontend URL
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/")
        api_response = requests.get(api_url)
        assert api_response.status_code == 200, "Backend API not accessible from frontend"
        
        print("✅ Environment configuration is correct")
        return True
    except Exception as e:
        print(f"❌ Environment configuration test failed: {str(e)}")
        return False

def test_static_assets():
    """Test if static assets are properly served"""
    try:
        response = requests.get(FRONTEND_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for CSS links
        css_links = soup.find_all('link', rel='stylesheet')
        
        # Check for JS scripts
        js_scripts = soup.find_all('script', src=True)
        
        assert len(css_links) > 0 or len(js_scripts) > 0, "No static assets found"
        
        # Try to access one of the assets
        if len(js_scripts) > 0:
            script_src = js_scripts[0]['src']
            if not script_src.startswith('http'):
                script_src = urljoin(FRONTEND_URL, script_src)
            
            asset_response = requests.get(script_src)
            assert asset_response.status_code == 200, f"Static asset not accessible: {script_src}"
        
        print("✅ Static assets are properly served")
        return True
    except Exception as e:
        print(f"❌ Static assets test failed: {str(e)}")
        return False

def test_app_structure():
    """Test if the app has the expected structure indicators"""
    try:
        response = requests.get(FRONTEND_URL)
        
        # Look for indicators of the Alliyn business networking app
        indicators = [
            'match',
            'business',
            'network',
            'partner',
            'profile',
            'sponsor'
        ]
        
        found_indicators = []
        for indicator in indicators:
            if re.search(indicator, response.text, re.IGNORECASE):
                found_indicators.append(indicator)
        
        assert len(found_indicators) > 0, "No app structure indicators found"
        
        print(f"✅ App structure indicators found: {', '.join(found_indicators)}")
        return True
    except Exception as e:
        print(f"❌ App structure test failed: {str(e)}")
        return False

def test_complete_request_flow():
    """Test a complete request flow from frontend to backend and back"""
    try:
        # 1. Create a unique test message
        test_message = f"Integration test message {int(time.time())}"
        
        # 2. Post the message to the status API
        status_api_url = urljoin(BACKEND_URL, API_PREFIX + "/status")
        post_data = {
            "message": test_message,
            "timestamp": int(time.time())
        }
        
        post_response = requests.post(status_api_url, json=post_data)
        assert post_response.status_code in [200, 201], f"Failed to post test message. Status: {post_response.status_code}"
        
        # 3. Get all statuses to verify our message was saved
        get_response = requests.get(status_api_url)
        assert get_response.status_code == 200, f"Failed to get statuses. Status: {get_response.status_code}"
        
        statuses = get_response.json()
        found = any(s.get('message') == test_message for s in statuses)
        assert found, "Test message not found in the response"
        
        print("✅ Complete request flow test passed")
        return True
    except Exception as e:
        print(f"❌ Complete request flow test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return overall status"""
    print("🔍 Starting comprehensive frontend integration tests...")
    
    tests = [
        ("Frontend Accessibility", test_frontend_accessibility),
        ("React Bundle Loading", test_react_bundle_loading),
        ("Backend API Integration", test_backend_api_integration),
        ("Status API", test_status_api),
        ("Environment Configuration", test_environment_configuration),
        ("Static Assets", test_static_assets),
        ("App Structure", test_app_structure),
        ("Complete Request Flow", test_complete_request_flow)
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
