from sqlalchemy.orm import Session
from app.models.depression_test import DepressionTest
from app.schemas.depression_test import DepressionTestCreate


def create_depression_test(db: Session, depression_test: DepressionTestCreate):
    db_test = DepressionTest(**depression_test.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


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
