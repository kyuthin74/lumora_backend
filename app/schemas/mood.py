from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


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

    model_config = ConfigDict(from_attributes=True)
