# -*- coding: utf-8 -*-
# GitHub Access Checker - AiPy Version
# Function: Real-time detection of github.com accessibility
import tkinter as tk
from tkinter import ttk
import requests
import threading
import time
from datetime import datetime
class GitHubChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Access Checker")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="GitHub Status Checker", 
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.pack(pady=(0, 15))
        
        # Status display area
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to check...",
            font=("Arial", 11),
            fg="#666"
        )
        self.status_label.pack(pady=5)
        
        # Response time
        self.speed_label = tk.Label(
            status_frame,
            text="Response: -- ms",
            font=("Arial", 9),
            fg="#888"
        )
        self.speed_label.pack(pady=2)
        
        # Last check time
        self.time_label = tk.Label(
            status_frame,
            text="Last Check: --:--:--",
            font=("Arial", 8),
            fg="#999"
        )
        self.time_label.pack(pady=2)
        
        # Button area
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        self.check_button = tk.Button(
            button_frame,
            text="Check Now",
            command=self.start_check,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_button = tk.Button(
            button_frame,
            text="Auto: OFF",
            command=self.toggle_auto,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        self.indicator = tk.Label(
            main_frame,
            text="●",
            font=("Arial", 30),
            fg="#999"
        )
        self.indicator.pack(pady=10)
        
        # Variables
        self.auto_checking = False
        self.check_thread = None
        
    def set_status(self, state):
        """Set status color and text"""
        if state == "ready":
            self.indicator.config(fg="#999")
            self.status_label.config(text="Ready", fg="#666")
        elif state == "checking":
            self.indicator.config(fg="#FFA500")
            self.status_label.config(text="Checking...", fg="#FFA500")
        elif state == "success":
            self.indicator.config(fg="#4CAF50")
            self.status_label.config(text="Accessible", fg="#4CAF50")
        elif state == "failed":
            self.indicator.config(fg="#F44336")
            self.status_label.config(text="Failed", fg="#F44336")
    
    def check_github(self):
        """Check GitHub access"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'Referer': 'https://github.com/'
            }
            
            start_time = time.time()
            response = requests.get(
                'https://github.com',
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            end_time = time.time()
            
            response_time = int((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                return True, response_time
            else:
                return False, response.status_code
                
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection Error"
        except Exception as e:
            return False, str(e)
    
    def update_ui(self, success, result):
        """Update UI"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Last Check: {current_time}")
        
        if success:
            self.set_status("success")
            self.speed_label.config(text=f"Response: {result} ms", fg="#4CAF50")
        else:
            self.set_status("failed")
            self.speed_label.config(text=f"Result: {result}", fg="#F44336")
    
    def do_check(self):
        """Execute check in thread"""
        self.set_status("checking")
        self.check_button.config(state=tk.DISABLED)
        
        try:
            success, result = self.check_github()
            self.update_ui(success, result)
        finally:
            self.check_button.config(state=tk.NORMAL)
    
    def start_check(self):
        """Start checking"""
        if self.check_thread and self.check_thread.is_alive():
            return
        
        self.check_thread = threading.Thread(target=self.do_check, daemon=True)
        self.check_thread.start()
    
    def auto_check_loop(self):
        """Auto check loop"""
        while self.auto_checking:
            self.do_check()
            for _ in range(50):
                if not self.auto_checking:
                    break
                time.sleep(0.1)
    
    def toggle_auto(self):
        """Toggle auto check"""
        if not self.auto_checking:
            self.auto_checking = True
            self.auto_button.config(text="Auto: ON", bg="#E91E63")
            self.check_button.config(state=tk.DISABLED)
            auto_thread = threading.Thread(target=self.auto_check_loop, daemon=True)
            auto_thread.start()
        else:
            self.auto_checking = False
            self.auto_button.config(text="Auto: OFF", bg="#2196F3")
            self.check_button.config(state=tk.NORMAL)
            self.set_status("ready")
def main():
    root = tk.Tk()
    app = GitHubChecker(root)
    
    footer = tk.Label(
        root,
        text="Generated by AiPy - Local Check Only",
        font=("Arial", 8),
        fg="#999"
    )
    footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    root.mainloop()
if __name__ == "__main__":
    main()