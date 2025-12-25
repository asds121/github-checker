# -*- coding: ascii -*-
"""
Checker module for GitHub Checker

Provides the main GitHub accessibility checking functionality.

Author: GitHub Checker Project
"""

from typing import List, Dict, Any, Tuple

import requests
import time

from utils.constants import (
    DEFAULT_TIMEOUT,
    MIN_REMAIN_TIMEOUT,
    RESPONSE_TIME_THRESHOLD_MS
)


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
        from utils.constants import FULL_TEST_ITERATIONS

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
