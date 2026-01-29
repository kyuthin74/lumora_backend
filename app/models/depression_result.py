from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class DepressionResult(Base):
    __tablename__ = "depression_results"

    result_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    depression_test_id = Column(
        Integer,
        ForeignKey("depression_tests.depression_test_id"),
        nullable=False
    )

    score = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User", back_populates="depression_results")
    depression_test = relationship("DepressionTest", back_populates="depression_results")