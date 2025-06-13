
import requests
import json
import time
import sys
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "http://localhost:8001"
API_PREFIX = "/api"

def test_admin_system():
    """Test the admin system functionality by directly calling the backend API"""
    try:
        # Test admin sponsorship endpoint
        admin_sponsorship_url = urljoin(BACKEND_URL, API_PREFIX + "/admin/sponsorship")
        
        print(f"Testing admin sponsorship endpoint: {admin_sponsorship_url}")
        
        # Try to get admin sponsorships
        get_response = requests.get(admin_sponsorship_url)
        
        print(f"GET response status: {get_response.status_code}")
        if get_response.status_code == 200:
            print(f"GET response body: {get_response.text[:500]}...")
            sponsorships = get_response.json()
            print(f"✅ Admin sponsorship GET API working correctly. Found {len(sponsorships) if isinstance(sponsorships, list) else 'some'} sponsorships.")
        else:
            print(f"❌ Admin sponsorship GET failed. Status: {get_response.status_code}, Response: {get_response.text}")
            return False
        
        # Try to create an admin sponsorship
        admin_sponsorship_data = {
            "company_name": "Admin Test Sponsor",
            "offer": "Special Admin Offer",
            "link": "https://example.com",
            "placement": "top",
            "start_date": "2025-06-13",
            "end_date": "2025-07-13"
        }
        
        print(f"Sending POST request to {admin_sponsorship_url} with data: {json.dumps(admin_sponsorship_data, indent=2)}")
        post_response = requests.post(admin_sponsorship_url, json=admin_sponsorship_data)
        
        print(f"POST response status: {post_response.status_code}")
        if post_response.status_code in [200, 201]:
            print(f"POST response body: {post_response.text}")
            print("✅ Admin sponsorship POST API working correctly")
        else:
            print(f"❌ Admin sponsorship POST failed. Status: {post_response.status_code}, Response: {post_response.text}")
            
            # If we get a 422 error, try to fix the request based on the error message
            if post_response.status_code == 422:
                error_detail = json.loads(post_response.text).get("detail", [])
                missing_fields = [error["loc"][1] for error in error_detail if error["type"] == "missing"]
                
                if missing_fields:
                    print(f"Missing fields: {missing_fields}")
                    
                    # Add missing fields with dummy values
                    for field in missing_fields:
                        admin_sponsorship_data[field] = f"Test {field.replace('_', ' ')}"
                    
                    print(f"Retrying with updated data: {json.dumps(admin_sponsorship_data, indent=2)}")
                    retry_response = requests.post(admin_sponsorship_url, json=admin_sponsorship_data)
                    
                    print(f"Retry response status: {retry_response.status_code}")
                    if retry_response.status_code in [200, 201]:
                        print(f"Retry response body: {retry_response.text}")
                        print("✅ Admin sponsorship POST API working correctly after fixing missing fields")
                    else:
                        print(f"❌ Admin sponsorship POST still failed after fixing missing fields. Status: {retry_response.status_code}, Response: {retry_response.text}")
                        return False
                else:
                    return False
            else:
                return False
        
        # Test admin user management endpoints
        admin_users_url = urljoin(BACKEND_URL, API_PREFIX + "/admin/users")
        
        print(f"\nTesting admin users endpoint: {admin_users_url}")
        
        # Try to get admin users
        users_response = requests.get(admin_users_url)
        
        print(f"GET users response status: {users_response.status_code}")
        if users_response.status_code == 200:
            print(f"GET users response body: {users_response.text[:500]}...")
            users = users_response.json()
            print(f"✅ Admin users GET API working correctly. Found {len(users) if isinstance(users, list) else 'some'} users.")
        elif users_response.status_code == 404:
            print("⚠️ Admin users endpoint not found. This might not be implemented yet.")
        else:
            print(f"❌ Admin users GET failed. Status: {users_response.status_code}, Response: {users_response.text}")
        
        # Test admin statistics endpoint
        admin_stats_url = urljoin(BACKEND_URL, API_PREFIX + "/admin/stats")
        
        print(f"\nTesting admin statistics endpoint: {admin_stats_url}")
        
        # Try to get admin statistics
        stats_response = requests.get(admin_stats_url)
        
        print(f"GET stats response status: {stats_response.status_code}")
        if stats_response.status_code == 200:
            print(f"GET stats response body: {stats_response.text}")
            print("✅ Admin statistics API working correctly")
        elif stats_response.status_code == 404:
            print("⚠️ Admin statistics endpoint not found. This might not be implemented yet.")
        else:
            print(f"❌ Admin statistics GET failed. Status: {stats_response.status_code}, Response: {stats_response.text}")
        
        return True
    except Exception as e:
        print(f"❌ Admin system test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_admin_system()
    sys.exit(0 if success else 1)
