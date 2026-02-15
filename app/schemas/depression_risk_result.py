from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
