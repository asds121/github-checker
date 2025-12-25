# -*- coding: ascii -*-
"""
Constants module for GitHub Checker

Contains all constants used throughout the application including:
- Request timeout settings
- Response time thresholds
- Spinner animation configurations

Author: GitHub Checker Project
"""

# Request timeout settings
DEFAULT_TIMEOUT = 8.0  # Default request timeout in seconds
FULL_TEST_ITERATIONS = 3  # Number of iterations for full test
MIN_REMAIN_TIMEOUT = 1.0  # Minimum remaining timeout for subsequent requests

# Response time thresholds
RESPONSE_TIME_THRESHOLD_MS = 3000  # Response time threshold in milliseconds
RESPONSE_TIME_THRESHOLD_SEC = 3.0  # Response time threshold in seconds

# Spinner animation constants
SPINNER_PADDING = 50  # Number of spaces to clear spinner animation
SPINNER_JOIN_TIMEOUT = 0.2  # Timeout for joining spinner thread (seconds)
SPINNER_DELAY = 0.1  # Delay between spinner frames (seconds)
SPINNER_CHARS = '|/\\-'  # Spinner character sequence

# Version information
VERSION = "1.1.0"
