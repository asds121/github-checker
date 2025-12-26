import itertools
import sys
import threading
import time
from typing import Iterator
from utils.constants import SPINNER_CHARS, SPINNER_DELAY, SPINNER_JOIN_TIMEOUT, SPINNER_PADDING

# -*- coding: ascii -*-
"""
Animation utilities for GitHub Checker

Provides spinner animation and cursor effects for CLI output.

Author: GitHub Checker Project
"""



# Global event to control spinner thread stopping
_spinner_stop_event = threading.Event()


def spinning_cursor() -> Iterator[str]:
    """
    Generator that yields spinning cursor animation

    Yields:
        str: Spinning cursor characters
    """
    while True:
        for cursor in SPINNER_CHARS:  # Spinner character sequence
            yield cursor  # Generate next cursor character


def start_spinner() -> threading.Thread:
    """
    Start the spinner animation in a background thread

    Returns:
        threading.Thread: The spinner thread
    """
    # Reset the stop event for new spinner
    _spinner_stop_event.clear()

    spinner_thread = None


    def show_spinner():
        for cursor in itertools.cycle(SPINNER_CHARS):
            if _spinner_stop_event.is_set():
                break
            sys.stdout.write('\b' + cursor)
            sys.stdout.flush()
            time.sleep(SPINNER_DELAY)

    spinner_thread = threading.Thread(target=show_spinner)
    spinner_thread.daemon = True
    spinner_thread.start()

    return spinner_thread


def stop_spinner(spinner_thread: threading.Thread) -> None:
    """
    Stop the spinner animation

    Args:
        spinner_thread: The spinner thread to stop
    """
    if spinner_thread is not None:
        # Signal the spinner to stop
        _spinner_stop_event.set()
        # Wait for thread to join with timeout
        spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\r" + " " * SPINNER_PADDING + "\r", end="")
