# -*- coding: ascii -*-
"""
Animation utilities for GitHub Checker

Provides spinner animation and cursor effects for CLI output.

Author: GitHub Checker Project
"""

import itertools
import sys
import threading
import time
from typing import Iterator

from utils.constants import SPINNER_CHARS, SPINNER_DELAY, SPINNER_JOIN_TIMEOUT, SPINNER_PADDING


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
    spinner_thread = None

    def show_spinner():
        for cursor in itertools.cycle(SPINNER_CHARS):
            if hasattr(show_spinner, 'done'):
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
        if 'show_spinner' in locals() or hasattr(sys.modules[__name__], 'show_spinner'):
            try:
                show_spinner.done = True
            except NameError:
                pass
        spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\r" + " " * SPINNER_PADDING + "\r", end="")
