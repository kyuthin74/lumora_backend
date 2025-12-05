from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.database import get_db
from app.models.chart import MoodChartData, ActivityChartData, RiskChartData, ComprehensiveChartData
from app.crud import mood_entry as mood_crud, depression_risk_result as risk_crud
from app.api.auth import get_current_user
from app.utils.helpers import map_mood_to_numeric, format_date

router = APIRouter(prefix="/charts", tags=["Charts"])


@router.get("/mood", response_model=MoodChartData)
async def get_mood_chart(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mood chart data"""
    entries = mood_crud.get_user_mood_entries(db, user_id=current_user.id, limit=1000, days=days)
    
    # Prepare data
    dates = []
    mood_levels = []
    sleep_hours = []
    stress_levels = []
    
    for entry in reversed(entries):  # Oldest first
        dates.append(format_date(entry.created_at))
        mood_levels.append(map_mood_to_numeric(entry.mood_level))
        sleep_hours.append(entry.sleep_hours)
        stress_levels.append(entry.stress_level)
    
    return MoodChartData(
        dates=dates,
        mood_levels=mood_levels,
        sleep_hours=sleep_hours,
        stress_levels=stress_levels
    )


@router.get("/activity", response_model=ActivityChartData)
async def get_activity_chart(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity chart data"""
    entries = mood_crud.get_user_mood_entries(db, user_id=current_user.id, limit=1000, days=days)
    
    dates = []
    physical_activity = []
    social_interaction = []
    
    for entry in reversed(entries):
        dates.append(format_date(entry.created_at))
        physical_activity.append(entry.physical_activity_minutes)
        social_interaction.append(entry.social_interaction_level)
    
    return ActivityChartData(
        dates=dates,
        physical_activity=physical_activity,
        social_interaction=social_interaction
    )


@router.get("/risk", response_model=RiskChartData)
async def get_risk_chart(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk trend chart data"""
    results = risk_crud.get_user_risk_results(db, user_id=current_user.id, limit=1000, days=days)
    
    dates = []
    risk_scores = []
    risk_levels = []
    
    for result in reversed(results):
        dates.append(format_date(result.created_at))
        risk_scores.append(result.risk_score)
        risk_levels.append(result.risk_level)
    
    return RiskChartData(
        dates=dates,
        risk_scores=risk_scores,
        risk_levels=risk_levels
    )


@router.get("/comprehensive", response_model=ComprehensiveChartData)
async def get_comprehensive_chart(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive chart data"""
    # Get mood data
    mood_entries = mood_crud.get_user_mood_entries(db, user_id=current_user.id, limit=1000, days=days)
    
    mood_dates = []
    mood_levels = []
    sleep_hours = []
    stress_levels = []
    physical_activity = []
    social_interaction = []
    
    for entry in reversed(mood_entries):
        mood_dates.append(format_date(entry.created_at))
        mood_levels.append(map_mood_to_numeric(entry.mood_level))
        sleep_hours.append(entry.sleep_hours)
        stress_levels.append(entry.stress_level)
        physical_activity.append(entry.physical_activity_minutes)
        social_interaction.append(entry.social_interaction_level)
    
    # Get risk data
    risk_results = risk_crud.get_user_risk_results(db, user_id=current_user.id, limit=1000, days=days)
    
    risk_dates = []
    risk_scores = []
    risk_levels = []
    
    for result in reversed(risk_results):
        risk_dates.append(format_date(result.created_at))
        risk_scores.append(result.risk_score)
        risk_levels.append(result.risk_level)
    
    return ComprehensiveChartData(
        mood_data=MoodChartData(
            dates=mood_dates,
            mood_levels=mood_levels,
            sleep_hours=sleep_hours,
            stress_levels=stress_levels
        ),
        activity_data=ActivityChartData(
            dates=mood_dates,
            physical_activity=physical_activity,
            social_interaction=social_interaction
        ),
        risk_data=RiskChartData(
            dates=risk_dates,
            risk_scores=risk_scores,
            risk_levels=risk_levels
        ),
        period_days=days
    )
