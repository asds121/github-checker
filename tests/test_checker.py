# -*- coding: ascii -*-
"""
Comprehensive tests for core.checker module

Tests the Checker class for GitHub accessibility checking functionality.

Author: GitHub Checker Project
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import TooManyRedirects
from requests.exceptions import RequestException

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.checker import Checker
from utils.constants import (
    DEFAULT_TIMEOUT,
    RESPONSE_TIME_THRESHOLD_MS,
    MIN_REMAIN_TIMEOUT,
    FULL_TEST_ITERATIONS
)


class TestCheckerInit(unittest.TestCase):
    """Test cases for Checker class initialization"""

    def test_checker_has_targets(self):
        """Test that Checker class has TARGETS attribute"""
        checker = Checker()
        self.assertTrue(hasattr(Checker, 'TARGETS'))
        self.assertIsInstance(Checker.TARGETS, list)
        self.assertGreater(len(Checker.TARGETS), 0)

    def test_checker_targets_content(self):
        """Test that TARGETS contains expected GitHub URLs"""
        checker = Checker()
        target_names = [name for name, url in Checker.TARGETS]
        target_urls = [url for name, url in Checker.TARGETS]

        self.assertIn('homepage', target_names)
        self.assertIn('api', target_names)
        self.assertIn('https://github.com', target_urls)
        self.assertIn('https://api.github.com', target_urls)


class TestCheckerTest(unittest.TestCase):
    """Test cases for Checker.test() method"""

    @patch('core.checker.time.time')
    @patch('core.checker.Checker.check')
    def test_test_method_calls_check(self, mock_check, mock_time):
        """Test that test() method calls check() multiple times"""
        checker = Checker()
        mock_time.side_effect = [0, 0.1, 0.2, 0.3]  # Simulate time progression

        # Mock check to return valid results
        mock_check.return_value = {
            'status': 'good',
            'ms': 100,
            'results': [
                ('homepage', {'ok': True, 'ms': 50}),
                ('api', {'ok': True, 'ms': 50})
            ]
        }

        result = checker.test(timeout=5)

        # Verify check was called FULL_TEST_ITERATIONS times
        self.assertEqual(mock_check.call_count, FULL_TEST_ITERATIONS)

    @patch('core.checker.time.time')
    @patch('core.checker.Checker.check')
    def test_test_method_returns_correct_structure(self, mock_check, mock_time):
        """Test that test() returns correct result structure"""
        checker = Checker()
        mock_time.side_effect = [0, 0.1, 0.2, 0.3] * FULL_TEST_ITERATIONS

        mock_check.return_value = {
            'status': 'good',
            'ms': 100,
            'results': [
                ('homepage', {'ok': True, 'ms': 50}),
                ('api', {'ok': True, 'ms': 50})
            ]
        }

        result = checker.test(timeout=5)

        # Verify all required keys are present
        required_keys = ['status', 'msg', 'iterations', 'avg_total_time',
                        'successful_checks', 'target_stats', 'all_results']
        for key in required_keys:
            self.assertIn(key, result)

        self.assertEqual(result['iterations'], FULL_TEST_ITERATIONS)

    @patch('core.checker.time.time')
    @patch('core.checker.Checker.check')
    def test_test_method_calculates_target_stats(self, mock_check, mock_time):
        """Test that test() calculates target statistics correctly"""
        checker = Checker()
        mock_time.side_effect = [0, 0.1, 0.2, 0.3] * FULL_TEST_ITERATIONS

        # Return results with varying response times
        mock_check.side_effect = [
            {
                'status': 'good',
                'ms': 100,
                'results': [
                    ('homepage', {'ok': True, 'ms': 50}),
                    ('api', {'ok': True, 'ms': 150})
                ]
            },
            {
                'status': 'good',
                'ms': 120,
                'results': [
                    ('homepage', {'ok': True, 'ms': 60}),
                    ('api', {'ok': True, 'ms': 160})
                ]
            },
            {
                'status': 'good',
                'ms': 110,
                'results': [
                    ('homepage', {'ok': True, 'ms': 55}),
                    ('api', {'ok': True, 'ms': 155})
                ]
            }
        ] * (FULL_TEST_ITERATIONS // 3 + 1)

        result = checker.test(timeout=5)

        # Verify target_stats has entries for both targets
        self.assertIn('homepage', result['target_stats'])
        self.assertIn('api', result['target_stats'])


class TestCheckerCheck(unittest.TestCase):
    """Test cases for Checker.check() method"""

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_returns_correct_structure(self, mock_time, mock_test):
        """Test that check() returns correct result structure"""
        checker = Checker()
        mock_time.side_effect = [0, 0.1, 0.2, 0.3]  # Enough time values
        mock_test.return_value = {'ok': True, 'ms': 100}

        result = checker.check(timeout=5)

        required_keys = ['status', 'ms', 'results', 'msg']
        for key in required_keys:
            self.assertIn(key, result)

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_calls_test_for_each_target(self, mock_time, mock_test):
        """Test that check() calls _test() for each target"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15, 0.2, 0.25]  # Enough time values for all targets
        # Return same result for each target
        mock_test.return_value = {'ok': True, 'ms': 100}

        checker.check(timeout=5)

        # Verify _test was called for each target (2 targets: homepage and api)
        self.assertEqual(mock_test.call_count, len(Checker.TARGETS))

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_stops_on_homepage_failure(self, mock_time, mock_test):
        """Test that check() stops testing if homepage fails"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15]
        # First call fails, second would succeed but shouldn't be called
        mock_test.side_effect = [
            {'ok': False, 'ms': 50, 'error': 'Connection failed'},
            {'ok': True, 'ms': 100}
        ]

        result = checker.check(timeout=5)

        # Should only call _test once (for homepage)
        self.assertEqual(mock_test.call_count, 1)
        self.assertEqual(result['status'], 'bad')

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_continues_on_homepage_success(self, mock_time, mock_test):
        """Test that check() continues testing api if homepage succeeds"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
        # Both succeed
        mock_test.side_effect = [
            {'ok': True, 'ms': 50},
            {'ok': True, 'ms': 100}
        ]

        result = checker.check(timeout=5)

        # Should call _test twice (homepage and api)
        self.assertEqual(mock_test.call_count, 2)
        self.assertEqual(result['status'], 'good')

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_handles_timeout(self, mock_time, mock_test):
        """Test that check() handles timeout correctly"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
        # Simulate timeout by returning False for exceeded time
        mock_test.side_effect = [
            {'ok': False, 'ms': 50, 'error': 'Timeout'},
            {'ok': False, 'ms': 50, 'error': 'Timeout'}
        ]

        result = checker.check(timeout=5)

        required_keys = ['status', 'ms', 'results', 'msg']
        for key in required_keys:
            self.assertIn(key, result)


class TestCheckerTestMethod(unittest.TestCase):
    """Test cases for Checker._test() method"""

    @patch('core.checker.requests.get')
    def test_test_method_returns_ok_on_success(self, mock_get):
        """Test that _test() returns ok=True on successful request"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.05
        mock_get.return_value = mock_response

        result = checker._test('https://example.com', timeout=5)

        self.assertTrue(result['ok'])
        self.assertIn('ms', result)
        self.assertEqual(result['status_code'], 200)

    @patch('core.checker.requests.get')
    def test_test_method_handles_request_exception(self, mock_get):
        """Test that _test() handles request exceptions correctly"""
        checker = Checker()
        mock_get.side_effect = RequestException('Connection failed')

        result = checker._test('homepage', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    @patch('core.checker.requests.get')
    def test_test_method_handles_timeout_exception(self, mock_get):
        """Test that _test() handles timeout exceptions correctly"""
        checker = Checker()
        mock_get.side_effect = Timeout('Request timed out')

        result = checker._test('homepage', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    @patch('core.checker.requests.get')
    def test_test_method_handles_connection_error(self, mock_get):
        """Test that _test() handles connection errors correctly"""
        checker = Checker()
        mock_get.side_effect = ConnectionError('Connection refused')

        result = checker._test('homepage', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    @patch('core.checker.requests.get')
    def test_test_method_handles_http_error(self, mock_get):
        """Test that _test() handles HTTP errors correctly"""
        checker = Checker()
        mock_get.side_effect = HTTPError('404 Not Found')

        result = checker._test('homepage', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    @patch('core.checker.requests.get')
    def test_test_method_handles_too_many_redirects(self, mock_get):
        """Test that _test() handles too many redirects correctly"""
        checker = Checker()
        mock_get.side_effect = TooManyRedirects('Too many redirects')

        result = checker._test('homepage', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)


class TestCheckerJudge(unittest.TestCase):
    """Test cases for Checker._judge() method"""

    def test_judge_returns_good_for_fast_response(self):
        """Test that _judge() returns 'good' for response below threshold"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 50}),
            ('api', {'ok': True, 'ms': 50})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'good')

    def test_judge_returns_warn_for_slow_response(self):
        """Test that _judge() returns 'warn' for response above threshold"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 4000}),
            ('api', {'ok': True, 'ms': 4000})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'warn')

    def test_judge_returns_good_at_threshold(self):
        """Test that _judge() returns 'good' at exactly threshold (3000ms)"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 3000}),
            ('api', {'ok': True, 'ms': 3000})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'good')

    def test_judge_returns_bad_for_failure(self):
        """Test that _judge() returns 'bad' for any failure"""
        checker = Checker()
        results = [
            ('homepage', {'ok': False, 'error': 'Failed'}),
            ('api', {'ok': True, 'ms': 50})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'bad')


class TestCheckerMsg(unittest.TestCase):
    """Test cases for Checker._msg() method"""

    def test_msg_returns_success_message(self):
        """Test that _msg() returns success message for good status"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 50}),
            ('api', {'ok': True, 'ms': 50})
        ]
        msg = checker._msg('good', results)
        self.assertIn('accessible', msg.lower())

    def test_msg_returns_failure_message(self):
        """Test that _msg() returns failure message for bad status"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 50}),
            ('api', {'ok': False, 'error': 'Failed'})
        ]
        msg = checker._msg('bad', results)
        self.assertIn('fail', msg.lower())

    def test_msg_returns_slow_message(self):
        """Test that _msg() returns slow message for warn status"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 200}),
            ('api', {'ok': True, 'ms': 200})
        ]
        msg = checker._msg('warn', results)
        self.assertIn('slow', msg.lower())


class TestCheckerEdgeCases(unittest.TestCase):
    """Test cases for edge cases in Checker class"""

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_handles_all_targets_failing(self, mock_time, mock_test):
        """Test that check() handles all targets failing"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15]
        mock_test.side_effect = [
            {'ok': False, 'ms': 50, 'error': 'Failed'},
        ]

        result = checker.check(timeout=5)

        self.assertEqual(result['status'], 'bad')

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_handles_mixed_results(self, mock_time, mock_test):
        """Test that check() handles mixed success/failure results"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
        mock_test.side_effect = [
            {'ok': True, 'ms': 50, 'status_code': 200},
            {'ok': False, 'ms': 50, 'error': 'Failed'}
        ]

        result = checker.check(timeout=5)

        self.assertEqual(result['status'], 'bad')
        self.assertIn('ms', result)


class TestCheckerBoundaryConditions(unittest.TestCase):
    """Boundary condition tests for Checker class"""

    @patch('core.checker.requests.get')
    def test_test_method_zero_timeout(self, mock_get):
        """Test _test() with zero timeout value"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.001
        mock_get.return_value = mock_response

        result = checker._test('https://example.com', timeout=0)

        self.assertTrue(result['ok'])
        self.assertIn('ms', result)

    @patch('core.checker.requests.get')
    def test_test_method_very_large_timeout(self, mock_get):
        """Test _test() with very large timeout value"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response

        result = checker._test('https://example.com', timeout=3600)

        self.assertTrue(result['ok'])
        self.assertIn('ms', result)

    @patch('core.checker.requests.get')
    def test_test_method_response_time_zero(self, mock_get):
        """Test _test() with zero response time (instant response)"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0
        mock_get.return_value = mock_response

        result = checker._test('https://example.com', timeout=5)

        self.assertTrue(result['ok'])
        self.assertEqual(result['ms'], 0)

    @patch('core.checker.requests.get')
    def test_test_method_response_time_very_large(self, mock_get):
        """Test _test() with very large response time"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 30
        mock_get.return_value = mock_response

        result = checker._test('https://example.com', timeout=60)

        self.assertTrue(result['ok'])
        self.assertGreaterEqual(result['ms'], 30000)

    @patch('core.checker.requests.get')
    def test_test_method_handles_keyboard_interrupt(self, mock_get):
        """Test _test() handles KeyboardInterrupt gracefully"""
        checker = Checker()
        mock_get.side_effect = KeyboardInterrupt()

        result = checker._test('https://example.com', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    @patch('core.checker.requests.get')
    def test_test_method_handles_generic_exception(self, mock_get):
        """Test _test() handles generic exceptions (non-RequestException)"""
        checker = Checker()
        mock_get.side_effect = ValueError('Invalid value')

        result = checker._test('https://example.com', timeout=5)

        self.assertFalse(result['ok'])
        self.assertIn('error', result)

    def test_judge_empty_results(self):
        """Test _judge() with empty results"""
        checker = Checker()
        result = checker._judge([])
        self.assertEqual(result, 'bad')

    def test_judge_all_ok_fast_response(self):
        """Test _judge() with all results ok and fast response"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 50}),
            ('api', {'ok': True, 'ms': 50})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'good')

    def test_judge_all_ok_slow_response(self):
        """Test _judge() with all results ok but slow response (>3000ms)"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 4000}),
            ('api', {'ok': True, 'ms': 4000})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'warn')

    def test_judge_with_failure(self):
        """Test _judge() with some results failing"""
        checker = Checker()
        results = [
            ('homepage', {'ok': True, 'ms': 50}),
            ('api', {'ok': False, 'error': 'Failed'})
        ]
        result = checker._judge(results)
        self.assertEqual(result, 'bad')

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_rapid_succession_calls(self, mock_time, mock_test):
        """Test multiple rapid check() calls don't interfere"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1, 0.15] * 10
        mock_test.return_value = {'ok': True, 'ms': 50, 'status_code': 200}

        results = [checker.check(timeout=5) for _ in range(5)]

        for result in results:
            self.assertIn('status', result)
            self.assertIn('ms', result)

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_with_minimum_targets(self, mock_time, mock_test):
        """Test check() with exactly one target available"""
        checker = Checker()
        mock_time.side_effect = [0, 0.05, 0.1]
        mock_test.return_value = {'ok': True, 'ms': 50, 'status_code': 200}

        # Temporarily reduce targets for this test
        original_targets = Checker.TARGETS
        Checker.TARGETS = [('single', 'https://example.com')]

        try:
            result = checker.check(timeout=5)
            self.assertIn('status', result)
            self.assertEqual(mock_test.call_count, 1)
        finally:
            Checker.TARGETS = original_targets


class TestCheckerPerformance(unittest.TestCase):
    """Performance-related tests for Checker class"""

    @patch('core.checker.Checker._test')
    @patch('core.checker.time.time')
    def test_check_timing_accuracy(self, mock_time, mock_test):
        """Test that check() timing is reasonably accurate"""
        checker = Checker()
        # Simulate varying response times
        mock_time.side_effect = [0, 0.1, 0.2, 0.35, 0.45, 0.6]
        mock_test.return_value = {'ok': True, 'ms': 100, 'status_code': 200}

        result = checker.check(timeout=5)

        self.assertIn('ms', result)
        self.assertGreater(result['ms'], 0)

    @patch('core.checker.requests.get')
    def test_test_method_performance(self, mock_get):
        """Test _test() completes within reasonable time"""
        checker = Checker()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.05
        mock_get.return_value = mock_response

        import time
        start = time.time()
        result = checker._test('https://example.com', timeout=5)
        elapsed = time.time() - start

        self.assertTrue(result['ok'])
        self.assertLess(elapsed, 1.0)  # Should complete well within 1 second


if __name__ == '__main__':
    unittest.main()



