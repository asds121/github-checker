# -*- coding: utf-8 -*-
# GitHub Access Checker - Enhanced Version
# Function: Real-time detection of github.com accessibility with enhanced features
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
import time
import json
import os
import logging
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

class ConfigManager:
    """Configuration manager for the application"""
    DEFAULT_CONFIG = {
        "timeout": 10,
        "auto_check_interval": 5,
        "max_retries": 3,
        "log_level": "INFO",
        "window_geometry": "500x400",
        "check_urls": ["https://github.com", "https://api.github.com"],
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
        ]
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            else:
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
            return False

class LoggerManager:
    """Enhanced logging manager"""
    def __init__(self, log_file: str = "github_checker.log", log_level: str = "INFO"):
        self.log_file = log_file
        self.setup_logging(log_level)
    
    def setup_logging(self, log_level: str):
        """Setup logging configuration"""
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        logging.basicConfig(
            level=level,
            handlers=[file_handler, console_handler],
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

class GitHubChecker:
    """Enhanced GitHub access checker with improved features"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.logger_manager = LoggerManager(log_level=self.config_manager.config["log_level"])
        
        # Setup main window
        self.setup_window()
        
        # State variables
        self.auto_checking = False
        self.check_thread = None
        self.stats = {"total_checks": 0, "successful_checks": 0, "failed_checks": 0}
        
        # Create UI
        self.create_ui()
        
        self.logger.info("GitHub Checker initialized")
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("GitHub Access Checker - Enhanced")
        self.root.geometry(self.config_manager.config["window_geometry"])
        self.root.resizable(True, True)
        self.root.minsize(400, 300)
        
        # Set window icon (if exists)
        try:
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def create_ui(self):
        """Create enhanced user interface"""
        # Create menu bar
        self.create_menu_bar()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title section
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="GitHub Access Checker",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Enhanced Version with Logging & Statistics",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        # Status indicator
        self.status_label = tk.Label(
            status_frame,
            text="Ready to check...",
            font=("Arial", 12, "bold"),
            fg="#95a5a6"
        )
        self.status_label.pack()
        
        # Response time
        self.response_label = tk.Label(
            status_frame,
            text="Response Time: --",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.response_label.pack()
        
        # Last check time
        self.time_label = tk.Label(
            status_frame,
            text="Last Check: Never",
            font=("Arial", 9),
            fg="#bdc3c7"
        )
        self.time_label.pack()
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.check_button = tk.Button(
            control_frame,
            text="Check Now",
            command=self.start_check,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            activebackground="#229954"
        )
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_button = tk.Button(
            control_frame,
            text="Auto Check: OFF",
            command=self.toggle_auto,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            activebackground="#2980b9"
        )
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        # Statistics section
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill=tk.X)
        
        self.total_label = tk.Label(stats_inner, text="Total Checks: 0", font=("Arial", 9))
        self.total_label.pack(side=tk.LEFT, padx=5)
        
        self.success_label = tk.Label(stats_inner, text="Successful: 0", font=("Arial", 9), fg="#27ae60")
        self.success_label.pack(side=tk.LEFT, padx=5)
        
        self.failed_label = tk.Label(stats_inner, text="Failed: 0", font=("Arial", 9), fg="#e74c3c")
        self.failed_label.pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        self.indicator = tk.Label(
            main_frame,
            text="●",
            font=("Arial", 40),
            fg="#95a5a6"
        )
        self.indicator.pack(pady=5)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Recent Logs", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=6,
            font=("Consolas", 8),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=100
        )
        self.progress.pack(fill=tk.X, pady=5)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Logs", command=self.export_logs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        tools_menu.add_command(label="Clear Statistics", command=self.clear_stats)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="View Full Logs", command=self.view_logs)
    
    def log_to_ui(self, message: str, level: str = "INFO"):
        """Add log message to UI log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_colors = {
            "INFO": "#3498db",
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c",
            "SUCCESS": "#27ae60"
        }
        color = level_colors.get(level, "#ecf0f1")
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", level)
        self.log_text.tag_config(level, foreground=color)
        self.log_text.see(tk.END)
        
        # Keep only last 100 lines
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 100:
            self.log_text.delete('1.0', f'{lines-100}.0')
    
    def update_statistics(self):
        """Update statistics display"""
        self.total_label.config(text=f"Total Checks: {self.stats['total_checks']}")
        self.success_label.config(text=f"Successful: {self.stats['successful_checks']}")
        self.failed_label.config(text=f"Failed: {self.stats['failed_checks']}")
    
    def set_status(self, state: str, message: Optional[str] = None):
        """Set status with enhanced display"""
        status_config = {
            "ready": ("#95a5a6", "Ready to check...", "INFO"),
            "checking": ("#f39c12", "Checking GitHub access...", "INFO"),
            "success": ("#27ae60", "GitHub is accessible", "SUCCESS"),
            "failed": ("#e74c3c", "GitHub access failed", "ERROR")
        }
        
        if state in status_config:
            color, default_msg, log_level = status_config[state]
            display_msg = message or default_msg
            
            self.indicator.config(fg=color)
            self.status_label.config(text=display_msg, fg=color)
            self.log_to_ui(display_msg, log_level)
    
    def check_github(self) -> Tuple[bool, Any]:
        """Enhanced GitHub access check with multiple URLs and retries"""
        urls = self.config_manager.config["check_urls"]
        timeout = self.config_manager.config["timeout"]
        max_retries = self.config_manager.config["max_retries"]
        
        self.stats["total_checks"] += 1
        
        for url in urls:
            for retry in range(max_retries):
                try:
                    self.log_to_ui(f"Checking {url} (attempt {retry + 1}/{max_retries})")
                    
                    headers = {
                        'User-Agent': self.config_manager.config["user_agents"][0],
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                        'Referer': 'https://github.com/'
                    }
                    
                    start_time = time.time()
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=timeout,
                        allow_redirects=True
                    )
                    end_time = time.time()
                    
                    response_time = int((end_time - start_time) * 1000)
                    
                    if response.status_code == 200:
                        self.stats["successful_checks"] += 1
                        self.update_statistics()
                        return True, response_time
                    else:
                        self.log_to_ui(f"HTTP {response.status_code} from {url}", "WARNING")
                        
                except requests.exceptions.Timeout:
                    self.log_to_ui(f"Timeout checking {url}", "WARNING")
                except requests.exceptions.ConnectionError:
                    self.log_to_ui(f"Connection error for {url}", "WARNING")
                except Exception as e:
                    self.log_to_ui(f"Error checking {url}: {str(e)}", "ERROR")
                
                if retry < max_retries - 1:
                    time.sleep(1)  # Brief pause between retries
        
        self.stats["failed_checks"] += 1
        self.update_statistics()
        return False, "All URLs failed"
    
    def update_ui(self, success: bool, result: Any):
        """Update UI with check results"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Last Check: {current_time}")
        
        if success:
            self.set_status("success", f"GitHub is accessible ({result}ms)")
            self.response_label.config(text=f"Response Time: {result}ms", fg="#27ae60")
        else:
            self.set_status("failed", f"Access failed: {result}")
            self.response_label.config(text=f"Status: {result}", fg="#e74c3c")
    
    def do_check(self):
        """Execute check in background thread"""
        self.progress.start()
        self.set_status("checking")
        self.check_button.config(state=tk.DISABLED)
        
        try:
            success, result = self.check_github()
            self.update_ui(success, result)
        except Exception as e:
            self.logger.error(f"Check failed: {e}")
            self.set_status("failed", f"Check error: {str(e)}")
        finally:
            self.progress.stop()
            self.check_button.config(state=tk.NORMAL)
    
    def start_check(self):
        """Start manual check"""
        if self.check_thread and self.check_thread.is_alive():
            self.log_to_ui("Check already in progress", "WARNING")
            return
        
        self.check_thread = threading.Thread(target=self.do_check, daemon=True)
        self.check_thread.start()
    
    def auto_check_loop(self):
        """Auto check loop with configurable interval"""
        interval = self.config_manager.config["auto_check_interval"]
        
        while self.auto_checking:
            self.do_check()
            
            # Wait for interval, checking if auto mode is still active
            for _ in range(interval * 10):  # Check every 0.1 seconds
                if not self.auto_checking:
                    break
                time.sleep(0.1)
    
    def toggle_auto(self):
        """Toggle auto check mode"""
        if not self.auto_checking:
            self.auto_checking = True
            self.auto_button.config(text="Auto Check: ON", bg="#e74c3c")
            self.check_button.config(state=tk.DISABLED)
            self.log_to_ui("Auto check mode enabled", "INFO")
            
            auto_thread = threading.Thread(target=self.auto_check_loop, daemon=True)
            auto_thread.start()
        else:
            self.auto_checking = False
            self.auto_button.config(text="Auto Check: OFF", bg="#3498db")
            self.check_button.config(state=tk.NORMAL)
            self.set_status("ready")
            self.log_to_ui("Auto check mode disabled", "INFO")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(self.logger_manager.log_file, 'r', encoding='utf-8') as source:
                    with open(filename, 'w', encoding='utf-8') as target:
                        target.write(source.read())
                
                messagebox.showinfo("Export Complete", f"Logs exported to {filename}")
                self.log_to_ui(f"Logs exported to {filename}", "SUCCESS")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export logs: {str(e)}")
            self.log_to_ui(f"Log export failed: {str(e)}", "ERROR")
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings form
        form_frame = ttk.Frame(settings_window, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timeout setting
        ttk.Label(form_frame, text="Timeout (seconds):").grid(row=0, column=0, sticky="w", pady=5)
        timeout_var = tk.StringVar(value=str(self.config_manager.config["timeout"]))
        ttk.Entry(form_frame, textvariable=timeout_var, width=10).grid(row=0, column=1, pady=5)
        
        # Auto check interval
        ttk.Label(form_frame, text="Auto Check Interval (seconds):").grid(row=1, column=0, sticky="w", pady=5)
        interval_var = tk.StringVar(value=str(self.config_manager.config["auto_check_interval"]))
        ttk.Entry(form_frame, textvariable=interval_var, width=10).grid(row=1, column=1, pady=5)
        
        # Max retries
        ttk.Label(form_frame, text="Max Retries:").grid(row=2, column=0, sticky="w", pady=5)
        retries_var = tk.StringVar(value=str(self.config_manager.config["max_retries"]))
        ttk.Entry(form_frame, textvariable=retries_var, width=10).grid(row=2, column=1, pady=5)
        
        # Log level
        ttk.Label(form_frame, text="Log Level:").grid(row=3, column=0, sticky="w", pady=5)
        log_level_var = tk.StringVar(value=self.config_manager.config["log_level"])
        ttk.Combobox(form_frame, textvariable=log_level_var, values=["DEBUG", "INFO", "WARNING", "ERROR"], width=10).grid(row=3, column=1, pady=5)
        
        def save_settings():
            """Save settings"""
            try:
                self.config_manager.config["timeout"] = int(timeout_var.get())
                self.config_manager.config["auto_check_interval"] = int(interval_var.get())
                self.config_manager.config["max_retries"] = int(retries_var.get())
                self.config_manager.config["log_level"] = log_level_var.get()
                
                if self.config_manager.save_config():
                    messagebox.showinfo("Success", "Settings saved successfully!")
                    settings_window.destroy()
                    self.log_to_ui("Settings updated", "SUCCESS")
                else:
                    messagebox.showerror("Error", "Failed to save settings!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
        
        # Save button
        ttk.Button(form_frame, text="Save Settings", command=save_settings).grid(row=4, column=0, columnspan=2, pady=20)
    
    def clear_stats(self):
        """Clear statistics"""
        if messagebox.askyesno("Clear Statistics", "Are you sure you want to clear all statistics?"):
            self.stats = {"total_checks": 0, "successful_checks": 0, "failed_checks": 0}
            self.update_statistics()
            self.log_to_ui("Statistics cleared", "INFO")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """GitHub Access Checker - Enhanced Version

A comprehensive tool for monitoring GitHub accessibility with:
• Real-time status checking
• Automatic retry mechanisms
• Detailed logging and statistics
• Configurable settings
• Multiple URL support

Version: 2.0
Created by: Enhanced with advanced features
License: Open Source"""
        
        messagebox.showinfo("About", about_text)
    
    def view_logs(self):
        """Open full log viewer"""
        try:
            log_window = tk.Toplevel(self.root)
            log_window.title("Application Logs")
            log_window.geometry("800x600")
            log_window.transient(self.root)
            
            # Create text widget with scrollbar
            text_frame = ttk.Frame(log_window, padding="10")
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            log_text = scrolledtext.ScrolledText(
                text_frame,
                font=("Consolas", 9),
                bg="#2c3e50",
                fg="#ecf0f1",
                insertbackground="#ecf0f1"
            )
            log_text.pack(fill=tk.BOTH, expand=True)
            
            # Load and display log content
            try:
                with open(self.logger_manager.log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    log_text.insert(tk.END, log_content)
                log_text.config(state=tk.DISABLED)
            except Exception as e:
                log_text.insert(tk.END, f"Failed to load logs: {str(e)}")
                log_text.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log viewer: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.auto_checking:
            if messagebox.askokcancel("Quit", "Auto check is running. Are you sure you want to quit?"):
                self.auto_checking = False
                self.root.quit()
        else:
            self.root.quit()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = GitHubChecker(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()