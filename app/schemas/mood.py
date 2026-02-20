from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.config import settings


class MoodBase(BaseModel):
    mood_type: str
    activities: List[str] = Field(default_factory=list)
    note: Optional[str] = None


class MoodCreate(MoodBase):
    pass


class MoodResponse(MoodBase):
    mood_id: int
    user_id: int
    created_at: datetime
    timezone: str = Field(default=settings.TIMEZONE, description="Timezone reference for created_at")

    model_config = ConfigDict(from_attributes=True)
