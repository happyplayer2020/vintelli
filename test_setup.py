#!/usr/bin/env python3
"""
Test script to verify Vintelli setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'flask',
        'requests', 
        'bs4',
        'openai',
        'dotenv'
    ]
    
    print("Testing package imports...")
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            return False
    
    return True

def test_flask_app():
    """Test if Flask app can be created"""
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_openai_config():
    """Test OpenAI configuration"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found")
        return True
    else:
        print("⚠️  OpenAI API key not found (set OPENAI_API_KEY in .env file)")
        return False

def main():
    """Run all tests"""
    print("🧪 Vintelli Setup Test")
    print("=" * 30)
    
    tests = [
        ("Package Imports", test_imports),
        ("Flask App", test_flask_app),
        ("OpenAI Config", test_openai_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print("\n" + "=" * 30)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Vintelli is ready to run.")
        print("\nTo start the app, run:")
        print("   python app.py")
        print("\nThen open http://localhost:5000 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 