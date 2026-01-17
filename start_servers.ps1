# UIDAI Aadhaar Analysis - Server Startup Script
# This script starts both backend and frontend servers in separate windows

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  UIDAI ML System - Starting Servers" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Get the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Backend Server in new window
Write-Host "Starting Backend Server (Port 8002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\backend'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; uvicorn main:app --reload --port 8002"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend Server in new window
Write-Host "Starting Frontend Server (Port 5174)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; npm run dev"

# Wait for servers to initialize
Start-Sleep -Seconds 5

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Servers Started Successfully!" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nBackend:  http://localhost:8002" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5174" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C in each window to stop servers`n" -ForegroundColor Yellow
