from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime

# --- ML Prediction Schemas ---

class PredictionRequest(BaseModel):
    state: str = Field(..., description="State name (e.g., 'Uttar Pradesh')")
    district: str = Field(..., description="District name (e.g., 'Agra')")
    year: int = Field(..., description="Target Year", ge=2010, le=2030)
    month: int = Field(..., description="Target Month (1-12)", ge=1, le=12)
    bio_age_5_17: float = Field(..., description="Biometric count for ages 5-17", ge=0)
    bio_age_17_: float = Field(..., description="Biometric count for ages 17+", ge=0)
    
    # Optional context for new districts
    lag_1m_bio: Optional[float] = Field(None)
    lag_2m_bio: Optional[float] = Field(None)
    lag_3m_bio: Optional[float] = Field(None)

    # Enrollment Spec (Optional for flexibility)
    age_0_5: Optional[float] = Field(0, description="Age 0-5 count (for Enrollment Prediction)")
    prediction_type: str = Field("demand", description="'demand' (biometric) or 'enrollment' (adult)")

    @validator('state', 'district')
    def clean_strings(cls, v):
        return v.strip().title()

class BulkPredictionRequest(BaseModel):
    items: List[PredictionRequest]

class OperationalMetrics(BaseModel):
    avgMonthlyLoad: float
    peakPressureRatio: float
    persistenceScore: float

class HistoryPoint(BaseModel):
    month: str
    value: int

class PredictionResponse(BaseModel):
    state: str
    district: str
    prediction: int
    risk_score: float = Field(..., description="Normalized score 0-100")
    status: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    confidence: int
    trend: float
    operationalMetrics: OperationalMetrics
    history: List[HistoryPoint]
    insight: str
    last_updated: datetime = Field(default_factory=datetime.now)

class BulkPredictionResponse(BaseModel):
    results: List[PredictionResponse]
    failed_count: int
    success_count: int

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    records_loaded: int

# --- Insights Schema ---

class FeatureImportanceItem(BaseModel):
    name: str
    value: float
    color: str

class AnomalyItem(BaseModel):
    district: str
    severity: str # High, Medium, Low
    description: str

class InsightsResponse(BaseModel):
    feature_importance: List[FeatureImportanceItem]
    anomalies: List[AnomalyItem]
    seasonal_insight: str
    mape_score: float
    recommendation: str
    api_version: str = "v1.0.0"

# --- Dashboard Schemas (Legacy/Dashboard Integration) ---

class Metric(BaseModel):
    label: str
    value: str
    change: float
    trend: str # 'up', 'down', 'neutral'

class TrendData(BaseModel):
    month: str
    actual: Optional[int]
    predicted: int
    confidenceLower: int
    confidenceUpper: int

class DistrictRisk(BaseModel):
    id: str
    district: str
    state: str
    riskScore: int
    prediction: int
    status: str # 'Critical', 'High', 'Medium', 'Low'

class DashboardResponse(BaseModel):
    kpi: List[Metric]
    trend: List[TrendData]
    districts: List[DistrictRisk]
