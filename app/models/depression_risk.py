from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DepressionRiskInput(BaseModel):
    """Schema for depression risk prediction input"""
    age: int = Field(..., ge=10, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    sleep_hours: float = Field(..., ge=0, le=24)
    physical_activity_hours: float = Field(..., ge=0, le=24)
    stress_level: int = Field(..., ge=1, le=10)
    social_support: int = Field(..., ge=1, le=5)
    mood_level: int = Field(..., ge=1, le=5)
    family_history: str = Field(..., pattern="^(Yes|No)$")


class DepressionRiskResult(BaseModel):
    """Schema for depression risk prediction result"""
    risk_level: str  # "Low", "Medium", "High"
    risk_score: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    recommendation: str
    

class DepressionRiskResponse(BaseModel):
    """Schema for depression risk response with history"""
    id: int
    user_id: int
    mood_entry_id: Optional[int] = None
    risk_level: str
    risk_score: float
    input_data: dict
    created_at: datetime
    
    class Config:
        from_attributes = True


class RiskTrend(BaseModel):
    """Schema for risk trend analysis"""
    current_risk: float
    previous_risk: Optional[float] = None
    trend: str  # "improving", "stable", "worsening"
    change_percentage: Optional[float] = None
