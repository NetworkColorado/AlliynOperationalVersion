
import requests
import json
import time
import sys
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "http://localhost:8001"
API_PREFIX = "/api"

def test_sponsorship_system():
    """Test the sponsorship system functionality by directly calling the backend API"""
    try:
        api_url = urljoin(BACKEND_URL, API_PREFIX + "/sponsorship")
        
        # Test sponsorship request data with snake_case field names as expected by the backend
        sponsorship_data = {
            "company_name": "Test Sponsor Company",
            "contact_name": "Test Sponsor",
            "email": "sponsor@example.com",
            "phone": "555-123-4567",
            "industry": "Technology",
            "package_type": "Basic",
            "budget": "$500-$1000",
            "message": "This is a test sponsorship request",
            "goals": "Testing the sponsorship API"
        }
        
        # Try to create a sponsorship request
        print(f"Sending POST request to {api_url} with data: {json.dumps(sponsorship_data, indent=2)}")
        post_response = requests.post(api_url, json=sponsorship_data)
        
        # Check if the endpoint exists and works
        if post_response.status_code == 404:
            print("⚠️ Sponsorship system API endpoint not found.")
            return False
        
        print(f"POST response status: {post_response.status_code}")
        print(f"POST response body: {post_response.text}")
        
        if post_response.status_code in [200, 201]:
            print("✅ Sponsorship request creation API working correctly")
        else:
            print(f"❌ Sponsorship request creation failed. Status: {post_response.status_code}")
            return False
        
        # Try to get sponsorship requests
        print(f"Sending GET request to {api_url}")
        get_response = requests.get(api_url)
        
        print(f"GET response status: {get_response.status_code}")
        print(f"GET response body: {get_response.text[:500]}...")
        
        if get_response.status_code == 200:
            sponsorships = get_response.json()
            print(f"✅ Sponsorship listing API working correctly. Found {len(sponsorships) if isinstance(sponsorships, list) else 'some'} sponsorships.")
            return True
        else:
            print(f"❌ Getting sponsorships failed. Status: {get_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Sponsorship system test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_sponsorship_system()
    sys.exit(0 if success else 1)
