#!/usr/bin/env python3
"""
Test script for the summarize-conversation endpoint
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_summarize_conversation():
    """Test the summarize-conversation endpoint with correct headers"""
    
    # Test data
    test_data = {
        "id": "11",
        "folder": "INBOX",
        "subject": "Re: Welcome message from Veltrix Foods",
        "from": "Алина Конончук <akononciuc@gmail.com>",
        "to": "Dimas Pro <test.server.composer@gmail.com>",
        "date": "Sat, 21 Jun 2025 18:26:59 +0300",
        "body": "Dear Dimas Pro,\r\n\r\nI think it's perfect!\r\nLet's schedule the meeting on wednesday 25.06.2025 at 4 pm.\r\n\r\nPlease let us know if this works for you.\r\n\r\nBest regards,\r\nMaria Iscariot\r\nProcurement Manager\r\nVeltrix Foods"
    }
    
    # Headers with Content-Type
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing summarize-conversation endpoint...")
    print(f"URL: {BASE_URL}/summarize-conversation")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        # Make the request with proper headers
        response = requests.post(
            f"{BASE_URL}/summarize-conversation",
            headers=headers,
            json=test_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Success! Request worked correctly.")
        else:
            print(f"\n❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

def test_without_content_type():
    """Test what happens without Content-Type header"""
    
    test_data = {
        "id": "11",
        "subject": "Test conversation",
        "from": "test@example.com",
        "body": "This is a test conversation for summarization."
    }
    
    print("\n" + "="*60)
    print("Testing WITHOUT Content-Type header (this should fail)...")
    print(f"URL: {BASE_URL}/summarize-conversation")
    print("Headers: None")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        # Make the request WITHOUT proper headers
        response = requests.post(
            f"{BASE_URL}/summarize-conversation",
            json=test_data  # This will set Content-Type automatically
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_summarize_conversation()
    test_without_content_type() 