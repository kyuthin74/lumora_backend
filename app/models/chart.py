from pydantic import BaseModel
from typing import List
from datetime import datetime


class ChartDataPoint(BaseModel):
    """Single data point for charts"""
    timestamp: datetime
    value: float
    label: str


class MoodChartData(BaseModel):
    """Mood chart data schema"""
    dates: List[str]
    mood_levels: List[float]
    sleep_hours: List[float]
    stress_levels: List[int]


class ActivityChartData(BaseModel):
    """Activity chart data schema"""
    dates: List[str]
    physical_activity: List[int]
    social_interaction: List[int]


class RiskChartData(BaseModel):
    """Risk trend chart data schema"""
    dates: List[str]
    risk_scores: List[float]
    risk_levels: List[str]


class ComprehensiveChartData(BaseModel):
    """Comprehensive chart data response"""
    mood_data: MoodChartData
    activity_data: ActivityChartData
    risk_data: RiskChartData
    period_days: int
