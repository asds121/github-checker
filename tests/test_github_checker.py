# GitHub Network Status Checker Tests

import unittest
from unittest.mock import MagicMock, patch
import requests
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.checker import Checker


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
        self.assertIn("accessible", msg.lower())
        self.assertIn("150", msg)  # Average of 100 and 200

    def test_msg_method_warn_status(self):
        """Test the _msg method with warn status"""
        results = [
            ("homepage", {"ok": False, "error": "timeout"}),
            ("api", {"ok": True, "ms": 2000})  # Slow
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        self.assertIn("unstable", msg.lower())
        self.assertIn("homepage", msg)  # Failed target should be mentioned

    def test_msg_method_error_status(self):
        """Test the _msg method with error status"""
        results = [
            ("homepage", {"ok": False, "error": "timeout"}),
            ("api", {"ok": False, "error": "timeout"})
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        self.assertIn("Cannot connect", msg)
        self.assertIn("homepage", msg)  # Failed target should be mentioned

    def test_judge_method_empty_results(self):
        """Test the _judge method with empty results"""
        results = []
        status = self.checker._judge(results)
        self.assertEqual(status, "bad")

    def test_msg_method_unknown_status(self):
        """Test the _msg method with unknown status"""
        results = [
            ("homepage", {"ok": True, "ms": 100}),
            ("api", {"ok": True, "ms": 200})
        ]
        
        msg = self.checker._msg("unknown", results)
        self.assertIn("Unknown status", msg)

    @patch('requests.get')
    def test_test_method_timeout_exception(self, mock_get):
        """Test the _test method with timeout exception"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = self.checker._test("https://github.com", timeout=1.0)
        
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "Request timed out")
        self.assertEqual(result["error_type"], "timeout")

    @patch('requests.get')
    def test_test_method_connection_error_exception(self, mock_get):
        """Test the _test method with connection error exception"""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = self.checker._test("https://github.com", timeout=1.0)
        
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "Connection error - check network")
        self.assertEqual(result["error_type"], "connection")

    @patch('requests.get')
    def test_test_method_request_exception(self, mock_get):
        """Test the _test method with request exception"""
        mock_get.side_effect = requests.exceptions.RequestException("Custom error")
        
        result = self.checker._test("https://github.com", timeout=1.0)
        
        self.assertFalse(result["ok"])
        self.assertIn("Request error", result["error"])
        self.assertEqual(result["error_type"], "request")

    @patch('requests.get')
    def test_test_method_unknown_exception(self, mock_get):
        """Test the _test method with unknown exception"""
        mock_get.side_effect = ValueError("Unknown error")
        
        result = self.checker._test("https://github.com", timeout=1.0)
        
        self.assertFalse(result["ok"])
        self.assertIn("Unexpected error", result["error"])
        self.assertEqual(result["error_type"], "unknown")

    @patch('requests.get')
    def test_test_method_non_200_status_code(self, mock_get):
        """Test the _test method with non-200 status code"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker._test("https://github.com", timeout=1.0)
        
        self.assertFalse(result["ok"])
        self.assertEqual(result["status_code"], 404)

    @patch('requests.get')
    def test_check_method_stops_on_homepage_failure(self, mock_get):
        """Test that check method stops when homepage fails"""
        # First call (homepage) fails
        mock_get.side_effect = [
            requests.exceptions.Timeout(),  # homepage fails
            MagicMock()  # This should not be called
        ]
        
        result = self.checker.check(timeout=1.0)
        
        # Should only have homepage result, not api
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0][0], "homepage")
        self.assertFalse(result["results"][0][1]["ok"])

    @patch('requests.get')
    def test_test_method_statistics_calculation(self, mock_get):
        """Test the test method statistics calculation"""
        # Mock responses with varying response times
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker.test(timeout=1.0)
        
        # Verify statistics are calculated correctly
        self.assertIn('target_stats', result)
        self.assertIn('avg_total_time', result)
        self.assertIn('successful_checks', result)
        self.assertEqual(result['iterations'], 3)
        
        # Check target stats structure
        for name, stats in result['target_stats'].items():
            self.assertIn('avg_response', stats)
            self.assertIn('success_rate', stats)

    @patch('requests.get')
    def test_test_method_mixed_success_failure(self, mock_get):
        """Test the test method with mixed success and failure"""
        # Mock alternating success and failure
        call_count = [0]
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            # Every 3rd call fails
            if call_count[0] % 3 == 0:
                raise requests.exceptions.Timeout()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.elapsed.total_seconds.return_value = 0.1
            return mock_response
        
        mock_get.side_effect = side_effect
        
        result = self.checker.test(timeout=1.0)
        
        # Should have some successful checks but not all
        self.assertGreater(result['successful_checks'], 0)
        self.assertLess(result['successful_checks'], result['iterations'])

    def test_spinning_cursor_generator(self):
        """Test the spinning cursor generator"""
        from utils.animation import spinning_cursor
        
        generator = spinning_cursor()
        
        # Test that it generates the expected sequence
        expected_chars = ['|', '/', '-', '\\']
        for i in range(10):
            char = next(generator)
            self.assertIn(char, expected_chars)

    @patch('requests.get')
    def test_check_method_timeout_calculation(self, mock_get):
        """Test that check method correctly calculates remaining timeout"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_get.return_value = mock_response
        
        result = self.checker.check(timeout=2.0)
        
        # Should complete successfully
        self.assertEqual(result["status"], "good")
        # Total time should be reasonable
        self.assertGreater(result["ms"], 0)

    def test_msg_method_warn_slow_response(self):
        """Test _msg method with warn status due to slow response"""
        # Create results with slow response time (> 3000ms)
        results = [
            ("homepage", {"ok": True, "ms": 4000}),
            ("api", {"ok": True, "ms": 3500})
        ]
        
        status = self.checker._judge(results)
        msg = self.checker._msg(status, results)
        
        # Should be warn due to slow response
        self.assertEqual(status, "warn")
        self.assertIn("slow", msg.lower())
        self.assertIn("accessible", msg.lower())

    @patch('requests.get')
    def test_msg_method_warn_partial_failure(self, mock_get):
        """Test _msg method with warn status due to partial failure"""
        # First target succeeds, second fails
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        
        mock_get.side_effect = [
            mock_response,  # homepage succeeds
            requests.exceptions.Timeout()  # api fails
        ]
        
        result = self.checker.check(timeout=2.0)
        
        # Should be warn due to partial failure
        self.assertEqual(result["status"], "warn")
        self.assertIn("unstable", result["msg"].lower())

    @patch('requests.get')
    def test_msg_method_good_with_ms(self, mock_get):
        """Test _msg method with good status and response time"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker.check(timeout=2.0)
        
        # Should be good with average time
        self.assertEqual(result["status"], "good")
        self.assertIn("avg", result["msg"].lower())
        self.assertIn("ms", result["msg"])

    @patch('requests.get')
    def test_msg_method_good_without_ms(self, mock_get):
        """Test _msg method with good status but no response time"""
        # Mock response without ms field
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker.check(timeout=2.0)
        
        # Should be good
        self.assertEqual(result["status"], "good")
        # Message should still indicate success
        self.assertIn("accessible", result["msg"].lower())

    @patch('requests.get')
    def test_test_method_target_stats_calculation(self, mock_get):
        """Test that test method correctly calculates target statistics"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker.test(timeout=2.0)
        
        # Verify target_stats structure
        self.assertIn('target_stats', result)
        self.assertIn('homepage', result['target_stats'])
        self.assertIn('api', result['target_stats'])
        
        # Check homepage stats
        homepage_stats = result['target_stats']['homepage']
        self.assertIn('avg_response', homepage_stats)
        self.assertIn('success_rate', homepage_stats)
        self.assertEqual(homepage_stats['success_rate'], 100.0)

    @patch('requests.get')
    def test_test_method_all_iterations_bad(self, mock_get):
        """Test test method when all iterations fail"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = self.checker.test(timeout=2.0)
        
        # Should have bad status
        self.assertEqual(result["status"], "bad")
        # Should have 0 successful checks
        self.assertEqual(result["successful_checks"], 0)
        self.assertEqual(result["iterations"], 3)

    @patch('requests.get')
    def test_test_method_all_iterations_good(self, mock_get):
        """Test test method when all iterations succeed"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        result = self.checker.test(timeout=2.0)
        
        # Should have good status
        self.assertEqual(result["status"], "good")
        # Should have 3 successful checks
        self.assertEqual(result["successful_checks"], 3)
        self.assertEqual(result["iterations"], 3)


if __name__ == '__main__':
    unittest.main()