# Start Backend and Frontend, then run integration tests

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "UIDAI System Startup & Test Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$workspaceRoot = "c:\Users\Shakil Ahmad\OneDrive\Desktop\UIDAI\Adhar Analysis"
Set-Location $workspaceRoot

# Check if backend is already running
Write-Host "`n[1/5] Checking if backend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8002/api/health" -Method Get -TimeoutSec 2
    Write-Host "✓ Backend already running!" -ForegroundColor Green
    $backendRunning = $true
} catch {
    Write-Host "✗ Backend not running, starting it..." -ForegroundColor Yellow
    $backendRunning = $false
    
    # Start backend in new window
    $backendPath = Join-Path $workspaceRoot "backend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python -m uvicorn main:app --host 127.0.0.1 --port 8002"
    
    Write-Host "  Waiting for backend to start..." -ForegroundColor Gray
    $maxWait = 30
    $waited = 0
    $started = $false
    
    while ($waited -lt $maxWait -and -not $started) {
        Start-Sleep -Seconds 2
        $waited += 2
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8002/api/health" -Method Get -TimeoutSec 2
            $started = $true
            Write-Host "✓ Backend started successfully!" -ForegroundColor Green
        } catch {
            Write-Host "  Still waiting... ($waited/$maxWait seconds)" -ForegroundColor Gray
        }
    }
    
    if (-not $started) {
        Write-Host "✗ Backend failed to start in $maxWait seconds" -ForegroundColor Red
        exit 1
    }
}

# Check if frontend is running
Write-Host "`n[2/5] Checking if frontend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method Get -TimeoutSec 2
    Write-Host "✓ Frontend already running!" -ForegroundColor Green
    $frontendRunning = $true
} catch {
    Write-Host "✗ Frontend not running, starting it..." -ForegroundColor Yellow
    $frontendRunning = $false
    
    # Start frontend in new window
    $frontendPath = Join-Path $workspaceRoot "frontend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"
    
    Write-Host "  Frontend starting (will check in 10 seconds)..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

# Test Backend Health
Write-Host "`n[3/5] Testing Backend Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8002/api/health" -Method Get
    Write-Host "✓ Status: $($health.status)" -ForegroundColor Green
    Write-Host "✓ Model Loaded: $($health.model_loaded)" -ForegroundColor Green
    Write-Host "✓ Records: $($health.records_loaded)" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend health check failed: $_" -ForegroundColor Red
}

# Test ML Prediction
Write-Host "`n[4/5] Testing ML Prediction..." -ForegroundColor Yellow
try {
    $predictionPayload = @{
        state = "Delhi"
        district = "Central Delhi"
        year = 2024
        month = 6
        bio_age_5_17 = 50000
        bio_age_17_ = 100000
    } | ConvertTo-Json

    $prediction = Invoke-RestMethod -Uri "http://localhost:8002/api/predict" -Method Post -Body $predictionPayload -ContentType "application/json"
    Write-Host "✓ Prediction: $($prediction.predicted_demand)" -ForegroundColor Green
    Write-Host "✓ Confidence: $($prediction.confidence)" -ForegroundColor Green
} catch {
    Write-Host "✗ Prediction failed: $_" -ForegroundColor Red
}

# Run comprehensive test
Write-Host "`n[5/5] Running comprehensive integration test..." -ForegroundColor Yellow
python "$workspaceRoot\test_integration.py"

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "Test Complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "`nBoth servers are running in separate windows." -ForegroundColor White
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "Backend API: http://localhost:8002" -ForegroundColor White
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
