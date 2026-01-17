@echo off
echo ========================================
echo Starting UIDAI Backend Server
echo ========================================
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8002
pause
