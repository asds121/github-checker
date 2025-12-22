#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local test for GitHub Access Checker without network requests (ASCII version)
"""

import json
import os
import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext
        print("[OK] tkinter modules imported successfully")
    except ImportError as e:
        print(f"[ERROR] tkinter import failed: {e}")
        return False
    
    try:
        import threading
        import time
        import logging
        from datetime import datetime
        print("[OK] Standard library modules imported successfully")
    except ImportError as e:
        print(f"[ERROR] Standard library import failed: {e}")
        return False
    
    try:
        import requests
        print(f"[OK] requests imported successfully (version: {requests.__version__})")
    except ImportError as e:
        print(f"[ERROR] requests import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    if not os.path.exists('config.json'):
        print("[ERROR] config.json not found")
        return False
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_keys = ['timeout', 'auto_check_interval', 'max_retries', 'check_urls']
        for key in required_keys:
            if key not in config:
                print(f"[ERROR] Missing required key: {key}")
                return False
        
        print("[OK] Configuration file is valid")
        print(f"  Timeout: {config['timeout']}s")
        print(f"  Auto check interval: {config['auto_check_interval']}s")
        print(f"  Max retries: {config['max_retries']}")
        print(f"  Check URLs: {len(config['check_urls'])} URLs")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Configuration error: {e}")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\nTesting file structure...")
    
    required_files = [
        'github_checker.py',
        'config.json',
        'requirements.txt',
        'README.md'
    ]
    
    optional_files = [
        'start.bat',
        'enhanced_start.py',
        'simple_start.py',
        'test_functionality.py'
    ]
    
    all_present = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            print(f"[ERROR] {file} - MISSING")
            all_present = False
    
    print("\nOptional files:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            print(f"[INFO] {file} - missing")
    
    return all_present

def test_code_syntax():
    """Test Python code syntax"""
    print("\nTesting code syntax...")
    
    try:
        with open('github_checker.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Try to compile the code
        compile(code, 'github_checker.py', 'exec')
        print("[OK] github_checker.py syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"[ERROR] Syntax error in github_checker.py: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Code validation error: {e}")
        return False

def test_basic_classes():
    """Test basic class instantiation"""
    print("\nTesting basic class functionality...")
    
    try:
        # Import the main module
        sys.path.insert(0, '.')
        
        # Try to import main components
        from github_checker import ConfigManager, LoggerManager
        
        # Test ConfigManager
        config_manager = ConfigManager()
        print("[OK] ConfigManager instantiated successfully")
        
        # Test LoggerManager
        logger_manager = LoggerManager()
        print("[OK] LoggerManager instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Class instantiation failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("GitHub Access Checker - Local Functionality Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
        ("Code Syntax", test_code_syntax),
        ("Basic Classes", test_basic_classes)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"[ERROR] {test_name} failed with exception: {e}")
            results.append((test_name, False))
            print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "[OK] PASS" if result else "[ERROR] FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! The application is ready to use.")
        print("Run 'python simple_start.py' to start the application.")
    else:
        print(f"\n{total - passed} tests failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()