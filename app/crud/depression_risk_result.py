from fastapi.params import Depends, Annotated
from sqlalchemy.orm import Session
from app.models.depression_risk_result import DepressionRiskResult
from typing import Optional, List, Dict
from datetime import datetime, timedelta, date
from collections import defaultdict

from app.services import prediction_service


def create_risk_result(
    db: Session,
    user_id: int,
    risk_level: str,
    risk_score: float,
    depression_test_id: Optional[int] = None,
) -> DepressionRiskResult:
    """
    Create a new depression risk result in the database.
    
    Args:
        db: Database session
        user_id: ID of the user
        risk_level: Risk level (Low, Medium, High)
        risk_score: Risk score (0.0 to 1.0)
        depression_test_id: Optional ID of the related depression test
    
    Returns:
        The created DepressionRiskResult object
    """
    db_result = DepressionRiskResult(
        user_id=user_id,
        depression_test_id=depression_test_id,
        risk_level=risk_level,
        risk_score=risk_score,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_risk_result_by_id(db: Session, result_id: int):
    return (
        db.query(DepressionRiskResult)
        .filter(DepressionRiskResult.result_id == result_id)
        .first()
    )


def get_risk_results_by_user(db: Session, user_id: int):
    return (
        db.query(DepressionRiskResult)
        .filter(DepressionRiskResult.user_id == user_id)
        .order_by(DepressionRiskResult.created_at.desc())
        .all()
    )


def get_latest_risk_result_by_user(db: Session, user_id: int):
    return (
        db.query(DepressionRiskResult)
        .filter(DepressionRiskResult.user_id == user_id)
        .order_by(DepressionRiskResult.created_at.desc())
        .first()
    )


def get_weekly_risk_scores(db: Session, user_id: int) -> List[Dict]:
    """
    Get risk scores aggregated by week for a user.
    
    Args:
        db: Database session
        user_id: ID of the user
    
    Returns:
        List of weekly risk score data with daily breakdowns
    """
    # Get all risk results for the user, ordered by date
    risk_results = (
        db.query(DepressionRiskResult)
        .filter(DepressionRiskResult.user_id == user_id)
        .order_by(DepressionRiskResult.created_at.asc())
        .all()
    )
    
    if not risk_results:
        return []
    
    # Group risk results by week
    weeks_data = defaultdict(lambda: {
        'week_start': None,
        'week_end': None,
        'daily_scores': defaultdict(list)
    })
    
    for result in risk_results:
        # Get the date of the result (without time)
        result_date = result.created_at.date()
        
        # Calculate the Monday of the week this result belongs to
        # ISO weekday: Monday=1, Sunday=7
        weekday = result_date.isoweekday()  # 1=Monday, 7=Sunday
        week_start = result_date - timedelta(days=weekday - 1)
        week_end = week_start + timedelta(days=6)
        
        # Use week_start as the key for grouping
        week_key = week_start
        
        # Store week boundaries
        weeks_data[week_key]['week_start'] = week_start
        weeks_data[week_key]['week_end'] = week_end
        
        # Get day of week name
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_name = day_names[weekday - 1]
        
        # Convert risk_score (0.0-1.0) to percentage (0-100) rounded to 2 decimal places
        risk_percentage = round(result.risk_score * 100, 2)
        
        # Store daily score
        weeks_data[week_key]['daily_scores'][day_name].append(risk_percentage)
    
    # Convert to list format and calculate averages
    weekly_scores = []
    sorted_weeks = sorted(weeks_data.keys())
    
    for week_num, week_start in enumerate(sorted_weeks, 1):
        week_info = weeks_data[week_start]
        
        # Calculate daily averages and build daily_risks list
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_risks = []
        all_daily_averages = []
        
        for day in day_names:
            if day in week_info['daily_scores'] and week_info['daily_scores'][day]:
                # Calculate average for this day
                day_average = round(sum(week_info['daily_scores'][day]) / len(week_info['daily_scores'][day]), 2)
                daily_risks.append({
                    'day': day,
                    'value': day_average
                })
                all_daily_averages.append(day_average)
            else:
                # No data for this day
                daily_risks.append({
                    'day': day,
                    'value': None
                })
        
        # Calculate weekly average (only from days with data)
        if all_daily_averages:
            average_risk = round(sum(all_daily_averages) / len(all_daily_averages), 2)
        else:
            average_risk = 0.0
        
        weekly_scores.append({
            'week_number': week_num,
            'week_start_date': week_info['week_start'],
            'week_end_date': week_info['week_end'],
            'average_risk': average_risk,
            'daily_risks': daily_risks
        })
    
    return weekly_scores

