#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for GitHub Access Checker functionality
"""

import requests
import time
import json
from datetime import datetime

def test_basic_functionality():
    """Test basic GitHub access functionality"""
    print("Testing basic GitHub access functionality...")
    
    urls_to_test = [
        "https://github.com",
        "https://api.github.com"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Referer': 'https://github.com/'
    }
    
    results = []
    
    for url in urls_to_test:
        try:
            print(f"Testing {url}...")
            start_time = time.time()
            
            response = requests.get(
                url,
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            
            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)
            
            result = {
                "url": url,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code == 200,
                "error": None
            }
            
            print(f"  Status: {response.status_code}")
            print(f"  Response time: {response_time}ms")
            print(f"  Success: {result['success']}")
            
            results.append(result)
            
        except requests.exceptions.Timeout:
            error_result = {
                "url": url,
                "status_code": None,
                "response_time_ms": None,
                "success": False,
                "error": "Timeout"
            }
            results.append(error_result)
            print(f"  Error: Timeout")
            
        except requests.exceptions.ConnectionError:
            error_result = {
                "url": url,
                "status_code": None,
                "response_time_ms": None,
                "success": False,
                "error": "Connection Error"
            }
            results.append(error_result)
            print(f"  Error: Connection Error")
            
        except Exception as e:
            error_result = {
                "url": url,
                "status_code": None,
                "response_time_ms": None,
                "success": False,
                "error": str(e)
            }
            results.append(error_result)
            print(f"  Error: {str(e)}")
        
        print()
    
    return results

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration loading...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("Configuration loaded successfully!")
        print(f"Timeout: {config.get('timeout', 'Not set')}")
        print(f"Auto check interval: {config.get('auto_check_interval', 'Not set')}")
        print(f"Max retries: {config.get('max_retries', 'Not set')}")
        print(f"Check URLs: {config.get('check_urls', [])}")
        
        return True
        
    except FileNotFoundError:
        print("Error: config.json not found!")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config.json: {e}")
        return False
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False

def save_test_results(results):
    """Save test results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total_tests": len(results),
            "successful_tests": sum(1 for r in results if r['success']),
            "failed_tests": sum(1 for r in results if not r['success'])
        }
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print(f"Test results saved to {filename}")
        return filename
        
    except Exception as e:
        print(f"Error saving test results: {e}")
        return None

def main():
    """Main test function"""
    print("=" * 60)
    print("GitHub Access Checker - Functionality Test")
    print("=" * 60)
    print()
    
    # Test configuration
    config_ok = test_configuration()
    print()
    
    if not config_ok:
        print("Configuration test failed. Exiting.")
        return
    
    # Test basic functionality
    print("Starting network tests...")
    print("Note: This will make actual HTTP requests to GitHub")
    print()
    
    results = test_basic_functionality()
    
    # Print summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total URLs tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    
    # Save results
    saved_file = save_test_results(results)
    if saved_file:
        print(f"\nDetailed results saved to: {saved_file}")
    
    # Overall result
    print("\n" + "=" * 60)
    if successful > 0:
        print("✅ Basic functionality test PASSED")
        print("The application should work correctly.")
    else:
        print("❌ Basic functionality test FAILED")
        print("There may be network issues or GitHub is inaccessible.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()