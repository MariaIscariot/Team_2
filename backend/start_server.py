#!/usr/bin/env python3
"""
Startup script for the File Analysis API server
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy model if not already installed"""
    print("Checking spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model already installed")
    except OSError:
        print("Downloading spaCy model...")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("✅ spaCy model downloaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download spaCy model: {e}")
            return False
    return True

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🚀 File Analysis API Server Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the backend directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Download spaCy model
    if not download_spacy_model():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 