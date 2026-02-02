from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DepressionTestCreate(BaseModel):
    user_id: int

    sleep_hour: Optional[str] = None
    appetite: Optional[str] = None
    exercise: Optional[str] = None
    screen_time: Optional[bool] = None
    academic_work: Optional[str] = None
    socialize: Optional[bool] = None
    energy_level: Optional[int] = None
    trouble_concentrating: Optional[str] = None
    negative_thoughts: Optional[str] = None
    decision_making: Optional[str] = None
    bothered_things: Optional[str] = None
    stressful_events: Optional[str] = None

    PHQ_label_one: Optional[str] = None
    PHQ_label_two: Optional[str] = None


class DepressionTestResponse(BaseModel):
    depression_test_id: int
    user_id: int

    sleep_hour: Optional[str]
    appetite: Optional[str]
    exercise: Optional[str]
    screen_time: Optional[bool]
    academic_work: Optional[str]
    socialize: Optional[bool]
    energy_level: Optional[int]
    trouble_concentrating: Optional[str]
    negative_thoughts: Optional[str]
    decision_making: Optional[str]
    bothered_things: Optional[str]
    stressful_events: Optional[str]

    PHQ_label_one: Optional[str]
    PHQ_label_two: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True
