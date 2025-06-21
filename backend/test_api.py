#!/usr/bin/env python3
"""
Test script for the File Analysis API
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:5000"

def test_home():
    """Test the home endpoint"""
    print("Testing home endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_process_file():
    """Test file processing endpoint"""
    print("Testing process-file endpoint...")
    
    # Check if there are any files in attachments folder (parent directory)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    attachments_dir = os.path.join(parent_dir, "attachments")
    
    if os.path.exists(attachments_dir):
        files = [f for f in os.listdir(attachments_dir) if f.endswith(('.pdf', '.docx', '.txt', '.xlsx'))]
        if files:
            test_file = os.path.join(attachments_dir, files[0])
            print(f"Using test file: {test_file}")
            
            with open(test_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{BASE_URL}/process-file", files=files)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
        else:
            print("No test files found in attachments directory")
    else:
        print("Attachments directory not found")
    print()

def test_analyze_json():
    """Test JSON analysis endpoint"""
    print("Testing analyze-json endpoint...")
    
    test_data = {
        "filename": "test_document.pdf",
        "type": "CV",
        "summary": "Test document summary",
        "entities": [
            {"text": "John Doe", "label": "PERSON"},
            {"text": "Software Engineer", "label": "WORK_OF_ART"}
        ],
        "full_text": "This is a test document content for analysis."
    }
    
    response = requests.post(f"{BASE_URL}/analyze-json", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_file_analysis():
    """Test file analysis endpoint"""
    print("Testing file-analysis endpoint...")
    
    test_data = {
        "filename": "test_document.pdf",
        "type": "CV",
        "summary": "Test document summary",
        "entities": [
            {"text": "John Doe", "label": "PERSON"},
            {"text": "Software Engineer", "label": "WORK_OF_ART"}
        ],
        "full_text": "This is a test document content for analysis."
    }
    
    response = requests.post(f"{BASE_URL}/file-analysis", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_load_emails():
    """Test load emails endpoint"""
    print("Testing load-emails endpoint...")
    
    response = requests.get(f"{BASE_URL}/load-emails")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_summarize_conversation():
    """Test conversation summary endpoint"""
    print("Testing summarize-conversation endpoint...")
    
    test_data = {
        "id": "1",
        "subject": "Test conversation",
        "from": "test@example.com",
        "body": "This is a test conversation for summarization."
    }
    
    response = requests.post(f"{BASE_URL}/summarize-conversation", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_generate_response():
    """Test response generation endpoint"""
    print("Testing generate-response endpoint...")
    
    test_data = {
        "id": "1",
        "subject": "Test message",
        "from": "test@example.com",
        "body": "This is a test message for response generation."
    }
    
    response = requests.post(f"{BASE_URL}/generate-response", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("=== File Analysis API Test Suite ===")
    print("Running from backend directory...")
    print()
    
    try:
        test_home()
        test_health()
        test_process_file()
        test_analyze_json()
        test_file_analysis()
        test_load_emails()
        test_summarize_conversation()
        test_generate_response()
        
        print("=== All tests completed ===")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 