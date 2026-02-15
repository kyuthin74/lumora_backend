from fastapi.params import Depends, Annotated
from sqlalchemy.orm import Session
from app.models.depression_risk_result import DepressionRiskResult
from typing import Optional

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
