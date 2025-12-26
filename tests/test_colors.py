# -*- coding: ascii -*-
"""
Test suite for core.colors module
"""

import sys
from unittest.mock import patch, MagicMock
from core.colors import Colors, enable_ansi_colors, colorize


class TestColors:
    """Test cases for Colors class"""

    def test_colors_class_exists(self):
        """Test that Colors class exists and has expected attributes"""
        assert hasattr(Colors, 'RESET')
        assert hasattr(Colors, 'BOLD')
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'YELLOW')
        assert hasattr(Colors, 'BLUE')
        assert hasattr(Colors, 'CYAN')
        assert hasattr(Colors, 'WHITE')
        assert hasattr(Colors, 'MAGENTA')

    def test_colors_reset(self):
        """Test RESET color code"""
        assert Colors.RESET == '\033[0m'

    def test_colors_bold(self):
        """Test BOLD color code"""
        assert Colors.BOLD == '\033[1m'

    def test_colors_foreground(self):
        """Test foreground color codes"""
        assert Colors.RED == '\033[31m'
        assert Colors.GREEN == '\033[32m'
        assert Colors.YELLOW == '\033[33m'
        assert Colors.BLUE == '\033[34m'
        assert Colors.MAGENTA == '\033[35m'
        assert Colors.CYAN == '\033[36m'
        assert Colors.WHITE == '\033[37m'

    def test_colors_background(self):
        """Test background color codes"""
        assert Colors.BG_RED == '\033[41m'
        assert Colors.BG_GREEN == '\033[42m'
        assert Colors.BG_YELLOW == '\033[43m'


class TestColorize:
    """Test cases for colorize function"""

    def test_colorize_red(self):
        """Test colorizing text with red"""
        result = colorize("Hello", Colors.RED)
        assert '\033[31m' in result
        assert 'Hello' in result
        assert '\033[0m' in result

    def test_colorize_green(self):
        """Test colorizing text with green"""
        result = colorize("World", Colors.GREEN)
        assert '\033[32m' in result
        assert 'World' in result
        assert '\033[0m' in result

    def test_colorize_yellow(self):
        """Test colorizing text with yellow"""
        result = colorize("Warning", Colors.YELLOW)
        assert '\033[33m' in result
        assert 'Warning' in result
        assert '\033[0m' in result

    def test_colorize_empty_string(self):
        """Test colorizing empty string"""
        result = colorize("", Colors.RED)
        assert result == '\033[31m\033[0m'

    def test_colorize_preserves_text(self):
        """Test that colorize preserves original text"""
        original_text = "Test message"
        result = colorize(original_text, Colors.BLUE)
        assert original_text in result

    def test_colorize_with_bold(self):
        """Test colorizing with bold attribute"""
        result = colorize("Bold text", Colors.BOLD)
        assert '\033[1m' in result
        assert 'Bold text' in result
        assert '\033[0m' in result


class TestEnableAnsiColors:
    """Test cases for enable_ansi_colors function"""

    @patch('core.colors.sys.platform', 'win32')
    def test_enable_ansi_colors_windows_already_enabled(self):
        """Test enable_ansi_colors on Windows when already enabled"""
        # Mock kernel32 module
        mock_kernel32 = MagicMock()
        mock_kernel32.GetStdHandle.return_value = MagicMock()
        mock_kernel32.GetConsoleMode.return_value.value = 0x0004 | 0x0001

        with patch('ctypes.windll.kernel32', mock_kernel32):
            result = enable_ansi_colors()
            assert result is True

    @patch('core.colors.sys.platform', 'win32')
    def test_enable_ansi_colors_windows_needs_enabling(self):
        """Test enable_ansi_colors on Windows when needs enabling"""

        mock_kernel32 = MagicMock()
        mock_stdout_handle = MagicMock()
        mock_kernel32.GetStdHandle.return_value = mock_stdout_handle

        mock_mode = MagicMock()
        mock_mode.value = 0x0001
        mock_kernel32.GetConsoleMode.return_value = mock_mode

        with patch('ctypes.windll.kernel32', mock_kernel32):
            result = enable_ansi_colors()
            assert result is True

    @patch('core.colors.sys.platform', 'win32')
    def test_enable_ansi_colors_windows_exception(self):
        """Test enable_ansi_colors on Windows when exception occurs"""

        mock_kernel32 = MagicMock()
        mock_kernel32.GetStdHandle.side_effect = Exception("Test error")

        with patch('ctypes.windll.kernel32', mock_kernel32):
            result = enable_ansi_colors()
            assert result is False

    @patch('core.colors.sys.platform', 'linux')
    def test_enable_ansi_colors_linux(self):
        """Test enable_ansi_colors on Linux (always returns True)"""
        result = enable_ansi_colors()
        assert result is True

    @patch('core.colors.sys.platform', 'darwin')
    def test_enable_ansi_colors_macos(self):
        """Test enable_ansi_colors on macOS (always returns True)"""
        result = enable_ansi_colors()
        assert result is True
