from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.mood import MoodEntryCreate, MoodEntryUpdate, MoodEntryResponse, MoodStats
from app.crud import mood_entry as mood_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/mood", tags=["Mood"])


@router.post("/entries", response_model=MoodEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_mood_entry(
    mood_entry: MoodEntryCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new mood entry"""
    db_mood = mood_crud.create_mood_entry(db, user_id=current_user.id, mood_entry=mood_entry)
    return db_mood


@router.get("/entries", response_model=List[MoodEntryResponse])
async def get_mood_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    days: Optional[int] = Query(None, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all mood entries for current user"""
    entries = mood_crud.get_user_mood_entries(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        days=days
    )
    return entries


@router.get("/entries/{mood_id}", response_model=MoodEntryResponse)
async def get_mood_entry(
    mood_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific mood entry"""
    mood_entry = mood_crud.get_mood_entry_by_id(db, mood_id=mood_id, user_id=current_user.id)
    
    if not mood_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    return mood_entry


@router.put("/entries/{mood_id}", response_model=MoodEntryResponse)
async def update_mood_entry(
    mood_id: int,
    mood_update: MoodEntryUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a mood entry"""
    updated_mood = mood_crud.update_mood_entry(
        db,
        mood_id=mood_id,
        user_id=current_user.id,
        mood_update=mood_update
    )
    
    if not updated_mood:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    return updated_mood


@router.delete("/entries/{mood_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood_entry(
    mood_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a mood entry"""
    success = mood_crud.delete_mood_entry(db, mood_id=mood_id, user_id=current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood entry not found"
        )
    
    return None


@router.get("/statistics", response_model=dict)
async def get_mood_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mood statistics for current user"""
    stats = mood_crud.get_mood_statistics(db, user_id=current_user.id, days=days)
    return stats
