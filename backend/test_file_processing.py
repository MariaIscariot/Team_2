#!/usr/bin/env python3
"""
Test script to verify file processing functionality
"""

import os
import sys
import json
import requests

def test_file_processing():
    """Test the file processing endpoint"""
    
    # Test with a real attachment file
    test_filepath = "attachments/CV_Cononciuc_Alina_Analyst_Rose_EN_1.pdf"
    
    # Check if file exists
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_filepath = os.path.join(backend_dir, test_filepath)
    
    print(f"Testing with file: {absolute_filepath}")
    print(f"File exists: {os.path.exists(absolute_filepath)}")
    
    # Test the API endpoint
    url = "http://localhost:5000/process-file-by-path"
    payload = {
        "filepath": test_filepath
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File processing successful!")
            print(f"Results: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ File processing failed!")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_file_processing() 