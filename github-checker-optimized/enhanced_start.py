#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced GitHub Access Checker Startup Script
Provides additional startup options and system integration
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing required packages...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages!")
        return False

def check_dependencies():
    """Check if all dependencies are available"""
    try:
        import requests
        print("✅ All dependencies are available!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def setup_environment():
    """Setup environment variables"""
    # Set UTF-8 encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # Create necessary directories
    dirs = ['logs', 'config', 'exports']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ Environment setup complete!")

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    GitHub Access Checker                     ║
║                    Enhanced Version 2.0                      ║
║                                                              ║
║  A comprehensive tool for monitoring GitHub accessibility    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_features():
    """Print feature list"""
    features = [
        "✅ Real-time GitHub status checking",
        "✅ Multi-URL support (github.com, api.github.com)",
        "✅ Detailed logging and statistics",
        "✅ Configurable settings and parameters",
        "✅ Automatic retry mechanisms",
        "✅ Enhanced user interface",
        "✅ Export and import capabilities",
        "✅ Cross-platform compatibility"
    ]
    
    print("Features:")
    for feature in features:
        print(f"  {feature}")
    print()

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if platform.system() != 'Windows':
        print("⚠️  Desktop shortcut creation is only available on Windows")
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "GitHub Checker Enhanced.lnk")
        target = os.path.join(os.getcwd(), "start.bat")
        wDir = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.save()
        
        print("✅ Desktop shortcut created!")
    except ImportError:
        print("⚠️  winshell not available. Install with: pip install winshell pywin32")
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description="Enhanced GitHub Access Checker")
    parser.add_argument("--install-deps", action="store_true", help="Install required dependencies")
    parser.add_argument("--create-shortcut", action="store_true", help="Create desktop shortcut (Windows)")
    parser.add_argument("--check-only", action="store_true", help="Check dependencies and exit")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Handle command line arguments
    if args.check_only:
        print("🔍 Checking dependencies...")
        if check_dependencies():
            print("✅ All checks passed!")
            sys.exit(0)
        else:
            print("❌ Some dependencies are missing!")
            sys.exit(1)
    
    if args.install_deps:
        if not install_requirements():
            sys.exit(1)
    
    if args.create_shortcut:
        create_desktop_shortcut()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Try running with --install-deps to install missing packages")
        response = input("Would you like to install dependencies now? (y/n): ")
        if response.lower() == 'y':
            if not install_requirements():
                sys.exit(1)
        else:
            sys.exit(1)
    
    print_features()
    
    # Set debug mode if requested
    if args.debug:
        os.environ['GITHUB_CHECKER_DEBUG'] = '1'
        print("🐛 Debug mode enabled")
    
    print("🚀 Starting GitHub Access Checker...")
    print("📋 Use the menu bar to access settings and advanced features")
    print("⏹️  Press Ctrl+C to stop the application")
    print()
    
    try:
        # Import and run the main application
        from github_checker import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()