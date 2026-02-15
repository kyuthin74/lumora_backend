from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.database import get_db
from app.schemas.mood import MoodCreate, MoodResponse
from app.crud.mood import create_mood, get_user_moods, get_daily_moods
from app.api.auth import get_current_user

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


@router.get("/daily", response_model=List[MoodResponse])
def read_daily_moods(
    selected_date: date = Query(..., description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    moods = get_daily_moods(
        db=db,
        user_id=current_user.id,
        selected_date=datetime.combine(selected_date, datetime.min.time())
    )

    return moods


@router.get("/{user_id}", response_model=List[MoodResponse])
def read_user_moods(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all mood journal entries for a user
    """
    return get_user_moods(db, user_id=user_id)
