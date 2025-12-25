# -*- coding: ascii -*-
"""
CLI module for GitHub Checker

Provides command-line argument parsing and main entry point.

Author: GitHub Checker Project
"""

import argparse
import json
import sys
import time
import requests
from typing import Dict, Any

from core import Checker, enable_ansi_colors
from utils import DEFAULT_TIMEOUT, VERSION
from utils.animation import start_spinner, stop_spinner
from ui.themes import render_minimal_theme, render_fun_theme, render_default_theme


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
    parser.add_argument('-t', '--theme', choices=['default', 'minimal', 'fun'],
                        default='default', help='Output theme (default: default)')
    # Add intro parameter to show value proposition
    parser.add_argument('-i', '--intro', action='store_true',
                        help='Show tool value proposition')
    return parser


def generate_suggestion(r: Dict[str, Any]) -> str:
    """
    Generate user-friendly suggestion based on status

    Args:
        r: Result dictionary containing test results

    Returns:
        str: Suggestion message
    """
    if r["status"] == "good":
        return "Network is stable, you can push code normally."
    elif r["status"] == "warn":
        failed_targets = [name for name, result in r.get("results", [])
                          if not result.get("ok")]
        if failed_targets:
            msg = f"Network is unstable for {', '.join(failed_targets)}. "
            return msg + "Try again later."
        else:
            return "Network is slow but accessible."
    else:
        return "Network connection failed."


def generate_json_output(r: Dict[str, Any], is_full_test: bool) -> Dict[str, Any]:
    """
    Generate JSON output from test results

    Args:
        r: Result dictionary containing test results
        is_full_test: Whether this is a full test

    Returns:
        Dict[str, Any]: JSON output structure
    """
    json_output = {
        "version": "v" + VERSION,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": r["status"],
        "message": r["msg"],
        "is_full_test": is_full_test
    }

    if is_full_test:
        json_output.update({
            "iterations": r["iterations"],
            "successful_checks": r["successful_checks"],
            "avg_total_time_ms": round(r["avg_total_time"], 2),
            "target_stats": {
                name: {
                    "avg_response_ms": round(stats["avg_response"], 2),
                    "success_rate": round(stats["success_rate"], 2)
                }
                for name, stats in r["target_stats"].items()
            }
        })
    else:
        json_output["results"] = [
            {
                "target": name,
                "status": "OK" if result.get("ok") else "FAIL",
                "response_time_ms": round(result.get("ms", 0), 2) if result.get("ok") else None,
                "error": result.get("error") if not result.get("ok") else None
            }
            for name, result in r["results"]
        ]

    json_output["suggestion"] = generate_suggestion(r)
    return json_output


def run_with_theme(r: Dict[str, Any], theme: str, is_full_test: bool) -> None:
    """
    Run output based on theme

    Args:
        r: Result dictionary containing test results
        theme: Theme name
        is_full_test: Whether this is a full test
    """
    if theme == "minimal":
        print(render_minimal_theme(r))
    elif theme == "fun":
        print(render_fun_theme(r, is_full_test))
    else:
        print(render_default_theme(r, is_full_test))


def main() -> int:
    """
    Main function: Execute GitHub accessibility check main logic

    This function is responsible for:
    1. Parsing command line arguments
    2. Starting animation indicator
    3. Executing checks
    4. Displaying results
    5. Providing operation suggestions

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    enable_ansi_colors()  # Enable ANSI colors

    parser = create_parser()
    args = parser.parse_args()

    # Show value proposition if --intro is used
    if args.intro:
        show_intro()

    # Print friendly welcome message and version
    print("=" * 50)
    print("GitHub Network Status Checker")
    print(f"Version: {VERSION}")
    print("=" * 50)
    # Print check start prompt
    print("Checking GitHub accessibility...", end=" ")

    spinner_thread = None

    # For normal checks, display animation until check completes
    if not args.full_test:
        spinner_thread = start_spinner()

    try:
        chk = Checker()  # Create checker instance
        if args.full_test:
            r = chk.test(timeout=DEFAULT_TIMEOUT)  # Execute full test
            is_full_test = True
        else:
            r = chk.check(timeout=DEFAULT_TIMEOUT)  # Execute normal check
            is_full_test = False

        # Stop animation thread if running
        if not args.full_test and spinner_thread is not None:
            stop_spinner(spinner_thread)

        # Format output based on JSON flag and theme
        if args.json:
            json_output = generate_json_output(r, is_full_test)
            print(json.dumps(json_output, indent=2, ensure_ascii=False))
        else:
            run_with_theme(r, args.theme, is_full_test)

        return 0  # Normal exit

    except KeyboardInterrupt:
        if spinner_thread is not None:
            stop_spinner(spinner_thread)
        print("\n\nInterrupted by user.")
        return 1
    except requests.exceptions.ConnectionError as e:
        if spinner_thread is not None:
            stop_spinner(spinner_thread)
        print("\n\n[ERROR] Network connection failed.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Please check your network connection and try again.")
        return 2
    except requests.exceptions.Timeout as e:
        if spinner_thread is not None:
            stop_spinner(spinner_thread)
        print("\n\n[ERROR] Request timeout.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Network is slow or GitHub is not responding. Try again later.")
        return 3
    except requests.exceptions.RequestException as e:
        if spinner_thread is not None:
            stop_spinner(spinner_thread)
        print("\n\n[ERROR] Request failed.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Check your network settings and try again.")
        return 4
    except Exception as e:
        if spinner_thread is not None:
            stop_spinner(spinner_thread)
        print("\n[ERROR] Unexpected error occurred.")
        print(f"Details: {type(e).__name__}: {str(e)}")
        print("\nSuggestion: Please report this issue with the error message above.")
        return 5


if __name__ == "__main__":
    # Execute main function when script is run directly
    sys.exit(main())
