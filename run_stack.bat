@echo off
echo Starting Backend...
start "Backend Server" /D "%~dp0" cmd /k "python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8002"

echo Starting Frontend...
start "Frontend Server" /D "%~dp0frontend" cmd /k "npm run dev"

echo Full Stack Started!
echo Backend: http://localhost:8002/docs
echo Frontend: http://localhost:5173 (or check console)
