from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from app.crud.depression_risk_result import create_risk_result
from app.models.depression_test import DepressionTest
from app.schemas.depression_test import DepressionTestCreate
from app.services.prediction_service import prediction_service


def create_depression_test(db: Session, depression_test: DepressionTestCreate):
    db_test = DepressionTest(**depression_test.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    risk_score, risk_level = prediction_service.predict_depression_risk(depression_test.model_dump())
    print("result from prediction service:", risk_level, risk_score)
    risk_result = create_risk_result(
        db=db,
        user_id=db_test.user_id,
        depression_test_id=db_test.depression_test_id,
        risk_level=risk_level,
        risk_score=risk_score,
    )
    return risk_result


def get_depression_test_by_id(db: Session, test_id: int):
    return (
        db.query(DepressionTest)
        .filter(DepressionTest.depression_test_id == test_id)
        .first()
    )


def get_depression_tests_by_user(db: Session, user_id: int):
    return (
        db.query(DepressionTest)
        .filter(DepressionTest.user_id == user_id)
        .order_by(DepressionTest.created_at.desc())
        .all()
    )


def has_user_submitted_test_on_date(
    db: Session,
    user_id: int,
    local_date: date,
    timezone_name: str,
) -> bool:
    tz = ZoneInfo(timezone_name)
    start_local = datetime.combine(local_date, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=1)

    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)

    return (
        db.query(DepressionTest)
        .filter(DepressionTest.user_id == user_id)
        .filter(DepressionTest.created_at >= start_utc)
        .filter(DepressionTest.created_at < end_utc)
        .first()
        is not None
    )
