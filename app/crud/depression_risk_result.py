from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.schemas.depression_risk_result import DepressionRiskResult
from typing import List, Optional
from datetime import datetime, timedelta


def create_risk_result(
    db: Session,
    user_id: int,
    risk_level: str,
    risk_score: float,
    input_data: dict,
    mood_entry_id: Optional[int] = None
) -> DepressionRiskResult:
    """Create new depression risk result"""
    db_risk = DepressionRiskResult(
        user_id=user_id,
        mood_entry_id=mood_entry_id,
        risk_level=risk_level,
        risk_score=risk_score,
        input_data=input_data
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk


def get_risk_result_by_id(db: Session, risk_id: int, user_id: int) -> Optional[DepressionRiskResult]:
    """Get risk result by ID"""
    return db.query(DepressionRiskResult).filter(
        DepressionRiskResult.id == risk_id,
        DepressionRiskResult.user_id == user_id
    ).first()


def get_user_risk_results(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    days: Optional[int] = None
) -> List[DepressionRiskResult]:
    """Get all risk results for a user"""
    query = db.query(DepressionRiskResult).filter(DepressionRiskResult.user_id == user_id)
    
    if days:
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(DepressionRiskResult.created_at >= start_date)
    
    return query.order_by(desc(DepressionRiskResult.created_at)).offset(skip).limit(limit).all()


def get_latest_risk_result(db: Session, user_id: int) -> Optional[DepressionRiskResult]:
    """Get the most recent risk result for a user"""
    return db.query(DepressionRiskResult).filter(
        DepressionRiskResult.user_id == user_id
    ).order_by(desc(DepressionRiskResult.created_at)).first()


def get_risk_trend(db: Session, user_id: int, days: int = 30) -> dict:
    """Get risk trend analysis"""
    results = get_user_risk_results(db, user_id, limit=100, days=days)
    
    if not results:
        return {
            'current_risk': None,
            'previous_risk': None,
            'trend': 'no_data',
            'change_percentage': None
        }
    
    current = results[0].risk_score
    previous = results[1].risk_score if len(results) > 1 else None
    
    if previous is not None and previous > 0:
        change_pct = ((current - previous) / previous) * 100
        if change_pct < -10:
            trend = 'improving'
        elif change_pct > 10:
            trend = 'worsening'
        else:
            trend = 'stable'
    else:
        change_pct = None
        trend = 'insufficient_data'
    
    return {
        'current_risk': current,
        'previous_risk': previous,
        'trend': trend,
        'change_percentage': change_pct
    }
