from pydantic import BaseModel
from typing import List, Optional

class MoodCreate(BaseModel):
    mood_type: str
    activities: Optional[List[str]] = []
    note: Optional[str] = None

class MoodResponse(BaseModel):
    mood_id: int
    mood_type: str
    activities: list[str]
    note: str | None
    created_at: str

    class Config:
        from_attributes = True

