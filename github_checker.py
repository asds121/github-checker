#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub网络状态检测工具 - 极简版

核心需求（第一性原理分析）：
1. 检测GitHub能否访问
2. 显示检测结果
3. 给用户操作建议

去掉的东西：
- 插件化架构（过度设计）
- 事件总线（不必要的复杂性）
- 多线程（单次请求足够快）
- 数据持久化（大多数用户不需要）
- 复杂配置系统
- 自动检测定时任务
- 完善日志系统
"""

import tkinter as tk
from tkinter import ttk
import requests
import time


class Checker:
    """核心检测逻辑 - 只有70行"""
    
    TARGETS = [
        ("主页", "https://github.com"),
        ("API", "https://api.github.com"),
    ]
    
    def check(self, timeout: float = 8.0) -> dict:
        start = time.time()
        results = []
        
        for name, url in self.TARGETS:
            elapsed = time.time() - start
            remain = max(1.0, timeout - elapsed)
            
            r = self._test(url, remain)
            results.append((name, r))
            
            if name == "主页" and not r["ok"]:
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
            "good": "✅ GitHub访问正常",
            "warn": "⚠️ GitHub访问不稳定",
            "bad": "❌ 无法连接GitHub"
        }
        return msgs.get(status, "❌ 未知状态")


class GUI:
    """极简界面 - 只有60行"""
    
    COLORS = {"good": "#27ae60", "warn": "#f39c12", "bad": "#e74c3c"}
    
    def __init__(self):
        self.chk = Checker()
        self._build()
    
    def _build(self):
        self.root = tk.Tk()
        self.root.title("GitHub状态检测")
        self.root.geometry("360x240")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        self._center()
        
        f = ttk.Frame(self.root, padding=15)
        f.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(f, text="GitHub状态检测",
                 font=("Arial", 13, "bold"),
                 background="#f5f5f5").pack(pady=(0, 10))
        
        self.status = tk.Label(f, text="●", font=("Arial", 45),
                              foreground="#999999", background="#f5f5f5")
        self.status.pack()
        
        self.msg = tk.Label(f, text="点击按钮开始检测",
                           font=("Arial", 10), wraplength=320,
                           background="#f5f5f5")
        self.msg.pack(pady=12)
        
        self.info = tk.Label(f, text="延迟: --",
                           font=("Arial", 9), foreground="#666",
                           background="#f5f5f5")
        self.info.pack()
        
        ttk.Button(f, text="开始检测", command=self._run,
                  width=12).pack(pady=15)
    
    def _center(self):
        self.root.update_idletasks()
        w, h = 360, 240
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")
    
    def _run(self):
        self.status.config(text="...", foreground="#666")
        self.root.update()
        
        try:
            r = self.chk.check(timeout=8.0)
            self.status.config(text="●", foreground=self.COLORS[r["status"]])
            self.msg.config(text=r["msg"])
            
            main = r["results"][0][1] if r["results"] else {}
            if main.get("ok"):
                self.info.config(text=f"延迟: {main['ms']:.0f}ms  |  正常")
            else:
                self.info.config(text="延迟: --  |  失败")
        except Exception as e:
            self.status.config(text="!", foreground="#e74c3c")
            self.msg.config(text=f"错误: {e}")
    
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    GUI().start()
