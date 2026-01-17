from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from schemas import (
    PredictionRequest, PredictionResponse, HealthResponse, DashboardResponse,
    BulkPredictionRequest, BulkPredictionResponse, InsightsResponse, DistrictRisk,
    BiometricPredictionRequest, BiometricPredictionResponse, TrendData
)
from typing import List, Optional
from model_service import model_service
from dashboard_service import dashboard_service
import uvicorn
import os
from pathlib import Path

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

@app.get("/api/enrollment-trends", response_model=List[TrendData])
async def get_enrollment_trends():
    """Get enrollment trend data (historical + forecast)"""
    try:
        return dashboard_service.get_enrollment_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enrollment trend fetch failed: {str(e)}")

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

@app.post("/api/predict/biometric", response_model=BiometricPredictionResponse)
async def predict_biometric_load(request: BiometricPredictionRequest):
    """Predict Biometric Update Load based on Enrollment Numbers"""
    try:
        return model_service.predict_biometric(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/predict/demographic")
async def predict_demographic_demand(request: PredictionRequest):
    """Predict Demographic Demand using trained demographic model"""
    try:
        result = model_service.predict_demographic(
            state=request.state,
            district=request.district,
            year=request.year,
            month=request.month
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ============================================================================
# VISUALIZATION ENDPOINTS
# ============================================================================

VISUALS_DIR = Path(__file__).parent.parent / "04_visuals"

@app.get("/api/visuals/list")
async def get_visuals_list():
    """Get list of all available visualizations"""
    try:
        visuals = {
            "heatmaps": [],
            "lifecycle": [],
            "trends": [],
            "anomalies": []
        }
        
        for category in visuals.keys():
            category_path = VISUALS_DIR / category
            if category_path.exists():
                visuals[category] = [
                    {
                        "name": f.name,
                        "path": f"visuals/{category}/{f.name}",
                        "category": category,
                        "title": f.stem.replace('_', ' ').title()
                    }
                    for f in category_path.glob("*.png")
                ]
        
        return visuals
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list visualizations: {str(e)}"
        )

@app.get("/api/visuals/{category}/{filename}")
async def get_visual(category: str, filename: str):
    """Serve visualization image"""
    try:
        file_path = VISUALS_DIR / category / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Visualization not found: {category}/{filename}"
            )
        
        return FileResponse(file_path, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

