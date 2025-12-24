#!/usr/bin/env python3
"""
Test runner for GitHub Network Status Checker
"""

import unittest
import sys
import os

if __name__ == '__main__':
    # Add the project root to the path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    if result.failures or result.errors:
        sys.exit(1)
    else:
        print("\nAll tests passed! ✓")