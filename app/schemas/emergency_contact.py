from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmergencyContactBase(BaseModel):
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[EmailStr] = None
    relationship: Optional[str] = Field(None, max_length=255)


class EmergencyContactCreate(EmergencyContactBase):
    user_id: int


class EmergencyContactUpdate(EmergencyContactBase):
    pass


class EmergencyContactResponse(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
