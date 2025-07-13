#!/usr/bin/env python3
"""
Vintelli Startup Script
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\n📝 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        print("\n🔑 Get your API key from: https://platform.openai.com/api-keys")
        return False
    
    # Load and check the .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not set in .env file!")
        print("\n📝 Please update your .env file with a valid API key:")
        print("   OPENAI_API_KEY=sk-your-actual-api-key-here")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Vintelli...")
    print("=" * 40)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Try to import and run the app
    try:
        from app import app
        print("✅ Flask app loaded successfully")
        print("\n🌐 Starting server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("\n" + "=" * 40)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        print("\n💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 