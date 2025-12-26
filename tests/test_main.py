# -*- coding: ascii -*-
"""
GitHub Network Status Checker Main Function Tests
"""

import unittest
from unittest.mock import MagicMock, patch, call, ANY, mock_open
import sys
import os
import json
import time
from requests.exceptions import RequestException

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import main, collect_feedback, save_feedback, show_quick_feedback_prompt


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function"""

    @patch('sys.argv', ['cli.py'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
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

    @patch('sys.argv', ['cli.py', '--full-test'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
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

    @patch('sys.argv', ['cli.py', '--json'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    @patch('cli.time.strftime', return_value='2023-01-01 12:00:00')
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

    @patch('sys.argv', ['cli.py', '--full-test', '--json'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    @patch('cli.time.strftime', return_value='2023-01-01 12:00:00')
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

    @patch('sys.argv', ['cli.py'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    @patch('cli.time')
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

    @patch('sys.argv', ['cli.py'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    def test_main_request_exception(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function handles RequestException"""
        # Mock Checker instance and simulate RequestException
        mock_checker = MagicMock()
        mock_checker.check.side_effect = RequestException("Connection error")
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 4)
        mock_checker.check.assert_called_once()

    @patch('sys.argv', ['cli.py'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    def test_main_other_exception(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function handles other exceptions"""
        # Mock Checker instance and simulate generic exception
        mock_checker = MagicMock()
        mock_checker.check.side_effect = Exception("Unexpected error")
        mock_checker_class.return_value = mock_checker

        # Call main function
        exit_code = main()

        # Verify results
        self.assertEqual(exit_code, 3)
        mock_checker.check.assert_called_once()

    @patch('sys.argv', ['cli.py', '--timeout', '10'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    def test_main_custom_timeout(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function with custom timeout"""
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
        # Verify check was called with custom timeout
        mock_checker.check.assert_called_once_with(timeout=10)


class TestCollectFeedback(unittest.TestCase):
    """Test cases for collect_feedback function"""

    @patch('builtins.input', side_effect=['5', '1', 'Great tool!'])
    def test_collect_feedback_full_flow_success(self, mock_input):
        """Test collect_feedback with valid rating, type and comment"""
        result_data = {'status': 'good', 'is_full_test': False}
        with patch('cli.save_feedback', return_value=True):
            result = collect_feedback(result_data)
            self.assertTrue(result)

    @patch('builtins.input', side_effect=['5', '1', ''])
    def test_collect_feedback_with_empty_comment(self, mock_input):
        """Test collect_feedback with empty comment"""
        result_data = {'status': 'good', 'is_full_test': False}
        with patch('cli.save_feedback', return_value=True):
            result = collect_feedback(result_data)
            self.assertTrue(result)

    @patch('builtins.input', return_value='')
    def test_collect_feedback_skip_rating(self, mock_input):
        """Test collect_feedback when user skips rating"""
        result_data = {'status': 'good', 'is_full_test': False}
        result = collect_feedback(result_data)
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['6', '1', ''])
    def test_collect_feedback_invalid_rating(self, mock_input):
        """Test collect_feedback with invalid rating"""
        result_data = {'status': 'good', 'is_full_test': False}
        result = collect_feedback(result_data)
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['invalid', '1', ''])
    def test_collect_feedback_non_numeric_rating(self, mock_input):
        """Test collect_feedback with non-numeric rating"""
        result_data = {'status': 'good', 'is_full_test': False}
        result = collect_feedback(result_data)
        self.assertFalse(result)


class TestSaveFeedback(unittest.TestCase):
    """Test cases for save_feedback function"""

    def test_save_feedback_success(self):
        """Test save_feedback creates file successfully"""
        with patch('builtins.open', mock_open()):
            with patch('cli.json.dump'):
                result = save_feedback(5, 'useful', 'Great tool!', {'status': 'good'})
                self.assertTrue(result)

    def test_save_feedback_failure(self):
        """Test save_feedback handles file creation failure"""
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            result = save_feedback(5, 'useful', 'Test comment', {'status': 'good'})
            self.assertFalse(result)


class TestShowQuickFeedbackPrompt(unittest.TestCase):
    """Test cases for show_quick_feedback_prompt function"""

    @patch('cli.print')
    def test_show_quick_feedback_prompt_calls_print(self, mock_print):
        """Test show_quick_feedback_prompt calls print function"""
        show_quick_feedback_prompt()
        mock_print.assert_called()


class TestMainEdgeCases(unittest.TestCase):
    """Test cases for edge cases in main function"""

    @patch('sys.argv', ['cli.py', '--bad-flag'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    def test_main_invalid_argument(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function with invalid argument"""
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', ['cli.py'])
    @patch('cli.Checker')
    @patch('cli.print')
    @patch('cli.time.sleep', return_value=None)
    def test_main_checker_init_failure(self, mock_sleep, mock_print, mock_checker_class):
        """Test main function when Checker initialization fails"""
        mock_checker_class.side_effect = Exception("Failed to initialize")
        exit_code = main()
        self.assertEqual(exit_code, 3)


if __name__ == '__main__':
    unittest.main()
