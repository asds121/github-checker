@echo off
REM GitHub Access Checker Enhanced - Startup Script
REM Enhanced version with advanced features

title GitHub Access Checker - Enhanced Version

echo ========================================
echo GitHub Access Checker - Enhanced Version
echo ========================================
echo.

REM Check if Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"
if %errorlevel% neq 0 (
    echo ERROR: Python 3.7 or higher is required!
    echo Current version:
    python --version
    echo.
    echo Please upgrade Python to version 3.7 or higher.
    echo.
    pause
    exit /b 1
)

REM Check if requests module is available
python -c "import requests" >nul 2>nul
if %errorlevel% neq 0 (
    echo INFO: requests module not found. Installing...
    echo.
    python -m pip install requests
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requests module!
        echo Please run: pip install requests
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Successfully installed requests module.
    echo.
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Set Python environment variables for better performance
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1

echo Starting GitHub Access Checker (Enhanced Version)...
echo.
echo Features:
echo - Real-time status checking
echo - Multi-URL support
echo - Detailed logging
echo - Statistics tracking
echo - Configurable settings
echo.
echo To access settings and advanced features, use the menu bar.
echo Press Ctrl+C to stop the application.
echo.

REM Run the enhanced checker
python github_checker.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application failed to start!
    echo.
    echo Possible issues:
    echo - Missing or corrupted files
    echo - Configuration errors
    echo - Permission issues
    echo.
    echo Check the log file for detailed error information.
    echo.
    pause
)