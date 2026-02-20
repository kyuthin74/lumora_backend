from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class NotificationBase(BaseModel):
    type: Literal["result", "reminder", "mailsent", "highrisk"] = Field(
        ..., description="Type of notification"
    )
    title: str = Field(..., max_length=255, description="Notification title")
    message: str = Field(..., description="Notification body text")


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
