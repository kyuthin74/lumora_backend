from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.schemas.mood_entry import MoodEntry
from app.models.mood import MoodEntryCreate, MoodEntryUpdate
from typing import List, Optional
from datetime import datetime, timedelta


def create_mood_entry(db: Session, user_id: int, mood_entry: MoodEntryCreate) -> MoodEntry:
    """Create new mood entry"""
    db_mood = MoodEntry(
        user_id=user_id,
        mood_level=mood_entry.mood_level.value,
        sleep_hours=mood_entry.sleep_hours,
        sleep_quality=mood_entry.sleep_quality.value,
        physical_activity_minutes=mood_entry.physical_activity_minutes,
        social_interaction_level=mood_entry.social_interaction_level,
        stress_level=mood_entry.stress_level,
        notes=mood_entry.notes
    )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return db_mood


def get_mood_entry_by_id(db: Session, mood_id: int, user_id: int) -> Optional[MoodEntry]:
    """Get mood entry by ID"""
    return db.query(MoodEntry).filter(
        MoodEntry.id == mood_id,
        MoodEntry.user_id == user_id
    ).first()


def get_user_mood_entries(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    days: Optional[int] = None
) -> List[MoodEntry]:
    """Get all mood entries for a user"""
    query = db.query(MoodEntry).filter(MoodEntry.user_id == user_id)
    
    if days:
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(MoodEntry.created_at >= start_date)
    
    return query.order_by(desc(MoodEntry.created_at)).offset(skip).limit(limit).all()


def update_mood_entry(
    db: Session, 
    mood_id: int, 
    user_id: int, 
    mood_update: MoodEntryUpdate
) -> Optional[MoodEntry]:
    """Update mood entry"""
    db_mood = get_mood_entry_by_id(db, mood_id, user_id)
    if not db_mood:
        return None
    
    update_data = mood_update.model_dump(exclude_unset=True)
    
    # Convert enum values to strings
    for field, value in update_data.items():
        if hasattr(value, 'value'):
            update_data[field] = value.value
    
    for field, value in update_data.items():
        setattr(db_mood, field, value)
    
    db.commit()
    db.refresh(db_mood)
    return db_mood


def delete_mood_entry(db: Session, mood_id: int, user_id: int) -> bool:
    """Delete mood entry"""
    db_mood = get_mood_entry_by_id(db, mood_id, user_id)
    if not db_mood:
        return False
    
    db.delete(db_mood)
    db.commit()
    return True


def update_mood_risk_score(db: Session, mood_id: int, risk_score: float) -> Optional[MoodEntry]:
    """Update depression risk score for a mood entry"""
    db_mood = db.query(MoodEntry).filter(MoodEntry.id == mood_id).first()
    if not db_mood:
        return None
    
    db_mood.depression_risk_score = risk_score
    db.commit()
    db.refresh(db_mood)
    return db_mood


def get_mood_statistics(db: Session, user_id: int, days: int = 30) -> dict:
    """Get mood statistics for a user"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    stats = db.query(
        func.avg(MoodEntry.sleep_hours).label('avg_sleep'),
        func.avg(MoodEntry.stress_level).label('avg_stress'),
        func.count(MoodEntry.id).label('total_entries')
    ).filter(
        MoodEntry.user_id == user_id,
        MoodEntry.created_at >= start_date
    ).first()
    
    return {
        'average_sleep_hours': float(stats.avg_sleep) if stats.avg_sleep else 0,
        'average_stress_level': float(stats.avg_stress) if stats.avg_stress else 0,
        'total_entries': stats.total_entries or 0,
        'period_days': days
    }
