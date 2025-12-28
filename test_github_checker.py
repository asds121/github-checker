"""
Comprehensive test suite for GitHub Checker
Tests coverage:
1. Status judgment logic (_judge)
2. Message generation (_msg)
3. Exception handling (_test)
4. Check and test methods
5. Output formatting
6. Command-line argument parsing
"""

import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, '.')

from github_checker import (
    Checker, colorize, format_status, format_fun_status,
    DEFAULT_TIMEOUT, FULL_TEST_ITERATIONS, RESPONSE_TIME_THRESHOLD_MS,
    Colors, main
)
import requests


class TestColorize(unittest.TestCase):
    def test_colorize_red(self):
        result = colorize("test", Colors.RED)
        self.assertIn("test", result)
        self.assertIn(Colors.RESET, result)
        self.assertIn(Colors.RED, result)

    def test_colorize_green(self):
        result = colorize("success", Colors.GREEN)
        self.assertIn("success", result)
        self.assertIn(Colors.RESET, result)

    def test_colorize_yellow(self):
        result = colorize("warning", Colors.YELLOW)
        self.assertIn("warning", result)
        self.assertIn(Colors.RESET, result)


class TestFormatStatus(unittest.TestCase):
    def test_good_status(self):
        result = format_status("good", "Everything works")
        self.assertIn("[OK]", result)
        self.assertIn("Everything works", result)

    def test_warn_status(self):
        result = format_status("warn", "Something wrong")
        self.assertIn("[WARN]", result)
        self.assertIn("Something wrong", result)

    def test_bad_status(self):
        result = format_status("bad", "System down")
        self.assertIn("[FAIL]", result)
        self.assertIn("System down", result)

    def test_unknown_status(self):
        result = format_status("unknown", "Unknown")
        self.assertIn("[UNKNOWN]", result)


class TestFormatFunStatus(unittest.TestCase):
    def test_fun_good_very_fast(self):
        result = format_fun_status("good", 100)
        self.assertIn("super fast", result.lower())

    def test_fun_good_fast(self):
        result = format_fun_status("good", 700)
        self.assertIn("happy", result.lower())

    def test_fun_good_normal(self):
        result = format_fun_status("good", 2000)
        self.assertIn("accessible", result.lower())

    def test_fun_warn_slow(self):
        result = format_fun_status("warn", 4000)
        self.assertIn("nap", result.lower())

    def test_fun_warn_normal(self):
        result = format_fun_status("warn", 2000)
        self.assertIn("slow", result.lower())

    def test_fun_bad(self):
        result = format_fun_status("bad")
        self.assertIn("unreachable", result.lower())


class TestCheckerJudge(unittest.TestCase):
    """Test _judge method - status judgment logic"""

    def test_all_success_fast(self):
        results = [("homepage", {"ok": True, "ms": 500}), ("api", {"ok": True, "ms": 400})]
        self.assertEqual(Checker()._judge(results), "good")

    def test_all_success_slow(self):
        results = [("homepage", {"ok": True, "ms": 4000}), ("api", {"ok": True, "ms": 3000})]
        self.assertEqual(Checker()._judge(results), "warn")

    def test_partial_success(self):
        results = [("homepage", {"ok": True, "ms": 500}), ("api", {"ok": False, "error": "Failed"})]
        self.assertEqual(Checker()._judge(results), "warn")

    def test_all_fail(self):
        results = [("homepage", {"ok": False}), ("api", {"ok": False})]
        self.assertEqual(Checker()._judge(results), "bad")

    def test_empty_results(self):
        self.assertEqual(Checker()._judge([]), "bad")

    def test_boundary_case(self):
        results = [("homepage", {"ok": True, "ms": 2999}), ("api", {"ok": True, "ms": 2999})]
        self.assertEqual(Checker()._judge(results), "good")

        results_slow = [("homepage", {"ok": True, "ms": 3000}), ("api", {"ok": True, "ms": 3000})]
        self.assertEqual(Checker()._judge(results_slow), "warn")


class TestCheckerMsg(unittest.TestCase):
    """Test _msg method - message generation"""

    def test_good_with_timing(self):
        results = [("homepage", {"ok": True, "ms": 500}), ("api", {"ok": True, "ms": 400})]
        msg = Checker()._msg("good", results)
        self.assertIn("accessible", msg.lower())
        self.assertIn("ms", msg)

    def test_good_no_timing(self):
        results = [("homepage", {"ok": True}), ("api", {"ok": True})]
        msg = Checker()._msg("good", results)
        self.assertIn("accessible", msg.lower())

    def test_warn_partial_failure(self):
        results = [("homepage", {"ok": True, "ms": 500}), ("api", {"ok": False})]
        msg = Checker()._msg("warn", results)
        self.assertIn("unstable", msg.lower())
        self.assertIn("api", msg)

    def test_warn_slow(self):
        results = [("homepage", {"ok": True, "ms": 4000}), ("api", {"ok": True, "ms": 4000})]
        msg = Checker()._msg("warn", results)
        self.assertIn("slow", msg.lower())

    def test_bad(self):
        results = [("homepage", {"ok": False}), ("api", {"ok": False})]
        msg = Checker()._msg("bad", results)
        self.assertIn("Cannot connect", msg)
        self.assertIn("homepage", msg)
        self.assertIn("api", msg)


class TestCheckerTestMethod(unittest.TestCase):
    """Test _test method - URL testing with exception handling"""

    @patch('github_checker.requests.get')
    def test_success_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker()._test("https://github.com", 5.0)

        self.assertTrue(result["ok"])
        self.assertEqual(result["status_code"], 200)
        self.assertIn("ms", result)

    @patch('github_checker.requests.get')
    def test_success_non_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["status_code"], 404)

    @patch('github_checker.requests.get')
    def test_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "timeout")
        self.assertIn("timed out", result["error"].lower())

    @patch('github_checker.requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to resolve")

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "connection")

    @patch('github_checker.requests.get')
    def test_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("500 Server Error")

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "http")

    @patch('github_checker.requests.get')
    def test_too_many_redirects(self, mock_get):
        mock_get.side_effect = requests.exceptions.TooManyRedirects()

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "redirect")

    @patch('github_checker.requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Generic error")

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "request")

    @patch('github_checker.requests.get')
    def test_unexpected_exception(self, mock_get):
        mock_get.side_effect = ValueError("Unexpected error")

        result = Checker()._test("https://github.com", 5.0)

        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "unknown")


class TestCheckerCheckMethod(unittest.TestCase):
    """Test check method - single check operation"""

    @patch('github_checker.requests.get')
    def test_check_returns_dict(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().check(timeout=5.0)

        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("results", result)
        self.assertIn("ms", result)
        self.assertIn("msg", result)

    @patch('github_checker.requests.get')
    def test_check_stops_on_homepage_failure(self, mock_get):
        def side_effect(url, **kwargs):
            if "github.com" in url and "api" not in url:
                raise requests.exceptions.ConnectionError()
            return MagicMock(status_code=200)

        mock_get.side_effect = side_effect

        result = Checker().check(timeout=5.0)

        self.assertEqual(result["status"], "bad")
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0][0], "homepage")

    @patch('github_checker.requests.get')
    def test_check_all_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().check(timeout=5.0)

        self.assertIn(result["status"], ["good", "warn"])
        self.assertEqual(len(result["results"]), 2)

    @patch('github_checker.requests.get')
    def test_check_ms_positive(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().check(timeout=5.0)

        self.assertGreater(result["ms"], 0)


class TestCheckerTestFullMethod(unittest.TestCase):
    """Test test method - full test with iterations"""

    @patch('github_checker.requests.get')
    def test_full_test_returns_dict(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().test(timeout=5.0)

        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("iterations", result)
        self.assertIn("avg_total_time", result)
        self.assertIn("successful_checks", result)
        self.assertIn("target_stats", result)
        self.assertIn("results", result)
        self.assertIn("all_results", result)

    @patch('github_checker.requests.get')
    def test_full_test_iterations_count(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().test(timeout=5.0)

        self.assertEqual(result["iterations"], FULL_TEST_ITERATIONS)

    @patch('github_checker.requests.get')
    def test_full_test_has_results_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().test(timeout=5.0)

        self.assertIn("results", result)

    @patch('github_checker.requests.get')
    def test_full_test_target_stats(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().test(timeout=5.0)

        self.assertIsInstance(result["target_stats"], dict)
        self.assertIn("homepage", result["target_stats"])
        self.assertIn("api", result["target_stats"])


class TestCheckerTargets(unittest.TestCase):
    def test_targets_has_homepage(self):
        names = [t[0] for t in Checker.TARGETS]
        self.assertIn("homepage", names)

    def test_targets_has_api(self):
        names = [t[0] for t in Checker.TARGETS]
        self.assertIn("api", names)

    def test_targets_count(self):
        self.assertEqual(len(Checker.TARGETS), 2)

    def test_targets_urls_are_strings(self):
        for name, url in Checker.TARGETS:
            self.assertIsInstance(name, str)
            self.assertIsInstance(url, str)
            self.assertTrue(url.startswith("https://"))


class TestConstants(unittest.TestCase):
    def test_default_timeout_positive(self):
        self.assertGreater(DEFAULT_TIMEOUT, 0)
        self.assertIsInstance(DEFAULT_TIMEOUT, float)

    def test_full_test_iterations_positive(self):
        self.assertGreater(FULL_TEST_ITERATIONS, 0)
        self.assertIsInstance(FULL_TEST_ITERATIONS, int)

    def test_response_threshold_positive(self):
        self.assertGreater(RESPONSE_TIME_THRESHOLD_MS, 0)

    def test_full_test_iterations_matches_constant(self):
        self.assertEqual(FULL_TEST_ITERATIONS, 3)


class TestColors(unittest.TestCase):
    def test_colors_have_reset(self):
        self.assertTrue(Colors.RESET)

    def test_colors_have_main_colors(self):
        self.assertTrue(Colors.RED)
        self.assertTrue(Colors.GREEN)
        self.assertTrue(Colors.YELLOW)
        self.assertTrue(Colors.BLUE)

    def test_color_length(self):
        self.assertEqual(len(Colors.RESET), 4)


class TestSpinningCursor(unittest.TestCase):
    def test_spinning_cursor_is_generator(self):
        from github_checker import spinning_cursor
        gen = spinning_cursor()
        self.assertTrue(hasattr(gen, '__iter__'))
        self.assertTrue(hasattr(gen, '__next__'))

    def test_spinning_cursor_chars(self):
        from github_checker import spinning_cursor, SPINNER_CHARS
        gen = spinning_cursor()
        for char in SPINNER_CHARS:
            self.assertEqual(next(gen), char)


class TestMainFunction(unittest.TestCase):
    @patch('github_checker.requests.get')
    @patch('sys.stdout')
    def test_main_with_json_flag(self, mock_stdout, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch.object(sys, 'argv', ['github_checker', '-j']):
            result = main()

        self.assertEqual(result, 0)

    @patch('github_checker.requests.get')
    def test_main_exit_code_on_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch.object(sys, 'argv', ['github_checker']):
            result = main()

        self.assertEqual(result, 0)

    @patch('github_checker.requests.get')
    def test_main_exit_code_on_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with patch.object(sys, 'argv', ['github_checker']):
            try:
                result = main()
            except SystemExit as e:
                result = e.code

        self.assertNotEqual(result, 0)


class TestJsonOutputStructure(unittest.TestCase):
    @patch('github_checker.requests.get')
    def test_json_output_has_required_fields(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        checker = Checker()
        result = checker.check(timeout=5.0)

        self.assertIn("status", result)
        self.assertIn("msg", result)
        self.assertIn("results", result)

    @patch('github_checker.requests.get')
    def test_full_test_json_structure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        checker = Checker()
        result = checker.test(timeout=5.0)

        expected_keys = {"status", "msg", "iterations", "avg_total_time",
                         "successful_checks", "target_stats", "results", "all_results"}
        self.assertTrue(expected_keys.issubset(result.keys()))


class TestEdgeCases(unittest.TestCase):
    @patch('github_checker.requests.get')
    def test_check_with_zero_timeout(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().check(timeout=0.1)
        self.assertIn("status", result)

    @patch('github_checker.requests.get')
    def test_check_very_large_timeout(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Checker().check(timeout=60.0)
        self.assertIn("status", result)

    def test_judge_with_mixed_results(self):
        results = [
            ("homepage", {"ok": True, "ms": 100}),
            ("api", {"ok": False, "error": "Failed"})
        ]
        self.assertEqual(Checker()._judge(results), "warn")

    def test_judge_single_success(self):
        results = [("homepage", {"ok": True, "ms": 100})]
        self.assertEqual(Checker()._judge(results), "good")

    def test_judge_single_failure(self):
        results = [("homepage", {"ok": False})]
        self.assertEqual(Checker()._judge(results), "bad")


if __name__ == '__main__':
    unittest.main()
