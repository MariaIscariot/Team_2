#!/usr/bin/env python3
"""
Test script for the new /send-message endpoint
"""

import requests
import json

def test_send_message():
    """Test the send-message endpoint"""
    
    # API endpoint
    url = "http://localhost:5000/send-message"
    
    # Test data
    test_data = {
        "recipients": [
            "akononciuc@gmail.com",
            "gabrielapr2140@gmail.com"
        ],
        "message": "This is a test message from the new /send-message endpoint. Please confirm if you received this email."
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing /send-message endpoint...")
    print(f"📧 Recipients: {test_data['recipients']}")
    print(f"💬 Message: {test_data['message']}")
    print("=" * 60)
    
    try:
        # Make the request
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # Parse response
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"📄 Response Body:")
            print(json.dumps(result, indent=2))
        else:
            print(f"📄 Response Text: {response.text}")
        
        # Check if successful
        if response.status_code in [200, 207]:
            print("✅ Test completed successfully!")
            if response.status_code == 200:
                print("🎉 All emails sent successfully!")
            elif response.status_code == 207:
                print("⚠️  Some emails failed to send (partial success)")
        else:
            print("❌ Test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_invalid_data():
    """Test the endpoint with invalid data"""
    
    url = "http://localhost:5000/send-message"
    headers = {"Content-Type": "application/json"}
    
    print("\n🧪 Testing with invalid data...")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        {
            "name": "Missing recipients",
            "data": {"message": "Test message"},
            "expected_status": 400
        },
        {
            "name": "Missing message",
            "data": {"recipients": ["test@example.com"]},
            "expected_status": 400
        },
        {
            "name": "Empty recipients array",
            "data": {"recipients": [], "message": "Test"},
            "expected_status": 400
        },
        {
            "name": "Invalid email format",
            "data": {"recipients": ["invalid-email"], "message": "Test"},
            "expected_status": 400
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        try:
            response = requests.post(url, json=test_case['data'], headers=headers)
            print(f"   Status: {response.status_code} (expected: {test_case['expected_status']})")
            
            if response.status_code == test_case['expected_status']:
                print("   ✅ Passed")
            else:
                print("   ❌ Failed")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting /send-message endpoint tests...")
    print("=" * 60)
    
    # Test valid data
    test_send_message()
    
    # Test invalid data
    test_invalid_data()
    
    print("\n🏁 All tests completed!") 