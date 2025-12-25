# -*- coding: ascii -*-
"""
UI package for GitHub Checker

Contains modules for user interface and output formatting:
- themes: Theme definitions and rendering functions

Author: GitHub Checker Project
"""

from ui.themes import (
    format_status,
    format_fun_status,
    render_minimal_theme,
    render_fun_theme,
    render_default_theme
)

__all__ = [
    'format_status',
    'format_fun_status',
    'render_minimal_theme',
    'render_fun_theme',
    'render_default_theme'
]
