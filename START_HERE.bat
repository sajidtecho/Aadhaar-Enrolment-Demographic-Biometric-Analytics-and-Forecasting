@echo off
REM UIDAI Aadhaar Analysis - Quick Start Script
REM Double-click this file to start both servers

echo ========================================
echo   UIDAI ML System - Quick Start
echo ========================================
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0start_servers.ps1"

pause
