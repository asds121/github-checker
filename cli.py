# -*- coding: ascii -*-
"""
CLI module for GitHub Checker

Provides command-line argument parsing and main entry point.

Author: GitHub Checker Project
"""

import argparse
import json
import sys
import os
import random
from datetime import datetime
from typing import Dict, Any
from requests.exceptions import RequestException
from core import Checker
from utils import DEFAULT_TIMEOUT, VERSION
from ui.themes import (
    render_minimal_theme,
    render_fun_theme,
    render_default_theme,
    render_share_theme,
    generate_share_text
)


def show_intro() -> None:
    """
    Display the tool's value proposition
    """
    print("=" * 50)
    print("GitHub Network Status Checker - Solve Your GitHub Connection Anxiety")
    print("=" * 50)
    print("Core Value:")
    print("  * Quickly detect GitHub accessibility, avoid wasted operations")
    print("  * Provide response time reference, optimize your workflow")
    print("  * Give specific suggestions, reduce troubleshooting time")
    print("=" * 50)
    print()


WELCOME_MESSAGES = [
    "[ROCKET] GitHub Checker ready! Let's see if GitHub is awake...",
    "[BOLT] Checking GitHub accessibility... Fingers crossed!",
    "[MAG] Probing GitHub connection... One moment please...",
    "[GLOBE] Connecting to GitHub... Hello, world!",
    "[WRENCH] GitHub Checker v{version} is warming up...".format(version=VERSION),
]

# Feedback collection configuration
FEEDBACK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "feedback")
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "user_feedback.jsonl")


def ensure_feedback_dir() -> None:
    """Ensure feedback directory exists"""
    if not os.path.exists(FEEDBACK_DIR):
        os.makedirs(FEEDBACK_DIR, exist_ok=True)


def save_feedback(rating: int, feedback_type: str, comment: str, result_data: Dict[str, Any]) -> bool:
    """
    Save user feedback to file

    Args:
        rating: User rating (1-5)
        feedback_type: Type of feedback (useful, unclear, suggestion, bug, other)
        comment: User's comment
        result_data: Related check result data

    Returns:
        bool: Whether save was successful
    """
    try:
        ensure_feedback_dir()
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "feedback_type": feedback_type,
            "comment": comment,
            "version": VERSION,
            "result_status": result_data.get("status"),
            "is_full_test": result_data.get("is_full_test", False)
        }
        with open(FEEDBACK_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_entry, ensure_ascii=False) + '\n')
        return True
    except Exception:
        return False


def collect_feedback(result_data: Dict[str, Any]) -> bool:
    """
    Interactively collect user feedback

    Args:
        result_data: Result data from the check

    Returns:
        bool: Whether feedback was submitted
    """
    print("\n" + "=" * 50)
    print("Help us improve!")
    print("=" * 50)
    print("Was this tool helpful to you?")
    print("  1 - Not helpful")
    print("  2 - Slightly helpful")
    print("  3 - Moderately helpful")
    print("  4 - Very helpful")
    print("  5 - Extremely helpful")

    rating_input = input("\nPlease enter your rating (1-5) or press Enter to skip: ").strip()

    if not rating_input:
        print("Thanks for using GitHub Checker!")
        return False

    try:
        rating = int(rating_input)
        if rating < 1 or rating > 5:
            print("Invalid rating. Please enter a number between 1-5.")
            return False
    except ValueError:
        print("Invalid input. Please enter a number between 1-5.")
        return False

    print("\nFeedback type:")
    print("  1 - [useful] Useful feature")
    print("  2 - [unclear] Unclear documentation")
    print("  3 - [suggestion] Feature suggestion")
    print("  4 - [bug] Bug report")
    print("  5 - [other] Other")

    type_input = input("\nPlease select feedback type (1-5) or press Enter to skip: ").strip()

    feedback_type_map = {
        "1": "useful",
        "2": "unclear",
        "3": "suggestion",
        "4": "bug",
        "5": "other"
    }

    feedback_type = feedback_type_map.get(type_input, "other")

    comment = input("\nAny additional comments? (optional, press Enter to skip): ").strip()

    if save_feedback(rating, feedback_type, comment, result_data):
        print("\nThank you for your feedback! It helps us improve the tool.")
        return True
    else:
        print("\nFailed to save feedback. But thank you for trying!")
        return False


def show_quick_feedback_prompt() -> None:
    """Show quick feedback prompt at the end of execution"""
    print("\n" + "-" * 50)
    print("Love it? Hate it? Tell us!")
    print("Run with --feedback to share your thoughts")
    print("-" * 50)


def show_welcome() -> None:
    """
    Display a friendly welcome message
    """
    print("=" * 50)
    print("GitHub Network Status Checker")
    print(f"Version: {VERSION}")
    print(random.choice(WELCOME_MESSAGES))
    print("=" * 50)


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="GitHub Network Status Checker")
    # Add full test mode parameter
    parser.add_argument('-f', '--full-test', action='store_true',
                        help='Perform full test with multiple checks')
    # Add JSON output parameter
    parser.add_argument('-j', '--json', action='store_true',
                        help='Output results in JSON format')
    # Add theme parameter
    parser.add_argument('-t', '--theme', choices=['default', 'minimal', 'fun', 'share'],
                        default='default', help='Output theme (default: default)')
    # Add share text parameter for concise output
    parser.add_argument('-s', '--share', action='store_true',
                        help='Generate concise shareable text')
    # Add intro parameter to show value proposition
    parser.add_argument('-i', '--intro', action='store_true',
                        help='Show tool value proposition')
    # Add quiet mode parameter
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Run in quiet mode with minimal output')
    # Add timeout parameter
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                        help=f'Request timeout in seconds (default: {DEFAULT_TIMEOUT})')
    # Add interactive feedback parameter
    parser.add_argument('--feedback', action='store_true',
                        help='Prompt for user feedback after check')
    return parser


def show_result(result: Dict[str, Any], args) -> None:
    """
    Display the check result

    Args:
        result: Dictionary containing check result
        args: Parsed command-line arguments
    """
    if args.json:
        # Output in JSON format
        result['timestamp'] = datetime.now().isoformat()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.share:
        # Generate shareable text
        share_text = generate_share_text(result, args.theme)
        print(share_text)
        return

    # Choose theme for rendering
    theme_renderers = {
        'default': render_default_theme,
        'minimal': render_minimal_theme,
        'fun': render_fun_theme,
        'share': render_share_theme
    }

    renderer = theme_renderers.get(args.theme, render_default_theme)
    renderer(result)

    if args.feedback:
        collect_feedback(result)


def main() -> int:
    """
    Main function

    Returns:
        int: Exit code (0=success, 1=interrupt, 2=bad args, 3=error, 4=network error)
    """
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.intro:
            show_intro()
            return 0

        show_welcome()

        checker = Checker()

        if args.full_test:
            result = checker.test(iterations=3, timeout=args.timeout)
        else:
            result = checker.check(timeout=args.timeout)

        show_result(result, args)

        if args.feedback:
            collect_feedback(result)
        else:
            show_quick_feedback_prompt()

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except RequestException as e:
        print(f"\nNetwork error: {e}")
        return 4
    except SystemExit:
        raise
    except Exception as e:
        print(f"\nError: {e}")
        return 3


if __name__ == '__main__':
    sys.exit(main())

