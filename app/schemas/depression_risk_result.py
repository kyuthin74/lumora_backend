from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepressionRiskResultResponse(BaseModel):
    result_id: int
    user_id: int
    depression_test_id: Optional[int]

    risk_level: str
    risk_score: float

    created_at: datetime

    class Config:
        from_attributes = True
