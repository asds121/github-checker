#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
GitHub Network Status Checker - Minimal CLI Version

Core functions:
1. Check GitHub accessibility
2. Show detection results
3. Provide operation suggestions

Author: GitHub Checker Project
"""

import sys  # System-related parameters and functions, such as exit codes
import time  # Time-related operations, such as timing and delays
import json  # JSON encoding and decoding
import requests  # Used to send HTTP requests
import argparse  # Used to parse command-line arguments
from typing import List, Dict, Tuple, Any, Iterator


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


def format_status(status: str, message: str) -> str:
    """
    Format status message with colors and styling

    Args:
        status (str): Status type ("good", "warn", "bad")
        message (str): Status message

    Returns:
        str: Formatted status message with colors
    """
    if status == "good":
        return colorize(f"[OK] {message}", Colors.GREEN)
    elif status == "warn":
        return colorize(f"[WARN] {message}", Colors.YELLOW)
    elif status == "bad":
        return colorize(f"[FAIL] {message}", Colors.RED)
    else:
        return f"[{status.upper()}] {message}"


# Constants
DEFAULT_TIMEOUT = 8.0  # Default request timeout in seconds
FULL_TEST_ITERATIONS = 3  # Number of iterations for full test
MIN_REMAIN_TIMEOUT = 1.0  # Minimum remaining timeout for subsequent requests
RESPONSE_TIME_THRESHOLD_MS = 3000  # Response time threshold in milliseconds
RESPONSE_TIME_THRESHOLD_SEC = 3.0  # Response time threshold in seconds

# Spinner animation constants
SPINNER_PADDING = 50  # Number of spaces to clear spinner animation
SPINNER_JOIN_TIMEOUT = 0.2  # Timeout for joining spinner thread (seconds)
SPINNER_DELAY = 0.1  # Delay between spinner frames (seconds)
SPINNER_CHARS = '|/\\-'  # Spinner character sequence


class Checker:
    """GitHub accessibility checker

    This class is responsible for performing accessibility checks on GitHub
    website and API, and collecting statistics such as response time and
    success rate
    """

    # Target URLs - includes GitHub homepage and API endpoints
    TARGETS = [
        ("homepage", "https://github.com"),  # GitHub homepage
        ("api", "https://api.github.com"),  # GitHub API
    ]

    def test(self, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """
        Perform full test with multiple checks and calculate average

        Args:
            timeout (float): Request timeout in seconds

        Returns:
            Dict[str, Any]: Dictionary containing test results including:
                - status (str): Overall status ("good", "warn", "bad")
                - msg (str): Status message
                - iterations (int): Number of iterations performed
                - avg_total_time (float): Average total time in milliseconds
                - successful_checks (int): Number of successful checks
                - target_stats (dict): Statistics for each target
                - all_results (list): All test results
        """
        results: List[Dict[str, Any]] = []
        all_results: List[Tuple[str, Dict[str, Any]]] = []

        print(f"Running full test ({FULL_TEST_ITERATIONS} iterations)...")
        for i in range(FULL_TEST_ITERATIONS):
            progress = (i + 1) / FULL_TEST_ITERATIONS * 100
            print(f"  Iteration {i + 1}/{FULL_TEST_ITERATIONS} ({progress:.0f}%)...", end="\r")
            result = self.check(timeout=timeout)
            results.append(result)
            all_results.extend(result["results"])

        # Calculate overall statistics
        successful_checks = sum(1 for r in results if r["status"] != "bad")
        total_time = sum(r["ms"] for r in results)
        avg_time = total_time / len(results) if results else 0

        # Calculate average response times for each target
        target_stats: Dict[str, Dict[str, float]] = {}
        for name, url in self.TARGETS:
            target_results = [r for _, r in all_results if _ == name]
            if target_results:
                avg_response = sum(r.get("ms", 0) for r in target_results
                                   if "ms" in r) / len(target_results)
                successful_responses = sum(1 for r in target_results
                                           if r.get("ok", False))
                target_stats[name] = {
                    "avg_response": avg_response,
                    "success_rate": (successful_responses /
                                     len(target_results) * 100)
                }

        overall_status = self._judge(all_results)

        return {
            "status": overall_status,
            "msg": self._msg(overall_status, all_results),
            "iterations": FULL_TEST_ITERATIONS,
            "avg_total_time": avg_time,
            "successful_checks": successful_checks,
            "target_stats": target_stats,
            "all_results": all_results
        }

    def check(self, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """
        Execute single detection

        Args:
            timeout (float): Request timeout in seconds, default is 8 seconds

        Returns:
            Dict[str, Any]: Dictionary containing detection status, total time,
                  results and message
        """
        start = time.time()  # Record start time
        results: List[Tuple[str, Dict[str, Any]]] = []  # Store detection results

        # Iterate through all targets for detection
        for name, url in self.TARGETS:
            elapsed = time.time() - start  # Calculate elapsed time
            remain = max(MIN_REMAIN_TIMEOUT, timeout - elapsed)  # Remaining time

            r = self._test(url, remain)  # Execute single URL test
            results.append((name, r))  # Add result to list

            # If homepage detection fails, stop subsequent detection
            if name == "homepage" and not r["ok"]:
                break

        total_ms = (time.time() - start) * 1000  # Total time in ms
        status = self._judge(results)  # Judge detection status

        return {
            "status": status,  # Detection status (good/warn/bad)
            "ms": total_ms,  # Total time in milliseconds
            "results": results,  # Detection results list
            "msg": self._msg(status, results)  # Status message
        }

    def _test(self, url: str, timeout: float) -> Dict[str, Any]:
        """
        Test accessibility of a single URL

        Args:
            url (str): URL to test
            timeout (float): Request timeout in seconds

        Returns:
            Dict[str, Any]: Dictionary containing test results, including success status,
                  response time, status code or error message
        """
        try:
            t0 = time.time()  # Record request start time
            # Send GET request to specified URL, set timeout and user agent
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "GitHubChecker/1.0"
            })
            # Return success result: status code 200 means success
            return {
                "ok": resp.status_code == 200,  # Whether successful
                "ms": round((time.time() - t0) * 1000),  # Response time
                "status_code": resp.status_code  # HTTP status code
            }
        except requests.exceptions.Timeout:
            # Request timeout exception
            return {
                "ok": False,
                "error": "Request timed out",
                "error_type": "timeout",
                "suggestion": "Network is slow or server is not responding"
            }
        except requests.exceptions.ConnectionError as e:
            # Connection error exception
            return {
                "ok": False,
                "error": "Connection error - check network",
                "error_type": "connection",
                "suggestion": "Please verify your network connection",
                "details": str(e)
            }
        except requests.exceptions.HTTPError as e:
            # HTTP error exception
            return {
                "ok": False,
                "error": f"HTTP error: {str(e)}",
                "error_type": "http",
                "suggestion": "Server returned an invalid HTTP response"
            }
        except requests.exceptions.TooManyRedirects:
            # Too many redirects exception
            return {
                "ok": False,
                "error": "Too many redirects",
                "error_type": "redirect",
                "suggestion": "URL is redirecting too many times"
            }
        except requests.exceptions.RequestException as e:
            # Other request exceptions
            return {
                "ok": False,
                "error": f"Request error: {str(e)}",
                "error_type": "request",
                "suggestion": "Request failed, please try again"
            }
        except Exception as e:
            # Other unexpected exceptions
            return {
                "ok": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unknown",
                "suggestion": "An unexpected error occurred"
            }

    def _judge(self, results: List[Tuple[str, Dict[str, Any]]]) -> str:
        """
        Judge network status based on detection results

        Args:
            results (List[Tuple[str, Dict[str, Any]]]): Detection results list

        Returns:
            str: Network status ("good", "warn", or "bad")
                 - "good": All targets succeed and avg response < 3 seconds
                 - "warn": Partial success or avg response >= 3 seconds
                 - "bad": All targets fail
        """
        if not results:
            return "bad"  # No results means bad status

        # Calculate number of successful results
        ok = sum(1 for _, r in results if r.get("ok"))
        if ok == 0:
            return "bad"  # No successful results
        if ok < len(results):
            return "warn"  # Partial success

        # Calculate average response time
        avg = sum(r["ms"] for _, r in results) / len(results)
        return "good" if avg < RESPONSE_TIME_THRESHOLD_MS else "warn"

    def _msg(self, status: str, results: List[Tuple[str, Dict[str, Any]]]) -> str:
        """
        Generate user-friendly status message based on detection results

        Args:
            status (str): Network status ("good", "warn", or "bad")
            results (List[Tuple[str, Dict[str, Any]]]): Detection results list

        Returns:
            str: Formatted status message (without status prefix)
        """
        if status == "good":
            successful_results = [r for _, r in results if "ms" in r]
            if successful_results:
                avg_time = sum(r["ms"] for _, r in results
                               if "ms" in r) / len(successful_results)
                return f"GitHub is accessible (avg {avg_time:.0f}ms)"
            else:
                return "GitHub is accessible"
        elif status == "warn":
            failed_targets = [name for name, r in results if not r.get("ok")]
            if failed_targets:
                return (f"GitHub is unstable "
                        f"({', '.join(failed_targets)} affected)")
            else:
                successful_results = [r for _, r in results if "ms" in r]
                if successful_results:
                    avg_time = sum(r["ms"] for _, r in results
                                   if "ms" in r) / len(successful_results)
                    return (f"GitHub is accessible but slow "
                            f"(avg {avg_time:.0f}ms)")
                else:
                    return "GitHub is accessible but slow"
        elif status == "bad":
            failed_targets = [name for name, r in results if not r.get("ok")]
            return (f"Cannot connect to GitHub "
                    f"({', '.join(failed_targets)})")
        else:
            return "Unknown status"


def spinning_cursor() -> Iterator[str]:
    """
    Generator that yields spinning cursor animation

    Yields:
        str: Spinning cursor characters
    """
    while True:
        for cursor in SPINNER_CHARS:  # Spinner character sequence
            yield cursor  # Generate next cursor character


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
    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description="GitHub Network Status Checker")
    # Add full test mode parameter
    parser.add_argument('-f', '--full-test', action='store_true',
                        help='Perform full test with multiple checks')
    # Add JSON output parameter
    parser.add_argument('-j', '--json', action='store_true',
                        help='Output results in JSON format')
    args = parser.parse_args()  # Parse command line arguments

    # Print program title and separator
    print("GitHub Network Status Checker v1.1.0")
    print("=" * 40)
    # Print check start prompt
    print("Checking GitHub accessibility...", end=" ")

    # Start spinning cursor animation
    import threading  # For creating animation thread
    import itertools  # For cycling animation characters

    spinner_thread = None

    # For normal checks, display animation until check completes
    if not args.full_test:
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
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
            print("\r" + " " * SPINNER_PADDING + "\r", end="")

        # Format output based on JSON flag
        if args.json:
            # Output results in JSON format
            json_output = {
                "version": "v1.1.0",
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

            # Generate suggestion based on status
            if r["status"] == "good":
                json_output["suggestion"] = "Network is stable, you can push code normally."
            elif r["status"] == "warn":
                failed_targets = [name for name, result in r.get("results", [])
                                  if not result.get("ok")]
                if failed_targets:
                    msg = f"Network is unstable for {', '.join(failed_targets)}. "
                    json_output["suggestion"] = msg + "Try again later."
                else:
                    json_output["suggestion"] = "Network is slow but accessible."
            else:
                json_output["suggestion"] = "Network connection failed."

            print(json.dumps(json_output, indent=2, ensure_ascii=False))
        else:
            # Output results in human-readable format
            print("\nResults:")  # Print results title
            print("-" * 40)  # Print separator

            if is_full_test:
                # Display full test results
                print(f"Full test completed ({r['iterations']} iterations)")
                print(f"Successful checks: {r['successful_checks']}/{r['iterations']}")
                print(f"Average total time: {r['avg_total_time']:.0f}ms")
                print("\nTarget statistics:")
                for name, stats in r['target_stats'].items():
                    print(f"  {name:10}: Avg {stats['avg_response']:.0f}ms, "
                          f"Success rate: {stats['success_rate']:.1f}%")
            else:
                # Display normal check results
                for name, result in r["results"]:
                    if result.get("ok"):
                        status = "OK"
                        ms = result.get("ms", 0)
                        print(f"  {name:10}: {status:4} ({ms:.0f}ms)")
                    else:
                        status = "FAIL"
                        error_msg = result.get("error", "Unknown error")
                        print(f"  {name:10}: {status:4} ({error_msg})")

            print("-" * 40)
            # Display status with color formatting
            print(f"\nStatus: {format_status(r['status'], r['msg'])}")  # Print status message

            # Provide operation suggestions based on status
            if r["status"] == "good":
                print(f"\nSuggestion: {colorize('Network is stable, you can push code normally.', Colors.GREEN)}")
            elif r["status"] == "warn":
                failed_targets = [name for name, result in r.get("results", [])
                                  if not result.get("ok")]
                if failed_targets:
                    msg = f"Network is unstable for {', '.join(failed_targets)}. "
                    print(f"\nSuggestion: {colorize(msg + 'Try again later.', Colors.YELLOW)}")
                else:
                    print(f"\nSuggestion: {colorize('Network is slow but accessible.', Colors.YELLOW)}")
            else:
                print(f"\nSuggestion: {colorize('Network connection failed.', Colors.RED)}")

        return 0  # Normal exit

    except KeyboardInterrupt:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\n\nInterrupted by user.")
        return 1
    except requests.exceptions.ConnectionError as e:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\n\n[ERROR] Network connection failed.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Please check your network connection and try again.")
        return 2
    except requests.exceptions.Timeout as e:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\n\n[ERROR] Request timeout.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Network is slow or GitHub is not responding. Try again later.")
        return 3
    except requests.exceptions.RequestException as e:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\n\n[ERROR] Request failed.")
        print(f"Details: {str(e)}")
        print("\nSuggestion: Check your network settings and try again.")
        return 4
    except Exception as e:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=SPINNER_JOIN_TIMEOUT)
        print("\n[ERROR] Unexpected error occurred.")
        print(f"Details: {type(e).__name__}: {str(e)}")
        print("\nSuggestion: Please report this issue with the error message above.")
        return 5


if __name__ == "__main__":
    # Execute main function when script is run directly
    sys.exit(main())



