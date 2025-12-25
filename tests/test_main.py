# GitHub Network Status Checker Main Function Tests

import unittest
from unittest.mock import MagicMock, patch, call, ANY
import sys
import os
import json
import time

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_checker import main


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function"""

    @patch('sys.argv', ['github_checker.py'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    def test_main_normal_check(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function with normal check (not full test)"""
        # Mock Checker instance and its check method
        mock_checker = MagicMock()
        mock_checker.check.return_value = {
            'status': 'good',
            'msg': 'All targets accessible',
            'results': [
                ('github.com', {'ok': True, 'ms': 100}),
                ('api.github.com', {'ok': True, 'ms': 150})
            ]
        }
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 0)
        mock_checker.check.assert_called_once()
        self.assertFalse(mock_checker.test.called)
        mock_print.assert_called()

    @patch('sys.argv', ['github_checker.py', '--full-test'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    def test_main_full_test(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function with full test mode"""
        # Mock Checker instance and its test method
        mock_checker = MagicMock()
        mock_checker.test.return_value = {
            'status': 'good',
            'msg': 'All tests passed',
            'iterations': 3,
            'successful_checks': 3,
            'avg_total_time': 250,
            'target_stats': {
                'github.com': {'avg_response': 100, 'success_rate': 100},
                'api.github.com': {'avg_response': 150, 'success_rate': 100}
            }
        }
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 0)
        self.assertFalse(mock_checker.check.called)
        mock_checker.test.assert_called_once()
        mock_print.assert_called()

    @patch('sys.argv', ['github_checker.py', '--json'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    @patch('github_checker.time.strftime', return_value='2023-01-01 12:00:00')
    def test_main_json_output(self, mock_strftime, mock_sleep, mock_print, mock_checker_class):
        """Test main function with JSON output"""
        # Mock Checker instance and its check method
        mock_checker = MagicMock()
        mock_checker.check.return_value = {
            'status': 'good',
            'msg': 'All targets accessible',
            'results': [
                ('github.com', {'ok': True, 'ms': 100}),
                ('api.github.com', {'ok': True, 'ms': 150})
            ]
        }
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 0)
        mock_checker.check.assert_called_once()
        mock_print.assert_called()

    @patch('sys.argv', ['github_checker.py', '--full-test', '--json'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    @patch('github_checker.time.strftime', return_value='2023-01-01 12:00:00')
    def test_main_full_test_json(self, mock_strftime, mock_sleep, mock_print, mock_checker_class):
        """Test main function with full test mode and JSON output"""
        # Mock Checker instance and its test method
        mock_checker = MagicMock()
        mock_checker.test.return_value = {
            'status': 'good',
            'msg': 'All tests passed',
            'iterations': 3,
            'successful_checks': 3,
            'avg_total_time': 250,
            'target_stats': {
                'github.com': {'avg_response': 100, 'success_rate': 100},
                'api.github.com': {'avg_response': 150, 'success_rate': 100}
            }
        }
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 0)
        mock_checker.test.assert_called_once()
        mock_print.assert_called()

    @patch('sys.argv', ['github_checker.py'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    @patch('github_checker.time')
    def test_main_keyboard_interrupt(self, mock_time, mock_sleep, mock_print, mock_checker_class):
        """Test main function handles KeyboardInterrupt"""
        # Mock Checker instance and simulate KeyboardInterrupt
        mock_checker = MagicMock()
        mock_checker.check.side_effect = KeyboardInterrupt()
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 1)
        mock_checker.check.assert_called_once()

    @patch('sys.argv', ['github_checker.py'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    def test_main_request_exception(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function handles RequestException"""
        from requests.exceptions import RequestException

        # Mock Checker instance and simulate RequestException
        mock_checker = MagicMock()
        mock_checker.check.side_effect = RequestException("Connection error")
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 4)
        mock_checker.check.assert_called_once()

    @patch('sys.argv', ['github_checker.py'])
    @patch('github_checker.Checker')
    @patch('github_checker.print')
    @patch('github_checker.time.sleep', return_value=None)
    def test_main_generic_exception(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function handles generic exceptions"""
        # Mock Checker instance and simulate generic exception
        mock_checker = MagicMock()
        mock_checker.check.side_effect = Exception("Unknown error")
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 5)
        mock_checker.check.assert_called_once()


if __name__ == '__main__':
    unittest.main()