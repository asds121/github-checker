# -*- coding: ascii -*-
"""
UI themes module for GitHub Checker

Provides theme definitions and formatting functions for CLI output.

Author: GitHub Checker Project
"""

import random
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


# Fun status messages for different scenarios
FUN_STATUS_MESSAGES = {
    "good": {
        "super_fast": [
            "GitHub is super fast! Everything is blazing!",
            "Speed demon mode activated! GitHub is lightning quick!",
            "GitHub says: I am speed! Everything checks out!",
        ],
        "normal": [
            "GitHub is happy and responsive!",
            "All systems go! GitHub is working perfectly!",
            "GitHub says: Ready for action! Let's go!",
        ],
        "accessible": [
            "GitHub is accessible and working normally!",
            "Connection established! GitHub is ready!",
            "GitHub is online and waiting for your code!",
        ]
    },
    "warn": {
        "slow_github": [
            "GitHub seems to be taking a nap... zzz",
            "GitHub is moving at a leisurely pace today...",
            "GitHub might be on a coffee break...",
        ],
        "somewhat_slow": [
            "GitHub is a bit slow today...",
            "Things are moving slowly in GitHub land...",
            "GitHub is taking its time today...",
        ]
    },
    "bad": {
        "unreachable": [
            "GitHub appears to be unreachable at the moment",
            "GitHub seems to be on vacation...",
            "GitHub is not answering the door...",
            "GitHub might be hiding from us...",
        ]
    }
}


# Fun status icons for different statuses (ASCII alternative to emojis)
EMOJI_MAP = {
    "good": ["[OK]", "[PASS]", "[YES]", "[GO]", "[FAST]"],
    "warn": ["[WAIT]", "[SLOW]", "[WARN]", "[LATER]"],
    "bad": ["[FAIL]", "[NO]", "[DOWN]", "[STOP]", "[ERROR]"]
}


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
            category = "super_fast"
        elif avg_ms and avg_ms < 1000:
            category = "normal"
        else:
            category = "accessible"
    elif status == "warn":
        if avg_ms and avg_ms > 3000:
            category = "slow_github"
        else:
            category = "somewhat_slow"
    else:
        category = "unreachable"

    messages = FUN_STATUS_MESSAGES.get(status, {}).get(category, ["Status unknown"])
    return random.choice(messages)


def get_emoji(status: str) -> str:
    """
    Get a random emoji for the given status

    Args:
        status (str): Status type ("good", "warn", "bad")

    Returns:
        str: Random emoji
    """
    emojis = EMOJI_MAP.get(status, ["[?]"])
    return random.choice(emojis)


def format_fun_emoji_status(status: str, avg_ms: float = None) -> str:
    """
    Format status message with fun descriptions and emojis

    Args:
        status (str): Status type ("good", "warn", "bad")
        avg_ms (float): Average response time in milliseconds

    Returns:
        str: Fun status description with emoji
    """
    emoji = get_emoji(status)
    message = format_fun_status(status, avg_ms)
    return f"{emoji} {message}"


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

    lines = []
    emoji = get_emoji(r["status"])

    # Fun header
    lines.append("\n" + "=" * 50)
    lines.append(f"{emoji} DETECTION RESULTS {emoji}")
    lines.append("-" * 20)
    lines.append(f"Status: {r['status'].upper()}")

    if is_full_test:
        # Full test details
        lines.append(f"Iterations: {r.get('iterations', 'N/A')}")
        lines.append(f"Successful Checks: {r.get('successful_checks', 'N/A')}")
        lines.append(f"Average Time: {r.get('avg_total_time', 0):.2f}ms")

        # Target statistics
        target_stats = r.get('target_stats', {})
        if target_stats:
            lines.append("\nTarget Statistics:")
            for name, stats in target_stats.items():
                lines.append(f"  {name}:")
                lines.append(f"    Avg: {stats.get('avg_response', 0):.2f}ms")
                lines.append(f"    Success: {stats.get('success_rate', 0)}%")
    else:
        # Normal check results
        results = r.get('results', [])
        if results:
            lines.append("\nTarget Results:")
            for name, result in results:
                if result.get("ok"):
                    ms = result.get("ms", 0)
                    lines.append(f"  [OK] {name}: {ms:.0f}ms")
                else:
                    lines.append(f"  [FAIL] {name}: {result.get('error', 'Unknown error')}")

    # Fun footer
    lines.append("-" * 50)
    lines.append(format_fun_emoji_status(r["status"]))
    lines.append("=" * 50 + "\n")

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
    lines = []

    # Add status line with colors
    status_color = Colors.GREEN if r["status"] == "good" else Colors.YELLOW if r["status"] == "warn" else Colors.RED
    lines.append(colorize(f"\nStatus: {r['status'].upper()}", status_color))
    lines.append(colorize(f"Message: {r['msg']}", Colors.RESET))

    if is_full_test:
        # Full test details
        lines.append(f"\nFull Test Results:")
        lines.append(f"  Iterations: {r.get('iterations', 'N/A')}")
        lines.append(f"  Successful Checks: {r.get('successful_checks', 'N/A')}")
        lines.append(f"  Average Total Time: {r.get('avg_total_time', 0):.2f}ms")

        # Target statistics
        target_stats = r.get('target_stats', {})
        if target_stats:
            lines.append(f"\nTarget Statistics:")
            for name, stats in target_stats.items():
                lines.append(f"  {name}:")
                lines.append(f"    Average Response: {stats.get('avg_response', 0):.2f}ms")
                lines.append(f"    Success Rate: {stats.get('success_rate', 0)}%")
    else:
        # Normal check results
        results = r.get('results', [])
        if results:
            lines.append(f"\nDetailed Results:")
            for name, result in results:
                if result.get("ok"):
                    ms = result.get("ms", 0)
                    lines.append(f"  {name}: OK ({ms:.0f}ms)")
                else:
                    lines.append(f"  {name}: FAIL - {result.get('error', 'Unknown error')}")

    return "\n".join(lines)


def render_share_theme(r: Dict[str, Any], is_full_test: bool = False) -> str:
    """
    Render output using share theme (concise output for sharing)

    Args:
        r: Result dictionary containing test results
        is_full_test: Whether this is a full test result

    Returns:
        str: Formatted output string
    """
    lines = []

    # Header
    lines.append("GitHub Status Report")
    lines.append("-" * 30)

    # Overall status
    status_symbol = "[OK]" if r["status"] == "good" else "[WARN]" if r["status"] == "warn" else "[FAIL]"
    lines.append(f"{status_symbol} {r['status'].upper()}")

    if is_full_test:
        # Full test summary
        lines.append(f"Iterations: {r.get('iterations', 'N/A')}")
        lines.append(f"Success Rate: {r.get('successful_checks', 'N/A')}/{r.get('iterations', 'N/A')}")
        lines.append(f"Avg Time: {r.get('avg_total_time', 0):.0f}ms")
    else:
        # Normal check summary
        results = r.get('results', [])
        ok_count = sum(1 for _, result in results if result.get("ok"))
        total_count = len(results)
        lines.append(f"Results: {ok_count}/{total_count} OK")

    return "\n".join(lines)


def generate_share_text(r: Dict[str, Any], theme: str = "default") -> str:
    """
    Generate shareable text from test results

    Args:
        r: Result dictionary containing test results
        theme: Theme to use for rendering

    Returns:
        str: Shareable text
    """
    is_full_test = "iterations" in r

    if theme == "fun":
        return render_fun_theme(r, is_full_test)
    elif theme == "minimal":
        return render_minimal_theme(r)
    elif theme == "share":
        return render_share_theme(r, is_full_test)
    else:
        return render_default_theme(r, is_full_test)
