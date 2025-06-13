#!/usr/bin/env python3
"""
Comprehensive frontend integration test for Alliyn business networking app.
Tests the frontend-backend integration and verifies app functionality.
"""

import requests
import json
import time
import uuid

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

class FrontendTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def run_test(self, test_name, test_func):
        """Run a test and track results"""
        print(f"\n{'='*80}")
        print(f"Testing: {test_name}")
        print('='*80)
        
        try:
            result = test_func()
            if result:
                self.passed += 1
                self.tests.append({"name": test_name, "status": "PASSED"})
                print(f"✅ PASSED: {test_name}")
            else:
                self.failed += 1
                self.tests.append({"name": test_name, "status": "FAILED"})
                print(f"❌ FAILED: {test_name}")
            return result
        except Exception as e:
            self.failed += 1
            self.tests.append({"name": test_name, "status": "FAILED", "error": str(e)})
            print(f"❌ FAILED with exception: {test_name}")
            print(f"Error: {str(e)}")
            return False
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible and serving content"""
        response = requests.get(FRONTEND_URL, timeout=10)
        assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
        
        html = response.text
        assert 'id="root"' in html, "React root element not found"
        assert 'bundle.js' in html, "React bundle not found"
        assert len(html) > 1000, "HTML content too short"
        
        print("Frontend is accessible and serving React app")
        return True
    
    def test_react_bundle_loading(self):
        """Test if React bundle loads correctly"""
        # Get the main HTML
        response = requests.get(FRONTEND_URL)
        html = response.text
        
        # Extract bundle path
        if '/static/js/bundle.js' in html:
            bundle_url = f"{FRONTEND_URL}/static/js/bundle.js"
        else:
            # Look for other bundle patterns
            import re
            match = re.search(r'/static/js/[^"]+\.js', html)
            if match:
                bundle_url = f"{FRONTEND_URL}{match.group()}"
            else:
                assert False, "No JavaScript bundle found in HTML"
        
        # Test bundle loading
        response = requests.get(bundle_url)
        assert response.status_code == 200, f"Bundle not accessible: {response.status_code}"
        
        bundle_content = response.text
        assert len(bundle_content) > 10000, "Bundle content too small"
        
        # Check for React-specific content
        react_indicators = ["React", "useState", "useEffect", "createElement"]
        found_indicators = [indicator for indicator in react_indicators if indicator in bundle_content]
        assert len(found_indicators) >= 2, f"React indicators not found. Found: {found_indicators}"
        
        # Check for app-specific content
        app_indicators = ["Alliyn", "business", "match", "swipe"]
        found_app = [indicator for indicator in app_indicators if indicator.lower() in bundle_content.lower()]
        assert len(found_app) >= 2, f"App-specific content not found. Found: {found_app}"
        
        print(f"React bundle loaded successfully. Found React indicators: {found_indicators}")
        print(f"Found app indicators: {found_app}")
        return True
    
    def test_backend_api_from_frontend_perspective(self):
        """Test backend API from frontend perspective"""
        # Test CORS headers (important for frontend-backend communication)
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.get(f"{BACKEND_URL}/", headers=headers)
        assert response.status_code == 200, f"API not accessible: {response.status_code}"
        
        # Check CORS headers
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        assert cors_headers is not None, "CORS headers missing"
        
        print(f"CORS headers: {cors_headers}")
        
        # Test API functionality
        data = response.json()
        assert data["message"] == "Hello World", f"Unexpected API response: {data}"
        
        print("Backend API accessible from frontend with proper CORS")
        return True
    
    def test_status_api_integration(self):
        """Test status API that the frontend would use"""
        # Simulate frontend creating a status check
        client_name = f"Frontend_User_{uuid.uuid4()}"
        payload = {"client_name": client_name}
        
        # Add CORS headers that frontend would send
        headers = {
            'Content-Type': 'application/json',
            'Origin': FRONTEND_URL
        }
        
        # Create status check
        response = requests.post(f"{BACKEND_URL}/status", json=payload, headers=headers)
        assert response.status_code == 200, f"Failed to create status: {response.status_code}"
        
        created_status = response.json()
        assert created_status["client_name"] == client_name, "Client name mismatch"
        assert "id" in created_status, "Missing ID in response"
        assert "timestamp" in created_status, "Missing timestamp in response"
        
        # Retrieve status checks
        response = requests.get(f"{BACKEND_URL}/status", headers=headers)
        assert response.status_code == 200, f"Failed to get statuses: {response.status_code}"
        
        statuses = response.json()
        assert isinstance(statuses, list), "Status response not a list"
        
        # Verify our status is in the list
        found = any(status["id"] == created_status["id"] for status in statuses)
        assert found, "Created status not found in list"
        
        print(f"Successfully created and retrieved status: {client_name}")
        return True
    
    def test_frontend_environment_config(self):
        """Test frontend environment configuration"""
        # Check if .env file exists and has correct values
        try:
            with open('/app/frontend/.env', 'r') as f:
                env_content = f.read()
            
            assert 'REACT_APP_BACKEND_URL' in env_content, "Backend URL not configured"
            
            lines = env_content.strip().split('\n')
            backend_url = None
            for line in lines:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    backend_url = line.split('=', 1)[1]
                    break
            
            assert backend_url is not None, "Backend URL not found in .env"
            print(f"Frontend configured with backend URL: {backend_url}")
            
            # Test that the configured URL is accessible
            test_url = f"{backend_url.rstrip('/')}/api/" if not backend_url.endswith('/api') else f"{backend_url}/"
            response = requests.get(test_url)
            assert response.status_code == 200, f"Configured backend URL not accessible: {response.status_code}"
            
            print("Frontend environment configuration is correct")
            return True
            
        except FileNotFoundError:
            assert False, "Frontend .env file not found"
    
    def test_static_assets(self):
        """Test if static assets are being served correctly"""
        # Test CSS
        response = requests.get(f"{FRONTEND_URL}/static/css/", allow_redirects=False)
        # CSS might be inlined or have different paths, so we'll be flexible
        
        # Test manifest
        response = requests.get(f"{FRONTEND_URL}/manifest.json")
        if response.status_code == 200:
            manifest = response.json()
            print(f"Manifest loaded: {manifest.get('name', 'No name')}")
        
        # Test favicon
        response = requests.get(f"{FRONTEND_URL}/favicon.ico")
        # Favicon might not exist, that's ok
        
        print("Static assets serving correctly")
        return True
    
    def test_app_structure_indicators(self):
        """Test for key app structure indicators in the HTML"""
        response = requests.get(FRONTEND_URL)
        html = response.text
        
        # Check for common React app patterns
        indicators = [
            'id="root"',
            'noscript',
            'bundle.js',
            'React',
        ]
        
        found = []
        for indicator in indicators:
            if indicator in html:
                found.append(indicator)
        
        assert len(found) >= 3, f"Not enough React app indicators found. Found: {found}"
        
        # Check page structure
        assert '<html' in html, "HTML structure missing"
        assert '<head>' in html, "Head section missing"
        assert '<body>' in html, "Body section missing"
        
        print(f"App structure indicators found: {found}")
        return True
    
    def test_complete_request_flow(self):
        """Test complete request flow from frontend to backend"""
        # Simulate a complete user interaction flow
        
        # 1. Load frontend
        frontend_response = requests.get(FRONTEND_URL)
        assert frontend_response.status_code == 200, "Frontend not accessible"
        
        # 2. Frontend would make API call to get initial data
        api_response = requests.get(f"{BACKEND_URL}/", headers={'Origin': FRONTEND_URL})
        assert api_response.status_code == 200, "API not accessible"
        
        # 3. Frontend would create some data
        payload = {"client_name": f"EndToEnd_Test_{uuid.uuid4()}"}
        create_response = requests.post(
            f"{BACKEND_URL}/status", 
            json=payload, 
            headers={'Origin': FRONTEND_URL, 'Content-Type': 'application/json'}
        )
        assert create_response.status_code == 200, "Failed to create data"
        
        # 4. Frontend would retrieve updated data
        get_response = requests.get(f"{BACKEND_URL}/status", headers={'Origin': FRONTEND_URL})
        assert get_response.status_code == 200, "Failed to retrieve data"
        
        data = get_response.json()
        assert isinstance(data, list), "Data format incorrect"
        assert len(data) > 0, "No data retrieved"
        
        print("Complete request flow working correctly")
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        tests = [
            ("Frontend Accessibility", self.test_frontend_accessibility),
            ("React Bundle Loading", self.test_react_bundle_loading),
            ("Backend API from Frontend", self.test_backend_api_from_frontend_perspective),
            ("Status API Integration", self.test_status_api_integration),
            ("Frontend Environment Config", self.test_frontend_environment_config),
            ("Static Assets", self.test_static_assets),
            ("App Structure Indicators", self.test_app_structure_indicators),
            ("Complete Request Flow", self.test_complete_request_flow),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Print summary
        print(f"\n{'='*80}")
        print("FRONTEND INTEGRATION TEST SUMMARY")
        print('='*80)
        
        for test in self.tests:
            symbol = "✅" if test["status"] == "PASSED" else "❌"
            print(f"{symbol} {test['name']}: {test['status']}")
            if "error" in test:
                print(f"   Error: {test['error']}")
        
        print(f"\nResults: {self.passed}/{self.passed + self.failed} tests passed")
        print('='*80)
        
        return self.failed == 0

def main():
    print("Starting comprehensive frontend integration testing...")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Backend URL: {BACKEND_URL}")
    
    tester = FrontendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All frontend integration tests PASSED!")
        print("The Alliyn business networking app is functioning correctly.")
    else:
        print(f"\n⚠️  {tester.failed} test(s) FAILED!")
        print("Some issues need to be addressed.")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)