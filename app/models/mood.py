from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MoodLevel(str, Enum):
    """Mood level enumeration"""
    VERY_POOR = "very_poor"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class SleepQuality(str, Enum):
    """Sleep quality enumeration"""
    VERY_POOR = "very_poor"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class MoodEntryBase(BaseModel):
    """Base mood entry schema"""
    mood_level: MoodLevel
    sleep_hours: float = Field(..., ge=0, le=24)
    sleep_quality: SleepQuality
    physical_activity_minutes: int = Field(..., ge=0, le=1440)
    social_interaction_level: int = Field(..., ge=1, le=5)
    stress_level: int = Field(..., ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=1000)


class MoodEntryCreate(MoodEntryBase):
    """Schema for creating mood entry"""
    pass


class MoodEntryUpdate(BaseModel):
    """Schema for updating mood entry"""
    mood_level: Optional[MoodLevel] = None
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    sleep_quality: Optional[SleepQuality] = None
    physical_activity_minutes: Optional[int] = Field(None, ge=0, le=1440)
    social_interaction_level: Optional[int] = Field(None, ge=1, le=5)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=1000)


class MoodEntryResponse(MoodEntryBase):
    """Schema for mood entry response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    depression_risk_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class MoodStats(BaseModel):
    """Schema for mood statistics"""
    average_mood: float
    average_sleep_hours: float
    average_stress_level: float
    total_entries: int
    period_start: datetime
    period_end: datetime
