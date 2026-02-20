from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class DepressionRiskResultCreate(BaseModel):
    """Schema for creating a new depression risk result"""
    user_id: int = Field(..., description="ID of the user")
    depression_test_id: Optional[int] = Field(None, description="ID of the related depression test")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0.0 and 1.0")


class DepressionRiskResultResponse(BaseModel):
    result_id: int
    user_id: int
    depression_test_id: Optional[int]

    risk_level: str
    risk_score: float

    created_at: datetime

    class Config:
        from_attributes = True


class DailyRisk(BaseModel):
    """Schema for daily risk value"""
    day: str = Field(..., description="Day of the week (Mon, Tue, Wed, etc.)")
    value: Optional[float] = Field(None, description="Risk score as a percentage (0-100)")


class WeeklyRiskScore(BaseModel):
    """Schema for weekly aggregated risk scores"""
    week_number: int = Field(..., description="Week number in the series")
    week_start_date: date = Field(..., description="Start date of the week (Monday)")
    week_end_date: date = Field(..., description="End date of the week (Sunday)")
    average_risk: float = Field(..., description="Average risk score for the week (0-100)")
    daily_risks: List[DailyRisk] = Field(..., description="Daily risk scores for the week")


class WeeklyRiskScoresResponse(BaseModel):
    """Schema for weekly risk scores response"""
    user_id: str = Field(..., description="ID of the user")
    weeks: List[WeeklyRiskScore] = Field(..., description="List of weekly risk scores")
