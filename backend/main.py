from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    PredictionRequest, PredictionResponse, HealthResponse, DashboardResponse,
    BulkPredictionRequest, BulkPredictionResponse, InsightsResponse, DistrictRisk
)
from typing import List, Optional
from .model_service import model_service
from .dashboard_service import dashboard_service
import uvicorn
import os

app = FastAPI(
    title="Aadhaar Analytics AI API",
    description="Enterprise-grade ML System for Biometric Demand Forecasting",
    version="1.0.0"
)

# Production-ready CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "*" # For this demo, allow all. In prod, strict list.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """System Health & Model Status Check"""
    is_loaded = model_service.model is not None
    record_count = len(model_service.data) if model_service.data is not None else 0
    
    if not is_loaded:
        return HealthResponse(
            status="degraded", 
            model_loaded=False, 
            records_loaded=record_count
        )
        
    return HealthResponse(
        status="online",
        model_loaded=True,
        records_loaded=record_count
    )

@app.get("/api/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    """Complete Dashboard Aggregates (Real Data)"""
    try:
        data = dashboard_service.get_dashboard_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard aggregation failed: {str(e)}")

@app.get("/api/anomalies", response_model=List[DistrictRisk])
async def get_anomalies():
    """Get full risk assessment report for all districts."""
    try:
        return dashboard_service.get_full_risk_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly scan failed: {str(e)}")

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_single(request: PredictionRequest):
    """
    Generate Demand Prediction for a Single District.
    Uses strictly trained ML model + Historical Context.
    """
    try:
        result = model_service.predict_single(request)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/api/predict-bulk", response_model=BulkPredictionResponse)
async def predict_bulk(payload: BulkPredictionRequest):
    """
    Batch Processing for Regional Analysis.
    """
    results = []
    failed = 0
    success = 0
    
    for item in payload.items:
        try:
            res = model_service.predict_single(item)
            results.append(res)
            success += 1
        except Exception:
            failed += 1
            # In bulk, we might skip failures or return error objects. 
            # For now, we omit failed ones to keep schema simple.
            
    return BulkPredictionResponse(
        results=results,
        failed_count=failed,
        success_count=success
    )

@app.get("/api/insights", response_model=InsightsResponse)
async def get_model_insights(state: Optional[str] = None, district: Optional[str] = None):
    """Get model explainability, anomalies and seasonal trends."""
    if not model_service.model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not currently loaded"
        )
    return model_service.get_insights(state=state, district=district)

if __name__ == "__main__":
    # Production configuration
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)

