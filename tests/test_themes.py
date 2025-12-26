# -*- coding: ascii -*-
"""
Comprehensive tests for ui.themes module

Tests theme formatting and rendering functions for CLI output.

Author: GitHub Checker Project
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest

from ui.themes import (
    format_status,
    format_fun_status,
    get_emoji,
    format_fun_emoji_status,
    render_minimal_theme,
    render_fun_theme,
    render_default_theme,
    render_share_theme,
    generate_share_text,
    FUN_STATUS_MESSAGES,
    EMOJI_MAP
)


class TestFormatStatus(unittest.TestCase):
    """Test cases for format_status() function"""

    def test_format_status_good(self):
        """Test format_status with good status"""
        result = format_status("good", "All systems operational")
        self.assertIn("[OK]", result)
        self.assertIn("All systems operational", result)

    def test_format_status_warn(self):
        """Test format_status with warn status"""
        result = format_status("warn", "Some issues detected")
        self.assertIn("[WARN]", result)
        self.assertIn("Some issues detected", result)

    def test_format_status_bad(self):
        """Test format_status with bad status"""
        result = format_status("bad", "Connection failed")
        self.assertIn("[FAIL]", result)
        self.assertIn("Connection failed", result)

    def test_format_status_unknown(self):
        """Test format_status with unknown status"""
        result = format_status("unknown", "Something weird")
        self.assertIn("[UNKNOWN]", result)
        self.assertIn("Something weird", result)


class TestFormatFunStatus(unittest.TestCase):
    """Test cases for format_fun_status() function"""

    def test_format_fun_status_good_super_fast(self):
        """Test format_fun_status for good status with fast response"""
        result = format_fun_status("good", avg_ms=100)
        self.assertIn("GitHub", result)

    def test_format_fun_status_good_normal(self):
        """Test format_fun_status for good status with normal response"""
        result = format_fun_status("good", avg_ms=700)
        self.assertIn("GitHub", result)

    def test_format_fun_status_good_accessible(self):
        """Test format_fun_status for good status with slow but accessible response"""
        result = format_fun_status("good", avg_ms=2000)
        self.assertIn("GitHub", result)

    def test_format_fun_status_good_no_ms(self):
        """Test format_fun_status for good status without avg_ms"""
        result = format_fun_status("good")
        self.assertIn("GitHub", result)

    def test_format_fun_status_warn_slow_github(self):
        """Test format_fun_status for warn status with very slow response"""
        result = format_fun_status("warn", avg_ms=4000)
        self.assertIn("GitHub", result)

    def test_format_fun_status_warn_somewhat_slow(self):
        """Test format_fun_status for warn status with moderate response"""
        result = format_fun_status("warn", avg_ms=2000)
        self.assertIn("GitHub", result)

    def test_format_fun_status_bad(self):
        """Test format_fun_status for bad status"""
        result = format_fun_status("bad")
        self.assertIn("GitHub", result)

    def test_format_fun_status_returns_string(self):
        """Test format_fun_status always returns a string"""
        result = format_fun_status("good", 100)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


class TestGetEmoji(unittest.TestCase):
    """Test cases for get_emoji() function"""

    def test_get_emoji_good(self):
        """Test get_emoji returns valid emoji for good status"""
        result = get_emoji("good")
        self.assertIn(result, EMOJI_MAP["good"])

    def test_get_emoji_warn(self):
        """Test get_emoji returns valid emoji for warn status"""
        result = get_emoji("warn")
        self.assertIn(result, EMOJI_MAP["warn"])

    def test_get_emoji_bad(self):
        """Test get_emoji returns valid emoji for bad status"""
        result = get_emoji("bad")
        self.assertIn(result, EMOJI_MAP["bad"])

    def test_get_emoji_unknown(self):
        """Test get_emoji returns default for unknown status"""
        result = get_emoji("unknown")
        self.assertEqual(result, "[?]")

    def test_get_emoji_returns_string(self):
        """Test get_emoji always returns a string"""
        for status in ["good", "warn", "bad", "unknown"]:
            result = get_emoji(status)
            self.assertIsInstance(result, str)


class TestFormatFunEmojiStatus(unittest.TestCase):
    """Test cases for format_fun_emoji_status() function"""

    def test_format_fun_emoji_status_good(self):
        """Test format_fun_emoji_status with good status"""
        result = format_fun_emoji_status("good", 100)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_format_fun_emoji_status_warn(self):
        """Test format_fun_emoji_status with warn status"""
        result = format_fun_emoji_status("warn", 3000)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_format_fun_emoji_status_bad(self):
        """Test format_fun_emoji_status with bad status"""
        result = format_fun_emoji_status("bad")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_format_fun_emoji_status_contains_emoji(self):
        """Test format_fun_emoji_status contains an emoji"""
        result = format_fun_emoji_status("good", 100)
        # Should contain brackets which indicate emoji placeholders
        self.assertIn("[", result)
        self.assertIn("]", result)


class TestRenderMinimalTheme(unittest.TestCase):
    """Test cases for render_minimal_theme() function"""

    def test_render_minimal_theme_good(self):
        """Test render_minimal_theme with good status"""
        result = {
            'status': 'good',
            'msg': 'All good',
            'results': [
                ('homepage', {'ok': True, 'ms': 100}),
                ('api', {'ok': True, 'ms': 150})
            ]
        }
        output = render_minimal_theme(result)
        self.assertIn("All good", output)

    def test_render_minimal_theme_bad(self):
        """Test render_minimal_theme with bad status"""
        result = {
            'status': 'bad',
            'msg': 'Issues detected',
            'results': [
                ('homepage', {'ok': False, 'error': 'timeout'})
            ]
        }
        output = render_minimal_theme(result)
        self.assertIn("Issues detected", output)

    def test_render_minimal_theme_warn(self):
        """Test render_minimal_theme with warn status"""
        result = {
            'status': 'warn',
            'msg': 'Some issues',
            'results': [
                ('api', {'ok': True, 'ms': 3000})
            ]
        }
        output = render_minimal_theme(result)
        self.assertIn("Some issues", output)


class TestRenderFunTheme(unittest.TestCase):
    """Test cases for render_fun_theme() function"""

    def test_render_fun_theme_good(self):
        """Test render_fun_theme with good status"""
        result = {
            'status': 'good',
            'msg': 'Fast response!',
            'results': [
                ('homepage', {'ok': True, 'ms': 50}),
                ('api', {'ok': True, 'ms': 80})
            ]
        }
        output = render_fun_theme(result)
        # Fun theme shows results, status, and fun message
        self.assertIn("Status:", output)
        self.assertIn("GOOD", output)
        self.assertIn("homepage", output)

    def test_render_fun_theme_bad(self):
        """Test render_fun_theme with bad status"""
        result = {
            'status': 'bad',
            'msg': 'Oh no!',
            'results': [
                ('homepage', {'ok': False, 'error': 'Failed'})
            ]
        }
        output = render_fun_theme(result)
        # Fun theme shows status
        self.assertIn("Status:", output)
        self.assertIn("BAD", output)
        self.assertIn("homepage", output)

    def test_render_fun_theme_warn(self):
        """Test render_fun_theme with warn status"""
        result = {
            'status': 'warn',
            'msg': 'Slow but working',
            'results': [
                ('api', {'ok': True, 'ms': 5000})
            ]
        }
        output = render_fun_theme(result)
        # Fun theme shows status
        self.assertIn("Status:", output)
        self.assertIn("WARN", output)
        self.assertIn("api", output)


class TestRenderDefaultTheme(unittest.TestCase):
    """Test cases for render_default_theme() function"""

    def test_render_default_theme_good(self):
        """Test render_default_theme with good status"""
        result = {
            'status': 'good',
            'msg': 'All systems operational',
            'results': [
                ('homepage', {'ok': True, 'ms': 100}),
                ('api', {'ok': True, 'ms': 150})
            ]
        }
        output = render_default_theme(result)
        self.assertIsInstance(output, str)
        self.assertIn("Status:", output)
        self.assertIn("GOOD", output)

    def test_render_default_theme_bad(self):
        """Test render_default_theme with bad status"""
        result = {
            'status': 'bad',
            'msg': 'Systems down',
            'results': [
                ('homepage', {'ok': False, 'error': 'Connection refused'})
            ]
        }
        output = render_default_theme(result)
        self.assertIsInstance(output, str)
        self.assertIn("Status:", output)
        self.assertIn("BAD", output)

    def test_render_default_theme_warn(self):
        """Test render_default_theme with warn status"""
        result = {
            'status': 'warn',
            'msg': 'Degraded performance',
            'results': [
                ('api', {'ok': True, 'ms': 3500})
            ]
        }
        output = render_default_theme(result)
        self.assertIsInstance(output, str)
        self.assertIn("Status:", output)
        self.assertIn("WARN", output)


class TestGetAvailableThemes(unittest.TestCase):
    """Test cases for theme availability (check that theme functions work)"""

    def test_themes_functions_are_callable(self):
        """Test that theme rendering functions are callable"""
        self.assertTrue(callable(render_minimal_theme))
        self.assertTrue(callable(render_fun_theme))
        self.assertTrue(callable(render_default_theme))
        self.assertTrue(callable(render_share_theme))
        self.assertTrue(callable(generate_share_text))

    def test_theme_rendering_produces_string(self):
        """Test that theme rendering produces string output"""
        result = {
            'status': 'good',
            'msg': 'Test message',
            'results': []
        }
        self.assertIsInstance(render_minimal_theme(result), str)

    def test_all_status_functions_work(self):
        """Test that all status formatting functions work"""
        self.assertIsInstance(format_status("good", "test"), str)
        self.assertIsInstance(format_fun_status("good"), str)
        self.assertIsInstance(format_fun_emoji_status("good"), str)
        self.assertIsInstance(get_emoji("good"), str)


class TestGetThemeDescription(unittest.TestCase):
    """Test cases for theme descriptions (check format functions)"""

    def test_status_messages_exist(self):
        """Test that status message constants exist"""
        self.assertIn("good", FUN_STATUS_MESSAGES)
        self.assertIn("warn", FUN_STATUS_MESSAGES)
        self.assertIn("bad", FUN_STATUS_MESSAGES)

    def test_emoji_map_exists(self):
        """Test that emoji map constants exist"""
        self.assertIn("good", EMOJI_MAP)
        self.assertIn("warn", EMOJI_MAP)
        self.assertIn("bad", EMOJI_MAP)

    def test_emoji_map_has_valid_values(self):
        """Test that emoji map values are lists"""
        for status, emojis in EMOJI_MAP.items():
            self.assertIsInstance(emojis, list)
            for emoji in emojis:
                self.assertIsInstance(emoji, str)


class TestRenderShareTheme(unittest.TestCase):
    """Test cases for render_share_theme() function"""

    def test_render_share_theme_good(self):
        """Test render_share_theme with good status"""
        result = {
            'status': 'good',
            'msg': 'GitHub is accessible',
            'results': [
                ('homepage', {'ok': True, 'ms': 100})
            ]
        }
        output = render_share_theme(result)
        # Share theme shows status report header and status
        self.assertIn("GitHub Status Report", output)
        self.assertIn("OK", output)
        self.assertIn("GOOD", output)

    def test_render_share_theme_bad(self):
        """Test render_share_theme with bad status"""
        result = {
            'status': 'bad',
            'msg': 'GitHub is down',
            'results': [
                ('homepage', {'ok': False, 'error': 'timeout'})
            ]
        }
        output = render_share_theme(result)
        # Share theme shows status report header and status
        self.assertIn("GitHub Status Report", output)
        self.assertIn("FAIL", output)
        self.assertIn("BAD", output)


class TestGenerateShareText(unittest.TestCase):
    """Test cases for generate_share_text() function"""

    def test_generate_share_text_default_theme(self):
        """Test generate_share_text with default theme"""
        result = {
            'status': 'good',
            'msg': 'All good',
            'results': []
        }
        text = generate_share_text(result, 'default')
        self.assertIsInstance(text, str)
        # Default theme returns formatted output
        self.assertIn("Status:", text)

    def test_generate_share_text_minimal_theme(self):
        """Test generate_share_text with minimal theme"""
        result = {
            'status': 'good',
            'msg': 'OK',
            'results': []
        }
        text = generate_share_text(result, 'minimal')
        self.assertIsInstance(text, str)
        self.assertIn("STATUS:", text)

    def test_generate_share_text_fun_theme(self):
        """Test generate_share_text with fun theme"""
        result = {
            'status': 'good',
            'msg': 'Great!',
            'results': []
        }
        text = generate_share_text(result, 'fun')
        self.assertIsInstance(text, str)
        # Fun theme shows DETECTION RESULTS
        self.assertIn("DETECTION RESULTS", text)


if __name__ == '__main__':
    unittest.main()
