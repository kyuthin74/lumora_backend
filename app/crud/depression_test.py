from sqlalchemy.orm import Session
from app.crud.depression_risk_result import create_risk_result
from app.models.depression_test import DepressionTest
from app.schemas.depression_test import DepressionTestCreate
from app.services.prediction_service import prediction_service


def create_depression_test(db: Session, depression_test: DepressionTestCreate):
    print(depression_test)
    db_test = DepressionTest(**depression_test.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    print("depression test created with ID:", depression_test.model_dump())
    risk_score, risk_level = prediction_service.predict_depression_risk(depression_test.model_dump())
    print("result from prediction service:", risk_level, risk_score)
    risk_result = create_risk_result(
        db=db,
        user_id=db_test.user_id,
        depression_test_id=db_test.depression_test_id,
        risk_level=risk_level,
        risk_score=risk_score,
    )
    print("depression risk result created with ID:", risk_result)
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
