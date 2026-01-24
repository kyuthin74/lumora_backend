from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_notify_enabled = Column(Boolean, nullable=False, server_default="false")
    daily_reminder_time = Column(DateTime(timezone=True), nullable=True)
    is_risk_alert_enabled = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    mood_entries = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")
    depression_risk_results = relationship("DepressionRiskResult", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    emergency_contact = relationship("EmergencyContact", back_populates="user", uselist=False, cascade="all, delete-orphan")

    @property
    def emergency_contact_name(self) -> Optional[str]:
        return self.emergency_contact.contact_name if self.emergency_contact else None

    @property
    def emergency_contact_relationship(self) -> Optional[str]:
        return self.emergency_contact.relationship if self.emergency_contact else None

    @property
    def emergency_contact_email(self) -> Optional[str]:
        return self.emergency_contact.contact_email if self.emergency_contact else None

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: str = Field(..., max_length=255)
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    is_notify_enabled: Optional[bool] = False
    daily_reminder_time: Optional[datetime] = None
    is_risk_alert_enabled: Optional[bool] = False

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    is_notify_enabled: Optional[bool] = None
    daily_reminder_time: Optional[datetime] = None
    is_risk_alert_enabled: Optional[bool] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=100)

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    full_name: str
    created_at: datetime
    emergency_contact_name: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    emergency_contact_email: Optional[str] = None
    is_notify_enabled: bool
    daily_reminder_time: Optional[datetime] = None
    is_risk_alert_enabled: bool
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None