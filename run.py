#!/usr/bin/env python3
"""
SmartLearn Application Startup Script
This script provides a safe way to start the SmartLearn application with proper error handling.
"""

import sys
import logging
import traceback
from config import Config

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import flask
        print("✓ Flask is available")
    except ImportError:
        missing_deps.append("flask")
        print("✗ Flask is missing")
    
    try:
        import yt_dlp
        print("✓ yt-dlp is available")
    except ImportError:
        missing_deps.append("yt-dlp")
        print("✗ yt-dlp is missing")
    
    try:
        import requests
        print("✓ requests is available")
    except ImportError:
        missing_deps.append("requests")
        print("✗ requests is missing")
    
    # Optional AI dependencies
    try:
        import transformers
        print("✓ transformers is available (AI features enabled)")
    except ImportError:
        print("⚠ transformers is missing (AI features will be disabled)")
    
    try:
        import torch
        print("✓ PyTorch is available")
    except ImportError:
        print("⚠ PyTorch is missing (AI features may not work)")
    
    if missing_deps:
        print(f"\nMissing required dependencies: {', '.join(missing_deps)}")
        print("Please install them using: pip install -r newreqirements.txt")
        return False
    
    return True

def main():
    """Main startup function"""
    print("=" * 50)
    print("SmartLearn Application Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nConfiguration:")
    print(f"  - AI Classification: {'Enabled' if Config.ENABLE_AI_CLASSIFICATION else 'Disabled'}")
    print(f"  - Ollama Integration: {'Enabled' if Config.ENABLE_OLLAMA else 'Disabled'}")
    print(f"  - Community Features: {'Enabled' if Config.ENABLE_COMMUNITY_FEATURES else 'Disabled'}")
    print(f"  - Database: {Config.SQLALCHEMY_DATABASE_URI}")
    
    print("\nStarting application...")
    
    try:
        # Import and run the app
        from app import app
        
        print("✓ Application loaded successfully")
        print("✓ Database initialized")
        print("✓ Routes registered")
        
        print("\n" + "=" * 50)
        print("SmartLearn is running!")
        print("Access the application at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"\n✗ Failed to start application: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 