import sys
import threading
import time
from unittest.mock import patch, MagicMock
from utils.animation import spinning_cursor, start_spinner, stop_spinner
from utils.constants import SPINNER_CHARS, SPINNER_DELAY, SPINNER_JOIN_TIMEOUT, SPINNER_PADDING

# -*- coding: ascii -*-
"""
Test suite for utils.animation module
"""



class TestSpinningCursor:
    """Test cases for spinning_cursor function"""


    def test_spinning_cursor_returns_iterator(self):
        """Test that spinning_cursor returns an iterator"""
        cursor = spinning_cursor()
        assert hasattr(cursor, '__iter__')
        assert hasattr(cursor, '__next__')


    def test_spinning_cursor_yields_spinner_chars(self):
        """Test that spinning_cursor yields characters from SPINNER_CHARS"""
        cursor = spinning_cursor()
        # Get several characters and verify they're from the spinner chars
        for _ in range(5):
            char = next(cursor)
            assert char in SPINNER_CHARS


    def test_spinning_cursor_infinite_iterator(self):
        """Test that spinning_cursor is infinite (wraps around)"""
        cursor = spinning_cursor()
        # Get more characters than in SPINNER_CHARS to verify wrapping
        chars = [next(cursor) for _ in range(len(SPINNER_CHARS) + 5)]
        # Should have wrapped around at least once
        assert len(chars) > len(SPINNER_CHARS)


    def test_spinning_cursor_all_chars_from_set(self):
        """Test that all yielded chars are from SPINNER_CHARS"""
        cursor = spinning_cursor()
        for _ in range(100):
            char = next(cursor)
            assert char in SPINNER_CHARS


class TestStartSpinner:
    """Test cases for start_spinner function"""

    @patch('utils.animation.sys.stdout')


    def test_start_spinner_returns_thread(self, mock_stdout):
        """Test that start_spinner returns a thread object"""
        thread = start_spinner()
        assert isinstance(thread, threading.Thread)
        # Clean up
        stop_spinner(thread)
        time.sleep(0.1)

    @patch('utils.animation.sys.stdout')
    @patch('utils.animation.time.sleep')


    def test_start_spinner_is_daemon(self, mock_sleep, mock_stdout):
        """Test that spinner thread is daemon"""
        thread = start_spinner()
        assert thread.daemon == True
        # Clean up
        stop_spinner(thread)

    @patch('utils.animation.sys.stdout')


    def test_start_spinner_writes_to_stdout(self, mock_stdout):
        """Test that spinner writes to stdout"""
        thread = start_spinner()
        time.sleep(SPINNER_DELAY * 2)
        assert mock_stdout.write.called
        assert mock_stdout.flush.called
        # Clean up
        stop_spinner(thread)
        time.sleep(0.1)


class TestStopSpinner:
    """Test cases for stop_spinner function"""

    @patch('utils.animation.sys.stdout')


    def test_stop_spinner_with_none(self, mock_stdout):
        """Test stop_spinner with None thread"""
        # Should not raise exception
        stop_spinner(None)

    @patch('utils.animation.sys.stdout')


    def test_stop_spinner_clears_cursor(self, mock_stdout):
        """Test that stop_spinner clears the spinner cursor"""
        thread = start_spinner()
        time.sleep(SPINNER_DELAY * 2)
        stop_spinner(thread)
        time.sleep(0.1)
        # Should have written spaces to clear cursor
        assert mock_stdout.write.called

    @patch('utils.animation.sys.stdout')


    def test_stop_spinner_joins_thread(self, mock_stdout):
        """Test that stop_spinner joins the thread"""
        thread = start_spinner()
        time.sleep(SPINNER_DELAY * 5)  # Wait longer for thread to finish
        stop_spinner(thread)
        time.sleep(0.5)  # Give time for join to complete
        # Thread should be not alive
        assert not thread.is_alive()


class TestSpinnerConstants:
    """Test cases for spinner-related constants"""


    def test_spinner_chars_not_empty(self):
        """Test that SPINNER_CHARS is not empty"""
        assert len(SPINNER_CHARS) > 0


    def test_spinner_delay_positive(self):
        """Test that SPINNER_DELAY is positive"""
        assert SPINNER_DELAY > 0
        assert SPINNER_DELAY < 1  # Should be reasonable delay


    def test_spinner_join_timeout_positive(self):
        """Test that SPINNER_JOIN_TIMEOUT is positive"""
        assert SPINNER_JOIN_TIMEOUT > 0


    def test_spinner_padding_reasonable(self):
        """Test that SPINNER_PADDING is reasonable"""
        assert SPINNER_PADDING >= len(SPINNER_CHARS)
