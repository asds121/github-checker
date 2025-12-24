# GitHub Network Status Checker Tests

import unittest
from unittest.mock import patch, MagicMock
import time
import sys
import os

# Add the parent directory to the path to import github_checker
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_checker import Checker


class TestChecker(unittest.TestCase):
    """Test cases for the Checker class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.checker = Checker()

    def test_initialization(self):
        """Test that Checker initializes correctly"""
        self.assertIsNotNone(self.checker)
        self.assertEqual(len(self.checker.TARGETS), 2)
        self.assertIn("github.com", str(self.checker.TARGETS[0]))

    @patch('requests.get')
    def test_test_method_success(self, mock_get):
        """Test the test method with successful responses"""
        # Mock successful responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response

        result = self.checker.test(timeout=1.0)
        
        # Check that the result has expected structure
        self.assertIn('status', result)
        self.assertIn('msg', result)
        self.assertIn('iterations', result)
        self.assertIn('successful_checks', result)
        self.assertIn('avg_total_time', result)
        self.assertIn('target_stats', result)
        self.assertIn('all_results', result)

    @patch('requests.get')
    def test_check_method_success(self, mock_get):
        """Test the check method with successful responses"""
        # Mock successful responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response

        result = self.checker.check(timeout=1.0)
        
        # Check that the result has expected structure
        self.assertIn('status', result)
        self.assertIn('msg', result)
        self.assertIn('results', result)
        self.assertEqual(len(result['results']), len(self.checker.TARGETS))

    @patch('requests.get')
    def test_check_method_failure(self, mock_get):
        """Test the check method with failed responses"""
        # Mock failed responses (raising exception)
        mock_get.side_effect = Exception("Connection error")

        result = self.checker.check(timeout=1.0)
        
        # All results should have error status
        for name, result_item in result['results']:
            self.assertFalse(result_item.get('ok'))
            self.assertIn('error', result_item)

    def test_judge_method_good_status(self):
        """Test the _judge method with good status conditions"""
        results = [
            ("homepage", {"ok": True, "ms": 100}),
            ("api", {"ok": True, "ms": 200})
        ]
        
        status = self.checker._judge(results)
        self.assertEqual(status, "good")

    def test_judge_method_warn_status(self):
        """Test the _judge method with warning status conditions"""
        results = [
            ("homepage", {"ok": True, "ms": 1000}),  # Slow response
            ("api", {"ok": False, "error": "timeout"})  # Failed
        ]
        
        status = self.checker._judge(results)
        self.assertEqual(status, "warn")

    def test_judge_method_error_status(self):
        """Test the _judge method with error status conditions"""
        results = [
            ("homepage", {"ok": False, "error": "timeout"}),
            ("api", {"ok": False, "error": "timeout"})
        ]
        
        status = self.checker._judge(results)
        self.assertEqual(status, "bad")

    def test_msg_method_good_status(self):
        """Test the _msg method with good status"""
        results = [
            ("homepage", {"ok": True, "ms": 100}),
            ("api", {"ok": True, "ms": 200})
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        self.assertIn("OK", msg)
        self.assertIn("accessible", msg.lower())

    def test_msg_method_warn_status(self):
        """Test the _msg method with warn status"""
        results = [
            ("homepage", {"ok": False, "error": "timeout"}),
            ("api", {"ok": True, "ms": 2000})  # Slow
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        self.assertIn("WARN", msg)
        self.assertIn("unstable", msg.lower())

    def test_msg_method_error_status(self):
        """Test the _msg method with error status"""
        results = [
            ("homepage", {"ok": False, "error": "timeout"}),
            ("api", {"ok": False, "error": "timeout"})
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        self.assertIn("FAIL", msg)
        self.assertIn("Cannot connect", msg)


if __name__ == '__main__':
    unittest.main()