#!/usr/bin/env python3
"""
Diagnostic script to identify common setup issues
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check")
    print(f"   Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("   ❌ Python 3.8+ required")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Dependencies Check")
    required_packages = [
        'flask', 'pandas', 'fitz', 'docx', 'spacy', 'groq', 'openpyxl'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n   Install missing packages: pip install {' '.join(missing)}")
        return False
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 File Structure Check")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'start_server.py',
        '../main.py',
        '../analysis.py',
        'attachments/'
    ]
    
    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            missing.append(file_path)
    
    if missing:
        print(f"\n   Missing files: {missing}")
        return False
    return True

def check_spacy_model():
    """Check if spaCy model is installed"""
    print("\n🧠 spaCy Model Check")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("   ✅ en_core_web_sm model installed")
        return True
    except OSError:
        print("   ❌ en_core_web_sm model missing")
        print("   Install with: python -m spacy download en_core_web_sm")
        return False

def check_port_availability():
    """Check if port 5000 is available"""
    print("\n🌐 Port Availability Check")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("   ❌ Port 5000 is in use")
            return False
        else:
            print("   ✅ Port 5000 is available")
            return True
    except Exception as e:
        print(f"   ⚠️ Could not check port: {e}")
        return True

def check_encoding():
    """Check encoding settings"""
    print("\n🔤 Encoding Check")
    encoding = os.environ.get('PYTHONIOENCODING', 'Not set')
    print(f"   PYTHONIOENCODING: {encoding}")
    
    if encoding == 'utf-8':
        print("   ✅ UTF-8 encoding set")
        return True
    else:
        print("   ⚠️ UTF-8 encoding not set (may cause issues)")
        return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Basic Functionality Test")
    
    # Test file processing
    test_file = "attachments/Hotels_1.xlsx"
    if os.path.exists(test_file):
        try:
            import pandas as pd
            df = pd.read_excel(test_file)
            print(f"   ✅ Excel file reading: {df.shape[0]} rows, {df.shape[1]} columns")
        except Exception as e:
            print(f"   ❌ Excel file reading failed: {e}")
            return False
    else:
        print(f"   ⚠️ Test file not found: {test_file}")
    
    return True

def main():
    """Run all diagnostic checks"""
    print("🔍 Backend Setup Diagnostic")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_file_structure(),
        check_spacy_model(),
        check_port_availability(),
        check_encoding(),
        test_basic_functionality()
    ]
    
    print("\n" + "=" * 50)
    print("📊 Summary")
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All {total} checks passed! Backend should work.")
        print("\n🚀 Try starting the server:")
        print("   python start_server.py")
    else:
        print(f"❌ {total - passed} out of {total} checks failed.")
        print("\n🔧 Fix the issues above before starting the server.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 