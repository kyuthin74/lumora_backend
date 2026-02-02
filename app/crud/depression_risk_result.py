from sqlalchemy.orm import Session
from app.models.depression_risk_result import DepressionRiskResult


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
