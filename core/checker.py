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
    RESPONSE_TIME_THRESHOLD_MS,
    FULL_TEST_ITERATIONS
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
            # Send GET request to specified URL, set timeout and user agent
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "GitHubChecker/1.0"
            })
            # Return success result: status code 200 means success
            return {
                "ok": resp.status_code == 200,  # Whether successful
                "ms": round(resp.elapsed.total_seconds() * 1000),  # Response time in ms
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
                "error": f"HTTP error: {e}",
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
                "error": f"Request error: {e}",
                "error_type": "request",
                "suggestion": "An unexpected error occurred"
            }
        except Exception as e:
            # Generic exceptions (non-request related)
            return {
                "ok": False,
                "error": f"Unexpected error: {e}",
                "error_type": "generic",
                "suggestion": "An unexpected error occurred"
            }

    def _judge(self, results: List[Tuple[str, Dict[str, Any]]]) -> str:
        """
        Judge the overall status based on detection results

        Args:
            results (list): List of detection results

        Returns:
            str: Overall status ("good", "warn", or "bad")
        """
        if not results:
            return "bad"

        # If any result is not ok, return bad status
        if any(not r["ok"] for _, r in results):
            return "bad"

        # If all results are ok, check response time
        avg_response_time = sum(r.get("ms", 0) for _, r in results) / len(results)

        if avg_response_time > RESPONSE_TIME_THRESHOLD_MS:
            return "warn"

        return "good"

    def _msg(self, status: str, results: List[Tuple[str, Dict[str, Any]]]) -> str:
        """
        Generate status message based on status and results

        Args:
            status (str): Overall status
            results (list): List of detection results

        Returns:
            str: Status message
        """
        if status == "good":
            return "All targets accessible"

        if status == "warn":
            return "Accessible but slow response"

        # status == "bad"
        failed = [name for name, r in results if not r["ok"]]
        if failed:
            return f"Failed targets: {', '.join(failed)}"

        return "Detection failed"
