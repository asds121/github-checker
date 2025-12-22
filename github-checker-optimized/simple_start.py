#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GitHub Access Checker Startup Script
"""

import os
import sys
import subprocess

def check_python():
    """Check Python environment"""
    print("Checking Python environment...")
    
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher required!")
        return False
    
    print(f"Python version: {sys.version.split()[0]} - OK")
    return True

def check_requests():
    """Check if requests is available"""
    try:
        import requests
        print(f"requests version: {requests.__version__} - OK")
        return True
    except ImportError:
        print("requests module not found!")
        return False

def setup_env():
    """Setup basic environment"""
    # Create logs directory
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("Created logs directory")
    
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("Environment setup complete")

def main():
    """Main function"""
    print("=" * 50)
    print("GitHub Access Checker - Enhanced Version")
    print("=" * 50)
    print()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check requests
    if not check_requests():
        print("\nInstalling requests module...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            print("requests module installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install requests module!")
            input("Press Enter to exit...")
            sys.exit(1)
    
    # Setup environment
    setup_env()
    print()
    
    # Import and run main application
    try:
        print("Starting GitHub Access Checker...")
        print("Use the menu bar to access settings and features")
        print("Press Ctrl+C to stop the application")
        print()
        
        from github_checker import main as app_main
        app_main()
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()