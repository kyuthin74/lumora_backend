"""SQLAlchemy ORM model for depression risk results"""

from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DepressionRiskResult(Base):
    """Depression risk assessment result ORM model"""
    __tablename__ = "depression_risk_results"
    
    result_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    depression_test_id = Column(Integer, ForeignKey("depression_tests.depression_test_id"), nullable=True, index=True)
    
    # Risk assessment results
    risk_level = Column(String, nullable=False)  # Low, Medium, High
    risk_score = Column(Float, nullable=False)  # 0.0 to 1.0
    
    # Store input data for audit/analysis
    # input_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="depression_risk_results")
    depression_test = relationship("DepressionTest", back_populates="depression_risk_results")
