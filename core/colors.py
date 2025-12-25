# -*- coding: ascii -*-
"""
Colors module for GitHub Checker

Provides ANSI color codes and color utility functions for terminal output.

Author: GitHub Checker Project
"""

import sys


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'


def enable_ansi_colors() -> bool:
    """
    Enable ANSI colors on Windows terminal

    Returns:
        bool: True if ANSI colors were enabled or already available, False otherwise
    """
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            STD_OUTPUT_HANDLE = -11
            hOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            dwMode = ctypes.c_ulong()
            kernel32.GetConsoleMode(hOut, ctypes.byref(dwMode))
            if not (dwMode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING):
                kernel32.SetConsoleMode(hOut, dwMode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
                return True
            return True
        except Exception:
            return False
    return True


def colorize(text: str, color: str) -> str:
    """
    Apply color to text using ANSI codes

    Args:
        text (str): Text to colorize
        color (str): ANSI color code

    Returns:
        str: Colorized text
    """
    return f"{color}{text}{Colors.RESET}"
