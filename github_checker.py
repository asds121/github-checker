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
import requests  # Used to send HTTP requests
import argparse  # Used to parse command-line arguments


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

    def test(self, timeout: float = 8.0) -> dict:
        """
        Perform full test with multiple checks and calculate average
        """
        results = []
        all_results = []

        print("Running full test (3 iterations)...")
        for i in range(3):
            print(f"  Iteration {i+1}/3...", end="\r")
            result = self.check(timeout=timeout)
            results.append(result)
            all_results.extend(result["results"])

        # Calculate overall statistics
        successful_checks = sum(1 for r in results if r["status"] != "bad")
        total_time = sum(r["ms"] for r in results)
        avg_time = total_time / len(results) if results else 0

        # Calculate average response times for each target
        target_stats = {}
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
            "iterations": 3,
            "avg_total_time": avg_time,
            "successful_checks": successful_checks,
            "target_stats": target_stats,
            "all_results": all_results
        }

    def check(self, timeout: float = 8.0) -> dict:
        """
        Execute single detection

        Args:
            timeout (float): Request timeout in seconds, default is 8 seconds

        Returns:
            dict: Dictionary containing detection status, total time,
                  results and message
        """
        start = time.time()  # Record start time
        results = []  # Store detection results

        # Iterate through all targets for detection
        for name, url in self.TARGETS:
            elapsed = time.time() - start  # Calculate elapsed time
            remain = max(1.0, timeout - elapsed)  # Remaining time

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

    def _test(self, url: str, timeout: float) -> dict:
        """
        Test accessibility of a single URL

        Args:
            url (str): URL to test
            timeout (float): Request timeout in seconds

        Returns:
            dict: Dictionary containing test results, including success status,
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
            return {"ok": False, "error": "Request timed out",
                    "error_type": "timeout"}
        except requests.exceptions.ConnectionError:
            # Connection error exception
            return {"ok": False, "error": "Connection error - check network",
                    "error_type": "connection"}
        except requests.exceptions.RequestException as e:
            # Other request exceptions
            return {"ok": False, "error": f"Request error: {str(e)}",
                    "error_type": "request"}
        except Exception as e:
            # Other unexpected exceptions
            return {"ok": False, "error": f"Unexpected error: {str(e)}",
                    "error_type": "unknown"}

    def _judge(self, results: list) -> str:
        """
        Judge network status based on detection results

        Args:
            results (list): Detection results list

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
        return "good" if avg < 3000 else "warn"

    def _msg(self, status: str, results: list) -> str:
        """
        Generate user-friendly status message based on detection results

        Args:
            status (str): Network status ("good", "warn", or "bad")
            results (list): Detection results list

        Returns:
            str: Formatted status message
        """
        if status == "good":
            successful_results = [r for _, r in results if "ms" in r]
            if successful_results:
                avg_time = sum(r["ms"] for _, r in results
                               if "ms" in r) / len(successful_results)
                return f"[OK] GitHub is accessible (avg {avg_time:.0f}ms)"
            else:
                return "[OK] GitHub is accessible"
        elif status == "warn":
            failed_targets = [name for name, r in results if not r.get("ok")]
            if failed_targets:
                return (f"[WARN] GitHub is unstable "
                        f"({', '.join(failed_targets)} affected)")
            else:
                successful_results = [r for _, r in results if "ms" in r]
                if successful_results:
                    avg_time = sum(r["ms"] for _, r in results
                                   if "ms" in r) / len(successful_results)
                    return (f"[WARN] GitHub is accessible but slow "
                            f"(avg {avg_time:.0f}ms)")
                else:
                    return "[WARN] GitHub is accessible but slow"
        elif status == "bad":
            failed_targets = [name for name, r in results if not r.get("ok")]
            return (f"[FAIL] Cannot connect to GitHub "
                    f"({', '.join(failed_targets)})")
        else:
            return "[FAIL] Unknown status"


def spinning_cursor():
    """
    Generator that yields spinning cursor animation

    Yields:
        str: Spinning cursor characters (|, /, -, \\)
    """
    while True:
        for cursor in '|/-\\':  # Spinning cursor characters sequence
            yield cursor  # Generate next cursor character


def main():
    """
    Main function: Execute GitHub accessibility check main logic

    This function is responsible for:
    1. Parsing command line arguments
    2. Starting animation indicator
    3. Executing checks
    4. Displaying results
    5. Providing operation suggestions
    """
    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description="GitHub Network Status Checker")
    # Add full test mode parameter
    parser.add_argument('-n', '--full-test', action='store_true',
                        help='Perform full test with multiple checks')
    args = parser.parse_args()  # Parse command line arguments

    # Print program title and separator
    print("GitHub Network Status Checker v1.0")
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
            for cursor in itertools.cycle('|/-\\'):
                if hasattr(show_spinner, 'done'):
                    break
                sys.stdout.write('\b' + cursor)
                sys.stdout.flush()
                time.sleep(0.1)

        spinner_thread = threading.Thread(target=show_spinner)
        spinner_thread.daemon = True
        spinner_thread.start()

    try:
        chk = Checker()  # Create checker instance
        if args.full_test:
            r = chk.test(timeout=8.0)  # Execute full test
            is_full_test = True
        else:
            r = chk.check(timeout=8.0)  # Execute normal check
            is_full_test = False

        # Stop animation thread if running
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=0.2)
            print("\r" + " " * 50 + "\r", end="")

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
        print(f"\nStatus: {r['msg']}")  # Print status message

        # Provide operation suggestions based on status
        if r["status"] == "good":
            print("\nSuggestion: Network is stable, you can push code normally.")
        elif r["status"] == "warn":
            failed_targets = [name for name, result in r.get("results", [])
                              if not result.get("ok")]
            if failed_targets:
                print(f"\nSuggestion: Network is unstable for "
                      f"{', '.join(failed_targets)}. Try again later.")
            else:
                print("\nSuggestion: Network is slow but accessible.")
        else:
            print("\nSuggestion: Network connection failed.")

        return 0  # Normal exit

    except KeyboardInterrupt:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=0.2)
        print("\n\nInterrupted by user.")
        return 1
    except Exception as e:
        if not args.full_test and spinner_thread is not None:
            show_spinner.done = True
            spinner_thread.join(timeout=0.2)
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    # Execute main function when script is run directly
    sys.exit(main())

