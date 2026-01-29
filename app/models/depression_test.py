from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class DepressionTest(Base):
    __tablename__ = "depression_tests"

    depression_test_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sleep_hour = Column(String, nullable=True)
    appetite = Column(String, nullable=True)
    exercise = Column(String, nullable=True)
    screen_time = Column(Boolean, nullable=True)
    academic_work = Column(String, nullable=True)
    socialize = Column(Boolean, nullable=True)
    energy_level = Column(Integer, nullable=True)
    trouble_concentrating = Column(String, nullable=True)
    negative_thoughts = Column(String, nullable=True)
    decision_making = Column(String, nullable=True)
    bothered_things = Column(String, nullable=True)
    stressful_events = Column(String, nullable=True)

    PHQ_label_one = Column(String, nullable=True)
    PHQ_label_two = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship
    user = relationship("User", back_populates="depression_tests")
    depression_results = relationship("DepressionResult", back_populates="depression_test", uselist=False, cascade="all, delete-orphan")