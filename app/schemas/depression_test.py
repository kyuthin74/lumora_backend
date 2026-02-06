from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DepressionTestCreate(BaseModel):
    user_id: int

    mood: Optional[str] = None
    sleep_hour: Optional[str] = None
    appetite: Optional[str] = None
    exercise: Optional[str] = None
    screen_time: Optional[str] = None
    academic_work: Optional[str] = None
    socialize: Optional[str] = None
    energy_level: Optional[int] = None
    trouble_concentrating: Optional[str] = None
    negative_thoughts: Optional[str] = None
    decision_making: Optional[str] = None
    bothered_things: Optional[str] = None
    stressful_events: Optional[str] = None
    future_hope: Optional[str] = None


class DepressionTestResponse(BaseModel):
    depression_test_id: int
    user_id: int

    mood: Optional[str]
    sleep_hour: Optional[str]
    appetite: Optional[str]
    exercise: Optional[str]
    screen_time: Optional[str]
    academic_work: Optional[str]
    socialize: Optional[str]
    energy_level: Optional[int]
    trouble_concentrating: Optional[str]
    negative_thoughts: Optional[str]
    decision_making: Optional[str]
    bothered_things: Optional[str]
    stressful_events: Optional[str]
    future_hope: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True
