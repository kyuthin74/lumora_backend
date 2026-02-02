"""Pydantic schemas for depression risk assessment"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DepressionRiskInput(BaseModel):
    """Input schema for depression risk prediction"""
    age: int = Field(..., ge=10, le=120, description="User's age")
    gender: str = Field(..., description="Gender (Male, Female, Other)")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep per night")
    physical_activity_hours: float = Field(..., ge=0, le=24, description="Hours of physical activity per day")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level (1-10)")
    social_support: int = Field(..., ge=1, le=5, description="Social support level (1-5)")
    mood_level: int = Field(..., ge=1, le=5, description="Current mood level (1-5)")
    family_history: str = Field(..., description="Family history of depression (Yes, No)")


class DepressionRiskResult(BaseModel):
    """Depression risk assessment result"""
    id: int
    user_id: int
    mood_entry_id: Optional[int] = None
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score (0.0 to 1.0)")
    input_data: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DepressionRiskResponse(BaseModel):
    """Response schema for depression risk prediction"""
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk probability (0.0 to 1.0)")
    message: str = Field(..., description="Risk assessment message")
    recommendations: list[str] = Field(default_factory=list, description="Recommendations based on risk level")
    result_id: Optional[int] = None


class RiskTrend(BaseModel):
    """Risk trend analysis"""
    current_risk: Optional[float] = Field(None, description="Current risk score")
    previous_risk: Optional[float] = Field(None, description="Previous risk score")
    trend: str = Field(..., description="Trend direction (improving, stable, worsening, no_data, insufficient_data)")
    change_percentage: Optional[float] = Field(None, description="Percentage change in risk")
    period_days: int = Field(default=30, description="Analysis period in days")
