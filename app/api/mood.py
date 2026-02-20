from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, date, timezone
from app.database import get_db
from app.schemas.mood import MoodCreate, MoodResponse
from app.crud.mood import create_mood, get_user_moods, get_daily_moods, delete_daily_moods
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/moods",
    tags=["Mood Journaling"]
)


@router.post("/", response_model=MoodResponse)
def log_mood(
    mood: MoodCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Create a new mood journal entry for a user
    """
    return create_mood(db, user_id=current_user.id, mood=mood)


@router.get("/daily", response_model=List[MoodResponse])
def read_daily_moods(
    selected_date: date = Query(..., description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    moods = get_daily_moods(
        db=db,
        user_id=current_user.id,
        selected_date=datetime.combine(selected_date, datetime.min.time(), tzinfo=timezone.utc)
    )

    return moods


@router.delete("/daily", response_model=Dict[str, int])
def delete_daily_moods_endpoint(
    selected_date: date = Query(..., description="Format: YYYY-MM-DD"),
    mood_id: int = Query(..., description="ID of the mood entry to delete"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Delete a single mood journal entry for the current user on a specific date
    """
    deleted_count = delete_daily_moods(
        db=db,
        user_id=current_user.id,
        mood_id=mood_id,
        selected_date=datetime.combine(selected_date, datetime.min.time(), tzinfo=timezone.utc)
    )
    return {"deleted": deleted_count}


@router.get("/", response_model=List[MoodResponse])
def read_user_moods(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get all mood journal entries for a user
    """
    return get_user_moods(db, user_id=current_user.id)
