# -*- coding: ascii -*-
"""
Core package for GitHub Checker

Contains core functionality modules:
- colors: ANSI color codes and utilities
- checker: Main GitHub accessibility checking functionality

Author: GitHub Checker Project
"""

from core.colors import (
    Colors,
    colorize,
    enable_ansi_colors
)

from core.checker import (
    Checker
)

__all__ = [
    # Colors
    'Colors',
    'colorize',
    'enable_ansi_colors',
    # Checker
    'Checker'
]
