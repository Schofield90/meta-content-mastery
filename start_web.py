#!/usr/bin/env python3
"""
Startup script for Meta Content Manager Web Interface
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import requests
        import aiohttp
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are set"""
    app_id = os.getenv('META_APP_ID')
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    if not app_id:
        print("⚠️  META_APP_ID not found in environment")
    else:
        print(f"✅ META_APP_ID: {app_id}")
    
    if not access_token:
        print("⚠️  META_ACCESS_TOKEN not found in environment")
        print("Please set your access token in the .env file")
    else:
        print("✅ META_ACCESS_TOKEN is set")
    
    return bool(app_id and access_token)

def main():
    print("🚀 Starting Meta Content Manager...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  Some environment variables are missing.")
        print("The app will start but some features may not work.")
        print("Please check your .env file.")
    
    print("\n" + "=" * 50)
    print("🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the web app
    try:
        from web_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()