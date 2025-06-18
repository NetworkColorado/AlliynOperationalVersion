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

def test_create_sponsorship_request():
    """Test creating a sponsorship request"""
    # Create a unique sponsorship request
    company_name = f"TestCompany-{uuid.uuid4()}"
    payload = {
        "company_name": company_name,
        "contact_name": "Test Contact",
        "email": "test@example.com",
        "phone": "555-123-4567",
        "website": "https://example.com",
        "industry": "Technology",
        "package_type": "Premium",
        "budget": "$1,500-$2,000",
        "goals": "Increase brand visibility",
        "additional_info": "Test sponsorship request"
    }
    
    response = requests.post(f"{BACKEND_URL}/sponsorship", json=payload)
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "company_name" in data, "Response missing 'company_name' field"
    assert "estimated_quote" in data, "Response missing 'estimated_quote' field"
    assert data["company_name"] == company_name, f"Expected company_name '{company_name}', got '{data['company_name']}'"
    
    # Verify industry multiplier was applied (Technology has 1.2 multiplier)
    assert data["estimated_quote"] == 1800, f"Expected estimated_quote 1800 (1500 * 1.2), got {data['estimated_quote']}"
    
    print("Created sponsorship request:", data)
    return True

def test_get_sponsorship_requests():
    """Test retrieving all sponsorship requests"""
    # First create a new sponsorship request to ensure there's at least one
    company_name = f"TestCompany-{uuid.uuid4()}"
    payload = {
        "company_name": company_name,
        "contact_name": "Test Contact",
        "email": "test@example.com",
        "industry": "Financial Services",
        "package_type": "Basic",
        "goals": "Increase brand visibility"
    }
    
    create_response = requests.post(f"{BACKEND_URL}/sponsorship", json=payload)
    assert create_response.status_code == 200, "Failed to create test sponsorship request"
    
    # Now get all sponsorship requests
    response = requests.get(f"{BACKEND_URL}/sponsorship")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Expected at least one sponsorship request"
    
    # Check if our newly created sponsorship request is in the list
    found = False
    for request in data:
        if request["company_name"] == company_name:
            found = True
            break
    
    assert found, f"Newly created sponsorship request with company_name '{company_name}' not found in response"
    
    print(f"Retrieved {len(data)} sponsorship requests")
    return True

def test_sponsorship_stats():
    """Test sponsorship statistics endpoint"""
    response = requests.get(f"{BACKEND_URL}/sponsorship/stats")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "total_requests" in data, "Response missing 'total_requests' field"
    assert "industry_breakdown" in data, "Response missing 'industry_breakdown' field"
    assert "package_breakdown" in data, "Response missing 'package_breakdown' field"
    
    # Verify data types
    assert isinstance(data["total_requests"], int), "total_requests is not an integer"
    assert isinstance(data["industry_breakdown"], list), "industry_breakdown is not a list"
    assert isinstance(data["package_breakdown"], list), "package_breakdown is not a list"
    
    print("Sponsorship stats:", data)
    return True

def test_admin_sponsorship():
    """Test admin sponsorship creation and retrieval"""
    # Create a unique admin sponsorship
    business_name = f"AdminTestBusiness-{uuid.uuid4()}"
    payload = {
        "business_name": business_name,
        "offer_name": "Test Offer",
        "offer": "50% off for new customers",
        "website": "https://example.com",
        "logo_url": "https://example.com/logo.png",
        "media_url": "https://example.com/video.mp4",
        "release_date": "2025-01-01",
        "release_time": "12:00"
    }
    
    response = requests.post(f"{BACKEND_URL}/admin/sponsorship", json=payload)
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "business_name" in data, "Response missing 'business_name' field"
    assert data["business_name"] == business_name, f"Expected business_name '{business_name}', got '{data['business_name']}'"
    
    # Now get all admin sponsorships
    response = requests.get(f"{BACKEND_URL}/admin/sponsorship")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Expected at least one admin sponsorship"
    
    # Check if our newly created admin sponsorship is in the list
    found = False
    for sponsorship in data:
        if sponsorship["business_name"] == business_name:
            found = True
            break
    
    assert found, f"Newly created admin sponsorship with business_name '{business_name}' not found in response"
    
    print(f"Retrieved {len(data)} admin sponsorships")
    return True

def test_admin_user_management():
    """Test admin user management endpoints"""
    # Generate a unique user ID
    user_id = str(uuid.uuid4())
    
    # Test user upgrade
    response = requests.post(f"{BACKEND_URL}/admin/user/{user_id}/upgrade")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "user_id" in data, "Response missing 'user_id' field"
    assert "account_type" in data, "Response missing 'account_type' field"
    assert data["user_id"] == user_id, f"Expected user_id '{user_id}', got '{data['user_id']}'"
    assert data["account_type"] == "premium", f"Expected account_type 'premium', got '{data['account_type']}'"
    
    # Test user downgrade
    response = requests.post(f"{BACKEND_URL}/admin/user/{user_id}/downgrade")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "user_id" in data, "Response missing 'user_id' field"
    assert "account_type" in data, "Response missing 'account_type' field"
    assert data["user_id"] == user_id, f"Expected user_id '{user_id}', got '{data['user_id']}'"
    assert data["account_type"] == "free", f"Expected account_type 'free', got '{data['account_type']}'"
    
    # Test user deletion
    response = requests.delete(f"{BACKEND_URL}/admin/user/{user_id}")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "user_id" in data, "Response missing 'user_id' field"
    assert "status" in data, "Response missing 'status' field"
    assert data["user_id"] == user_id, f"Expected user_id '{user_id}', got '{data['user_id']}'"
    assert data["status"] == "deleted", f"Expected status 'deleted', got '{data['status']}'"
    
    print("Admin user management tests passed")
    return True

def test_admin_stats():
    """Test admin statistics endpoint"""
    response = requests.get(f"{BACKEND_URL}/admin/stats")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "total_sponsorships" in data, "Response missing 'total_sponsorships' field"
    assert "total_sponsorship_requests" in data, "Response missing 'total_sponsorship_requests' field"
    assert "total_users" in data, "Response missing 'total_users' field"
    assert "premium_users" in data, "Response missing 'premium_users' field"
    assert "free_users" in data, "Response missing 'free_users' field"
    
    # Verify data types
    assert isinstance(data["total_sponsorships"], int), "total_sponsorships is not an integer"
    assert isinstance(data["total_sponsorship_requests"], int), "total_sponsorship_requests is not an integer"
    
    print("Admin stats:", data)
    return True

def test_create_conversation():
    """Test creating a conversation"""
    # Generate unique user IDs
    sender_id = "user"
    recipient_id = f"recipient-{uuid.uuid4()}"
    
    payload = {
        "recipient_id": recipient_id,
        "recipient_name": "Test Recipient"
    }
    
    response = requests.post(f"{BACKEND_URL}/conversations", json=payload)
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "participants" in data, "Response missing 'participants' field"
    assert "participant_names" in data, "Response missing 'participant_names' field"
    
    # Verify participants
    assert sender_id in data["participants"], f"Sender ID '{sender_id}' not in participants"
    assert recipient_id in data["participants"], f"Recipient ID '{recipient_id}' not in participants"
    
    # Store conversation ID for later tests
    conversation_id = data["id"]
    print(f"Created conversation with ID: {conversation_id}")
    return True, conversation_id

def test_get_conversations():
    """Test retrieving all conversations for a user"""
    # First create a new conversation to ensure there's at least one
    success, _ = test_create_conversation()
    assert success, "Failed to create test conversation"
    
    # Now get all conversations
    response = requests.get(f"{BACKEND_URL}/conversations?user_id=user")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Expected at least one conversation"
    
    # Verify structure of each conversation
    for conversation in data:
        assert "id" in conversation, "Conversation missing 'id' field"
        assert "participants" in conversation, "Conversation missing 'participants' field"
        assert "participant_names" in conversation, "Conversation missing 'participant_names' field"
        assert "user" in conversation["participants"], "User not in participants"
    
    print(f"Retrieved {len(data)} conversations")
    return True

def test_send_message():
    """Test sending a message"""
    # First create a new conversation
    success, conversation_id = test_create_conversation()
    assert success, "Failed to create test conversation"
    
    # Now send a message
    message_content = f"Test message {uuid.uuid4()}"
    payload = {
        "recipient_id": "recipient",
        "content": message_content,
        "message_type": "text"
    }
    
    response = requests.post(f"{BACKEND_URL}/messages", json=payload)
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "conversation_id" in data, "Response missing 'conversation_id' field"
    assert "sender_id" in data, "Response missing 'sender_id' field"
    assert "content" in data, "Response missing 'content' field"
    assert data["content"] == message_content, f"Expected content '{message_content}', got '{data['content']}'"
    
    # Store message ID and conversation ID for later tests
    message_id = data["id"]
    conversation_id = data["conversation_id"]
    print(f"Sent message with ID: {message_id} in conversation: {conversation_id}")
    return True, message_id, conversation_id

def test_get_messages():
    """Test retrieving messages for a conversation"""
    # First send a message to ensure there's at least one
    success, _, conversation_id = test_send_message()
    assert success, "Failed to send test message"
    
    # Now get all messages for the conversation
    response = requests.get(f"{BACKEND_URL}/messages/{conversation_id}")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Expected at least one message"
    
    # Verify structure of each message
    for message in data:
        assert "id" in message, "Message missing 'id' field"
        assert "conversation_id" in message, "Message missing 'conversation_id' field"
        assert "sender_id" in message, "Message missing 'sender_id' field"
        assert "content" in message, "Message missing 'content' field"
        assert message["conversation_id"] == conversation_id, f"Expected conversation_id '{conversation_id}', got '{message['conversation_id']}'"
    
    print(f"Retrieved {len(data)} messages for conversation {conversation_id}")
    return True

def test_mark_message_read():
    """Test marking a message as read"""
    # First send a message to get a message ID
    success, message_id, _ = test_send_message()
    assert success, "Failed to send test message"
    
    # Now mark the message as read
    response = requests.put(f"{BACKEND_URL}/messages/{message_id}/read")
    
    # Verify status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Verify response content
    data = response.json()
    assert "status" in data, "Response missing 'status' field"
    assert data["status"] == "Message marked as read", f"Expected status 'Message marked as read', got '{data['status']}'"
    
    print(f"Marked message {message_id} as read")
    return True

import websocket
import threading
import time

def test_websocket_connection():
    """Test WebSocket connection"""
    try:
        # Generate a unique user ID
        user_id = f"ws-user-{uuid.uuid4()}"
        
        # Create a WebSocket connection
        ws_url = f"ws://localhost:8001/ws/{user_id}"
        
        # Flag to track if we received a message
        received_message = False
        
        def on_message(ws, message):
            nonlocal received_message
            print(f"Received message: {message}")
            assert "Echo:" in message, f"Expected 'Echo:' in message, got '{message}'"
            received_message = True
        
        def on_error(ws, error):
            print(f"WebSocket error: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print(f"WebSocket closed: {close_status_code} - {close_msg}")
        
        def on_open(ws):
            print(f"WebSocket connection opened for user {user_id}")
            # Send a test message
            test_message = f"Test message {uuid.uuid4()}"
            print(f"Sending message: {test_message}")
            ws.send(test_message)
        
        # Create WebSocket connection
        ws = websocket.WebSocketApp(ws_url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        
        # Start WebSocket connection in a separate thread
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Wait for the message to be received
        timeout = 5  # seconds
        start_time = time.time()
        while not received_message and time.time() - start_time < timeout:
            time.sleep(0.1)
        
        # Close the WebSocket connection
        ws.close()
        
        # Wait for the thread to finish
        wst.join(timeout=1)
        
        assert received_message, "Did not receive echo message from WebSocket"
        
        print("WebSocket connection test passed")
        return True
    except Exception as e:
        print(f"WebSocket test failed: {str(e)}")
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
        ("Create Sponsorship Request", test_create_sponsorship_request),
        ("Get Sponsorship Requests", test_get_sponsorship_requests),
        ("Sponsorship Stats", test_sponsorship_stats),
        ("Admin Sponsorship", test_admin_sponsorship),
        ("Admin User Management", test_admin_user_management),
        ("Admin Stats", test_admin_stats),
        ("Create Conversation", lambda: test_create_conversation()[0]),
        ("Get Conversations", test_get_conversations),
        ("Send Message", lambda: test_send_message()[0]),
        ("Get Messages", test_get_messages),
        ("Mark Message Read", test_mark_message_read),
        ("WebSocket Connection", test_websocket_connection),
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
