# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.database import Base


# class User(Base):
#     """User ORM model"""
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     full_name = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
#     # Relationships
#     mood_entries = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")
#     depression_risk_results = relationship("DepressionRiskResult", back_populates="user", cascade="all, delete-orphan")
#     alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user response (without password)"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None

