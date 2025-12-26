@echo off
REM Enable ANSI color support on Windows 10/11
reg query "HKCU\Console" /v VirtualTerminalLevel 2>nul | findstr 1 >nul
if %errorlevel% equ 1 (
    reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul
)
chcp 65001 >nul
python "%~dp0cli.py" -f %*
pause
