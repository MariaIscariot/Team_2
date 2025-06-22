#!/usr/bin/env python3
"""
Test script to verify encoding fixes
"""

import os
import sys
import subprocess

def test_encoding():
    """Test the encoding fixes"""
    
    # Test with a file that has non-ASCII characters in the path
    test_filepath = "attachments/1 июня_fe55cec7-f0bd-4f3c-a081-0720ccd36e02_1.docx"
    
    # Check if file exists
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_filepath = os.path.join(backend_dir, test_filepath)
    
    print(f"Testing with file: {absolute_filepath}")
    print(f"File exists: {os.path.exists(absolute_filepath)}")
    
    # Test the main.py script directly
    main_script = os.path.join(os.path.dirname(backend_dir), 'main.py')
    
    # Set environment variables for proper encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run([sys.executable, main_script], 
                              input=absolute_filepath + '\n', 
                              text=True, 
                              capture_output=True,
                              env=env,
                              encoding='utf-8')
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Encoding test successful!")
        else:
            print("❌ Encoding test failed!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_encoding() 