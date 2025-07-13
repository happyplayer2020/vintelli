#!/usr/bin/env python3
"""
Railway Deployment Helper Script
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git_repo():
    """Check if this is a git repository"""
    if not Path('.git').exists():
        print("❌ This is not a git repository!")
        print("\n📝 Please initialize git and push to GitHub:")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        print("   git branch -M main")
        print("   git remote add origin https://github.com/YOUR_USERNAME/vintelli.git")
        print("   git push -u origin main")
        return False
    return True

def check_env_file():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("\n📝 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_openai_api_key_here")
        return False
    return True

def check_deployment_files():
    """Check if all deployment files exist"""
    required_files = ['Procfile', 'runtime.txt', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing deployment files: {', '.join(missing_files)}")
        return False
    
    print("✅ All deployment files present")
    return True

def open_railway():
    """Open Railway in browser"""
    print("\n🌐 Opening Railway...")
    try:
        import webbrowser
        webbrowser.open('https://railway.app')
        print("✅ Railway opened in your browser")
    except:
        print("📝 Please go to: https://railway.app")

def main():
    """Main deployment helper"""
    print("🚀 Vintelli Railway Deployment Helper")
    print("=" * 50)
    
    # Check prerequisites
    if not check_git_repo():
        return
    
    if not check_env_file():
        return
    
    if not check_deployment_files():
        return
    
    print("\n✅ All checks passed! Ready to deploy.")
    
    # Deployment steps
    print("\n📋 Deployment Steps:")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your Vintelli repository")
    print("5. Add environment variable: OPENAI_API_KEY")
    print("6. Deploy!")
    
    # Ask if user wants to open Railway
    response = input("\n🤔 Open Railway in browser? (y/n): ").lower()
    if response in ['y', 'yes']:
        open_railway()
    
    print("\n🎉 After deployment, your app will be live at:")
    print("   https://your-app-name.railway.app")
    
    print("\n💡 Tips:")
    print("- Make sure your .env file is NOT in the repository")
    print("- Railway will automatically detect it's a Python app")
    print("- The free tier includes 500 hours/month")
    print("- You can add a custom domain later")

if __name__ == "__main__":
    main() 