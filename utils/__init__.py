# -*- coding: ascii -*-
"""
Utils package for GitHub Checker

Contains utility modules:
- constants: Application-wide constants
- animation: Spinner animation utilities

Author: GitHub Checker Project
"""

from utils.constants import (
    DEFAULT_TIMEOUT,
    FULL_TEST_ITERATIONS,
    MIN_REMAIN_TIMEOUT,
    RESPONSE_TIME_THRESHOLD_MS,
    RESPONSE_TIME_THRESHOLD_SEC,
    SPINNER_PADDING,
    SPINNER_JOIN_TIMEOUT,
    SPINNER_DELAY,
    SPINNER_CHARS,
    VERSION
)

from utils.animation import (
    spinning_cursor,
    start_spinner,
    stop_spinner
)

__all__ = [
    # Constants
    'DEFAULT_TIMEOUT',
    'FULL_TEST_ITERATIONS',
    'MIN_REMAIN_TIMEOUT',
    'RESPONSE_TIME_THRESHOLD_MS',
    'RESPONSE_TIME_THRESHOLD_SEC',
    'SPINNER_PADDING',
    'SPINNER_JOIN_TIMEOUT',
    'SPINNER_DELAY',
    'SPINNER_CHARS',
    'VERSION',
    # Animation
    'spinning_cursor',
    'start_spinner',
    'stop_spinner'
]
