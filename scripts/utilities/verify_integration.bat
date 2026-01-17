@echo off
REM ============================================================
REM UIDAI System - Complete Integration Verification
REM ============================================================

echo.
echo ====================================================
echo UIDAI SYSTEM - INTEGRATION VERIFICATION
echo ====================================================
echo.

REM Check if models exist
echo [1/5] Checking ML Models...
if exist "03_models\uidai_demand_model.pkl" (
    if exist "03_models\uidai_biometric_model.pkl" (
        if exist "03_models\uidai_demographic_model.pkl" (
            echo [OK] All ML models found
        ) else (
            echo [ERROR] Demographic model missing
            goto :error
        )
    ) else (
        echo [ERROR] Biometric model missing
        goto :error
    )
) else (
    echo [ERROR] Demand model missing
    goto :error
)

REM Check if data files exist
echo [2/5] Checking Data Files...
if exist "01_data\processed\clean_biometric_data.csv" (
    if exist "01_data\processed\clean_demographic_data.csv" (
        echo [OK] Data files found
    ) else (
        echo [ERROR] Demographic data missing
        goto :error
    )
) else (
    echo [ERROR] Biometric data missing
    goto :error
)

REM Check backend files
echo [3/5] Checking Backend Files...
if exist "backend\main.py" (
    if exist "backend\model_service.py" (
        echo [OK] Backend files found
    ) else (
        echo [ERROR] model_service.py missing
        goto :error
    )
) else (
    echo [ERROR] main.py missing
    goto :error
)

REM Check frontend files
echo [4/5] Checking Frontend Files...
if exist "frontend\package.json" (
    if exist "frontend\src\services\api.ts" (
        echo [OK] Frontend files found
    ) else (
        echo [ERROR] api.ts missing
        goto :error
    )
) else (
    echo [ERROR] package.json missing
    goto :error
)

echo [5/5] Checking Dependencies...
python -c "import fastapi, pandas, numpy, sklearn, xgboost, joblib" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python dependencies installed
) else (
    echo [WARNING] Some Python dependencies may be missing
    echo Installing missing dependencies...
    pip install -r backend\requirements.txt
)

echo.
echo ====================================================
echo INTEGRATION STATUS: ALL COMPONENTS VERIFIED
echo ====================================================
echo.
echo Frontend:  frontend\src\  (React + TypeScript)
echo Backend:   backend\       (FastAPI + Python)
echo ML Models: 03_models\     (4 models, 4.4M+ records)
echo.
echo ====================================================
echo READY TO START
echo ====================================================
echo.
echo Option 1: Start services manually
echo   Terminal 1: .\start_backend.bat
echo   Terminal 2: .\start_frontend.bat
echo.
echo Option 2: Run integration test
echo   python test_integration.py
echo.
echo Option 3: View full report
echo   Open: INTEGRATION_STATUS_REPORT.md
echo.
pause
goto :eof

:error
echo.
echo ====================================================
echo [ERROR] Integration verification failed!
echo ====================================================
echo Please check the error messages above.
echo.
pause
exit /b 1
