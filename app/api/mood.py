from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.mood import MoodCreate, MoodResponse
from app.crud.mood import create_mood, get_user_moods

router = APIRouter(
    prefix="/moods",
    tags=["Mood Journaling"]
)


@router.post("/{user_id}", response_model=MoodResponse)
def log_mood(
    user_id: int,
    mood: MoodCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new mood journal entry for a user
    """
    return create_mood(db, user_id=user_id, mood=mood)


@router.get("/{user_id}", response_model=List[MoodResponse])
def read_user_moods(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all mood journal entries for a user
    """
    return get_user_moods(db, user_id=user_id)
