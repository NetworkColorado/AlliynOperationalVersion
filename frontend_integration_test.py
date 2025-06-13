#!/usr/bin/env python3
"""
Frontend integration test for Alliyn business networking app.
Tests the frontend functionality through browser automation using Selenium.
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8001/api"

def setup_driver():
    """Setup Chrome driver with headless options"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Failed to setup Chrome driver: {e}")
        return None

def test_frontend_loads():
    """Test if frontend loads correctly"""
    print("Testing frontend loading...")
    
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    
    # Check if HTML contains React app structure
    html = response.text
    assert 'id="root"' in html, "React root element not found"
    assert 'bundle.js' in html, "React bundle not found"
    
    print("✅ Frontend loads correctly")
    return True

def test_backend_api():
    """Test backend API is accessible from frontend context"""
    print("Testing backend API accessibility...")
    
    # Test health check
    response = requests.get(f"{BACKEND_URL}/")
    assert response.status_code == 200, f"Backend API not accessible: {response.status_code}"
    
    data = response.json()
    assert data["message"] == "Hello World", f"Unexpected API response: {data}"
    
    print("✅ Backend API accessible")
    return True

def test_react_app_with_selenium():
    """Test React app functionality using Selenium"""
    print("Testing React app with Selenium...")
    
    driver = setup_driver()
    if not driver:
        print("❌ Could not setup browser driver")
        return False
    
    try:
        # Navigate to the app
        driver.get(FRONTEND_URL)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        
        # Check if the app loaded
        root = driver.find_element(By.ID, "root")
        assert root is not None, "React root element not found"
        
        # Wait for React app to initialize (look for key elements)
        try:
            # Look for authentication modal or main app content
            WebDriverWait(driver, 15).until(
                lambda d: len(d.find_elements(By.TAG_NAME, "div")) > 1
            )
            
            # Check page title
            title = driver.title
            print(f"Page title: {title}")
            
            # Check if there are any JavaScript errors
            logs = driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if errors:
                print("JavaScript errors found:")
                for error in errors:
                    print(f"  - {error['message']}")
            else:
                print("✅ No JavaScript errors found")
            
            # Try to find key elements that indicate the app is working
            divs = driver.find_elements(By.TAG_NAME, "div")
            print(f"Found {len(divs)} div elements (indicates React rendering)")
            
            # Look for specific app elements
            buttons = driver.find_elements(By.TAG_NAME, "button")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            
            print(f"Found {len(buttons)} buttons and {len(inputs)} inputs")
            
            # Check if authentication modal or main content is visible
            modals = driver.find_elements(By.CLASS_NAME, "modal")
            if modals:
                print(f"✅ Found {len(modals)} modal(s) - likely authentication modal")
            
            # Look for Alliyn-specific content
            page_source = driver.page_source.lower()
            if "alliyn" in page_source or "business" in page_source or "match" in page_source:
                print("✅ Found Alliyn-specific content")
            else:
                print("⚠️  No Alliyn-specific content found in page source")
            
            return True
            
        except Exception as e:
            print(f"❌ React app initialization failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False
    finally:
        driver.quit()

def test_api_integration():
    """Test if frontend can communicate with backend"""
    print("Testing API integration...")
    
    # Test creating a status check (simulating frontend call)
    payload = {"client_name": "Frontend_Test_Client"}
    response = requests.post(f"{BACKEND_URL}/status", json=payload)
    
    assert response.status_code == 200, f"Failed to create status check: {response.status_code}"
    data = response.json()
    assert "id" in data, "Status check response missing ID"
    
    # Test retrieving status checks
    response = requests.get(f"{BACKEND_URL}/status")
    assert response.status_code == 200, f"Failed to get status checks: {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Status checks response not a list"
    
    print("✅ API integration working correctly")
    return True

def run_all_tests():
    """Run all frontend tests"""
    tests = [
        ("Frontend Loading", test_frontend_loads),
        ("Backend API", test_backend_api),
        ("API Integration", test_api_integration),
        ("React App with Browser", test_react_app_with_selenium),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED"))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, "FAILED"))
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, status in results:
        symbol = "✅" if status == "PASSED" else "❌"
        print(f"{symbol} {test_name}: {status}")
        if status == "PASSED":
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    return passed == len(results)

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)