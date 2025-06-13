#!/usr/bin/env python3
import requests
import json
import uuid
import time
from datetime import datetime
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys

# Load environment variables from backend/.env
load_dotenv('/app/backend/.env')

# Configuration
BACKEND_URL = "http://localhost:8001/api"
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

print(f"Testing backend at: {BACKEND_URL}")
print(f"MongoDB connection: {MONGO_URL}")
print(f"Database name: {DB_NAME}")

# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def run_test(test_name, test_func):
    """Run a test and track results"""
    test_results["total"] += 1
    print(f"\n{'='*80}\nRunning test: {test_name}\n{'='*80}")
    
    try:
        result = test_func()
        if result:
            test_results["passed"] += 1
            test_results["tests"].append({"name": test_name, "status": "PASSED"})
            print(f"✅ Test PASSED: {test_name}")
            return True
        else:
            test_results["failed"] += 1
            test_results["tests"].append({"name": test_name, "status": "FAILED"})
            print(f"❌ Test FAILED: {test_name}")
            return False
    except Exception as e:
        test_results["failed"] += 1
        test_results["tests"].append({"name": test_name, "status": "FAILED", "error": str(e)})
        print(f"❌ Test FAILED with exception: {test_name}")
        print(f"Error: {str(e)}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BACKEND_URL}/")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "message" in data, "Response missing 'message' field"
    assert data["message"] == "Hello World", f"Expected 'Hello World', got '{data['message']}'"
    
    print("Health check endpoint returned:", data)
    return True

def test_create_status_check():
    """Test creating a status check"""
    client_name = f"TestClient-{uuid.uuid4()}"
    payload = {"client_name": client_name}
    
    response = requests.post(f"{BACKEND_URL}/status", json=payload)
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "client_name" in data, "Response missing 'client_name' field"
    assert "timestamp" in data, "Response missing 'timestamp' field"
    assert data["client_name"] == client_name, f"Expected client_name '{client_name}', got '{data['client_name']}'"
    
    # Verify UUID format
    try:
        uuid_obj = uuid.UUID(data["id"])
        assert str(uuid_obj) == data["id"], "ID is not a valid UUID string"
    except ValueError:
        assert False, f"ID '{data['id']}' is not a valid UUID"
    
    # Verify timestamp format (ISO format)
    try:
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
    except ValueError:
        assert False, f"Timestamp '{data['timestamp']}' is not in ISO format"
    
    print("Created status check:", data)
    return True

def test_get_status_checks():
    """Test retrieving all status checks"""
    # First create a new status check to ensure there's at least one
    client_name = f"TestClient-{uuid.uuid4()}"
    payload = {"client_name": client_name}
    create_response = requests.post(f"{BACKEND_URL}/status", json=payload)
    assert create_response.status_code == 200, "Failed to create test status check"
    
    # Now get all status checks
    response = requests.get(f"{BACKEND_URL}/status")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Expected at least one status check"
    
    # Verify structure of each status check
    for status in data:
        assert "id" in status, "Status check missing 'id' field"
        assert "client_name" in status, "Status check missing 'client_name' field"
        assert "timestamp" in status, "Status check missing 'timestamp' field"
        
        # Verify UUID format
        try:
            uuid_obj = uuid.UUID(status["id"])
            assert str(uuid_obj) == status["id"], "ID is not a valid UUID string"
        except ValueError:
            assert False, f"ID '{status['id']}' is not a valid UUID"
        
        # Verify timestamp format (ISO format)
        try:
            datetime.fromisoformat(status["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            assert False, f"Timestamp '{status['timestamp']}' is not in ISO format"
    
    # Check if our newly created status check is in the list
    found = False
    for status in data:
        if status["client_name"] == client_name:
            found = True
            break
    
    assert found, f"Newly created status check with client_name '{client_name}' not found in response"
    
    print(f"Retrieved {len(data)} status checks")
    return True

def test_error_handling():
    """Test error handling for invalid inputs"""
    # Test missing required field
    response = requests.post(f"{BACKEND_URL}/status", json={})
    assert response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid input, got {response.status_code}"
    
    # Test invalid JSON
    response = requests.post(f"{BACKEND_URL}/status", data="invalid json", headers={"Content-Type": "application/json"})
    assert response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid JSON, got {response.status_code}"
    
    print("Error handling tests passed")
    return True

def test_cors_headers():
    """Test CORS headers"""
    # Use a regular GET request with Origin header to test CORS
    headers = {"Origin": "http://localhost:3000"}
    response = requests.get(f"{BACKEND_URL}/", headers=headers)
    
    # Check for CORS headers
    assert "Access-Control-Allow-Origin" in response.headers, "Missing CORS header: Access-Control-Allow-Origin"
    
    # Print all headers for debugging
    print("Response headers:", response.headers)
    
    print("CORS headers present in response")
    return True

def test_mongodb_connection():
    """Test direct MongoDB connection and data persistence"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Generate unique client name
        client_name = f"MongoTest-{uuid.uuid4()}"
        
        # Insert a document directly
        doc_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        db.status_checks.insert_one({
            "id": doc_id,
            "client_name": client_name,
            "timestamp": timestamp
        })
        
        # Verify document was inserted
        found_doc = db.status_checks.find_one({"id": doc_id})
        assert found_doc is not None, "Document not found in MongoDB"
        assert found_doc["client_name"] == client_name, f"Expected client_name '{client_name}', got '{found_doc['client_name']}'"
        
        # Now verify we can retrieve it through the API
        response = requests.get(f"{BACKEND_URL}/status")
        assert response.status_code == 200, "Failed to get status checks from API"
        
        data = response.json()
        found_in_api = False
        for status in data:
            if status["id"] == doc_id:
                found_in_api = True
                assert status["client_name"] == client_name, f"API returned wrong client_name: {status['client_name']}"
                break
        
        assert found_in_api, f"Document with id '{doc_id}' not found in API response"
        
        # Clean up - remove the test document
        db.status_checks.delete_one({"id": doc_id})
        
        print("MongoDB connection and data persistence verified")
        return True
    
    except Exception as e:
        print(f"MongoDB connection test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    tests = [
        ("Health Check Endpoint", test_health_check),
        ("Create Status Check", test_create_status_check),
        ("Get Status Checks", test_get_status_checks),
        ("Error Handling", test_error_handling),
        ("CORS Headers", test_cors_headers),
        ("MongoDB Connection", test_mongodb_connection),
    ]
    
    for test_name, test_func in tests:
        run_test(test_name, test_func)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY: {test_results['passed']}/{test_results['total']} tests passed")
    print(f"{'='*80}")
    
    for test in test_results["tests"]:
        status_symbol = "✅" if test["status"] == "PASSED" else "❌"
        print(f"{status_symbol} {test['name']}: {test['status']}")
        if "error" in test:
            print(f"   Error: {test['error']}")
    
    print(f"{'='*80}")
    
    # Return True if all tests passed
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
