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

import sys
import time
import requests


class Checker:
    """Core detection logic"""
    
    TARGETS = [
        ("homepage", "https://github.com"),
        ("api", "https://api.github.com"),
    ]
    
    def check(self, timeout: float = 8.0) -> dict:
        start = time.time()
        results = []
        
        for name, url in self.TARGETS:
            elapsed = time.time() - start
            remain = max(1.0, timeout - elapsed)
            
            r = self._test(url, remain)
            results.append((name, r))
            
            if name == "homepage" and not r["ok"]:
                break
        
        total_ms = (time.time() - start) * 1000
        status = self._judge(results)
        
        return {
            "status": status,
            "ms": total_ms,
            "results": results,
            "msg": self._msg(status, results)
        }
    
    def _test(self, url: str, timeout: float) -> dict:
        try:
            t0 = time.time()
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "GitHubChecker/1.0"
            })
            return {
                "ok": resp.status_code == 200,
                "ms": round((time.time() - t0) * 1000)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _judge(self, results: list) -> str:
        if not results:
            return "bad"
        
        ok = sum(1 for _, r in results if r.get("ok"))
        if ok == 0:
            return "bad"
        if ok < len(results):
            return "warn"
        
        avg = sum(r["ms"] for _, r in results) / len(results)
        return "good" if avg < 300 else "warn"
    
    def _msg(self, status: str, results: list) -> str:
        msgs = {
            "good": "[OK] GitHub is accessible",
            "warn": "[WARN] GitHub is unstable",
            "bad": "[FAIL] Cannot connect to GitHub"
        }
        return msgs.get(status, "[FAIL] Unknown status")


def spinning_cursor():
    """Generator for spinning cursor animation"""
    while True:
        for cursor in '|/-\\':
            yield cursor


def main():
    """Main function"""
    print("GitHub Network Status Checker v1.0")
    print("=" * 40)
    print("Checking GitHub accessibility...")
    
    spinner = spinning_cursor()
    
    try:
        chk = Checker()
        r = chk.check(timeout=8.0)
        
        print("\r" + " " * 50 + "\r", end="")
        
        print("\nResults:")
        print("-" * 40)
        
        for name, result in r["results"]:
            status = "OK" if result.get("ok") else "FAIL"
            ms = result.get("ms", 0)
            print(f"  {name:10}: {status:4} ({ms:.0f}ms)")
        
        print("-" * 40)
        print(f"\nStatus: {r['msg']}")
        
        if r["status"] == "good":
            print("\nSuggestion: You can push code normally.")
        elif r["status"] == "warn":
            print("\nSuggestion: Try again later, or use proxy.")
        else:
            print("\nSuggestion: Check network connection or VPN.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
