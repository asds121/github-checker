# -*- coding: ascii -*-
"""
UI themes module for GitHub Checker

Provides theme definitions and formatting functions for CLI output.

Author: GitHub Checker Project
"""

from typing import Dict, Any

from core.colors import Colors, colorize


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


def format_fun_status(status: str, avg_ms: float = None) -> str:
    """
    Format status message with fun descriptions

    Args:
        status (str): Status type ("good", "warn", "bad")
        avg_ms (float): Average response time in milliseconds

    Returns:
        str: Fun status description
    """
    if status == "good":
        if avg_ms and avg_ms < 500:
            return "GitHub is super fast! Everything is blazing!"
        elif avg_ms and avg_ms < 1000:
            return "GitHub is happy and responsive!"
        else:
            return "GitHub is accessible and working normally!"
    elif status == "warn":
        if avg_ms and avg_ms > 3000:
            return "GitHub seems to be taking a nap... zzz"
        else:
            return "GitHub is a bit slow today..."
    else:
        return "GitHub appears to be unreachable at the moment"


def render_minimal_theme(r: Dict[str, Any], results_key: str = "results") -> str:
    """
    Render output using minimal theme

    Args:
        r: Result dictionary containing test results
        results_key: Key to access results list (for full test vs normal test)

    Returns:
        str: Formatted output string
    """
    lines = []
    results = r.get(results_key, r.get("results", []))

    for name, result in results:
        if result.get("ok"):
            status = "OK"
            ms = result.get("ms", 0)
            lines.append(f"{name}: {status} ({ms:.0f}ms)")
        else:
            lines.append(f"{name}: FAIL")

    # Add status line
    if r["status"] == "good":
        lines.append(f"STATUS: OK ({r['msg']})")
    elif r["status"] == "warn":
        lines.append(f"STATUS: WARN ({r['msg']})")
    else:
        lines.append(f"STATUS: FAIL ({r['msg']})")

    return "\n".join(lines)


def render_fun_theme(r: Dict[str, Any], is_full_test: bool = False) -> str:
    """
    Render output using fun theme

    Args:
        r: Result dictionary containing test results
        is_full_test: Whether this is a full test result

    Returns:
        str: Formatted output string
    """
    import time

    lines = []
    lines.append("\n" + "=" * 50)
    lines.append("DETECTION RESULTS")
    lines.append("-" * 20)

    for name, result in r["results"]:
        if result.get("ok"):
            status = "OK"
            ms = result.get("ms", 0)
            lines.append(f"  {name:10}: {status:4} ({ms:.0f}ms)")
        else:
            status = "FAIL"
            lines.append(f"  {name:10}: {status:4}")

    lines.append("\n" + "=" * 50)

    # Fun status messages
    avg_ms = r.get("avg_total_time", 0) if is_full_test else None
    fun_status = format_fun_status(r["status"], avg_ms)
    lines.append(f"STATUS: {fun_status}")

    lines.append("\n" + "=" * 50)
    lines.append("SUGGESTION")

    if r["status"] == "good":
        lines.append("  You can push code now! Go for it!")
        lines.append("  Everything is working great!")
    elif r["status"] == "warn":
        failed_targets = [name for name, result in r.get("results", [])
                          if not result.get("ok")]
        if failed_targets:
            lines.append("  GitHub is having some trouble...")
            failed_list = ', '.join(failed_targets)
            lines.append(f"  Slow spot: {failed_list}")
            lines.append("  Maybe wait a bit and try again?")
        else:
            lines.append("  Things are a bit slow today...")
            lines.append("  But you can still get work done!")
    else:
        lines.append("  GitHub seems to be taking a break...")
        lines.append("  Check your network connection first.")

    lines.append("\n" + "=" * 50)
    lines.append("SHARE THIS RESULT")
    lines.append(f"GitHub Checker v1.1.0 | {r['msg']} | {time.strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)


def render_default_theme(r: Dict[str, Any], is_full_test: bool = False) -> str:
    """
    Render output using default theme

    Args:
        r: Result dictionary containing test results
        is_full_test: Whether this is a full test result

    Returns:
        str: Formatted output string
    """
    import time

    lines = []

    if is_full_test:
        # Full test output format
        lines.append("\nResults:")
        lines.append("-" * 40)
        lines.append(f"Full test completed ({r['iterations']} iterations)")
        lines.append(f"Successful checks: {r['successful_checks']}/{r['iterations']}")
        lines.append(f"Average total time: {r['avg_total_time']:.0f}ms")
        lines.append("\nTarget statistics:")
        for name, stats in r['target_stats'].items():
            lines.append(f"  {name:10}: Avg {stats['avg_response']:.0f}ms, "
                        f"Success rate: {stats['success_rate']:.1f}%")

        lines.append("\n" + "=" * 50)
        lines.append(f"STATUS: {format_status(r['status'], r['msg'])}")

        lines.append("\n" + "=" * 50)
        lines.append("SUGGESTION")

        if r["status"] == "good":
            lines.append(f"  {colorize('Network is stable.', Colors.GREEN)}")
            lines.append(f"  {colorize('You can push code normally.', Colors.GREEN)}")
        elif r["status"] == "warn":
            failed_targets = [name for name, result in r.get("results", [])
                              if not result.get("ok")]
            if failed_targets:
                lines.append(f"  {colorize('Network is unstable.', Colors.YELLOW)}")
                failed_list = ', '.join(failed_targets)
                lines.append(f"  {colorize(f'Issues with: {failed_list}', Colors.YELLOW)}")
                lines.append(f"  {colorize('Try again later.', Colors.YELLOW)}")
            else:
                lines.append(f"  {colorize('Network is slow but accessible.', Colors.YELLOW)}")
                lines.append(f"  {colorize('Consider waiting for better connectivity.', Colors.YELLOW)}")
        else:
            lines.append(f"  {colorize('Network connection failed.', Colors.RED)}")
            lines.append(f"  {colorize('Check your network settings.', Colors.RED)}")

        lines.append("\n" + "=" * 50)
        lines.append("SHARE THIS RESULT")
        lines.append(f"GitHub Checker v1.1.0 | {r['msg']} | {time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # Normal test output format
        lines.append("\n" + "=" * 50)
        lines.append("DETECTION RESULTS")
        lines.append("-" * 20)

        for name, result in r["results"]:
            if result.get("ok"):
                status = "OK"
                ms = result.get("ms", 0)
                lines.append(f"  {name:10}: {status:4} ({ms:.0f}ms)")
            else:
                status = "FAIL"
                error_msg = result.get("error", "Unknown error")
                lines.append(f"  {name:10}: {status:4} ({error_msg})")

        lines.append("\n" + "=" * 50)
        lines.append(f"STATUS: {format_status(r['status'], r['msg'])}")

        lines.append("\n" + "=" * 50)
        lines.append("SUGGESTION")

        if r["status"] == "good":
            lines.append(f"  {colorize('Network is stable.', Colors.GREEN)}")
            lines.append(f"  {colorize('You can push code normally.', Colors.GREEN)}")
        elif r["status"] == "warn":
            failed_targets = [name for name, result in r.get("results", [])
                              if not result.get("ok")]
            if failed_targets:
                lines.append(f"  {colorize('Network is unstable.', Colors.YELLOW)}")
                failed_list = ', '.join(failed_targets)
                lines.append(f"  {colorize(f'Issues with: {failed_list}', Colors.YELLOW)}")
                lines.append(f"  {colorize('Try again later.', Colors.YELLOW)}")
            else:
                lines.append(f"  {colorize('Network is slow but accessible.', Colors.YELLOW)}")
                lines.append(f"  {colorize('Consider waiting for better connectivity.', Colors.YELLOW)}")
        else:
            lines.append(f"  {colorize('Network connection failed.', Colors.RED)}")
            lines.append(f"  {colorize('Check your network settings.', Colors.RED)}")

        lines.append("\n" + "=" * 50)
        lines.append("SHARE THIS RESULT")
        lines.append(f"GitHub Checker v1.1.0 | {r['msg']} | {time.strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)
