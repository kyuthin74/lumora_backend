from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MoodEntry(Base):
    """Mood entry ORM model"""
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Mood data
    mood_level = Column(String, nullable=False)  # very_poor, poor, fair, good, excellent
    sleep_hours = Column(Float, nullable=False)
    sleep_quality = Column(String, nullable=False)  # very_poor, poor, fair, good, excellent
    physical_activity_minutes = Column(Integer, nullable=False)
    social_interaction_level = Column(Integer, nullable=False)  # 1-5
    stress_level = Column(Integer, nullable=False)  # 1-10
    notes = Column(Text, nullable=True)
    
    # Risk assessment (computed after ML prediction)
    depression_risk_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="mood_entries")
    depression_risk_result = relationship("DepressionRiskResult", back_populates="mood_entry", uselist=False)
