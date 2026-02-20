from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.mood import MoodJournaling
from app.schemas.mood import MoodCreate


def _as_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware in UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def create_mood(db: Session, user_id: int, mood: MoodCreate):
    new_mood = MoodJournaling(
        created_at=datetime.now(timezone.utc),
        user_id=user_id,
        mood_type=mood.mood_type,
        activities=mood.activities,
        note=mood.note
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return new_mood

def get_user_moods(db: Session, user_id: int):
    return db.query(MoodJournaling)\
        .filter(MoodJournaling.user_id == user_id)\
        .order_by(MoodJournaling.created_at.desc())\
        .all()

def get_daily_moods(db: Session, user_id: int, selected_date: datetime):
    selected_date = _as_utc(selected_date)
    start_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = selected_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    return db.query(MoodJournaling).filter(
        MoodJournaling.user_id == user_id,
        MoodJournaling.created_at >= start_date,
        MoodJournaling.created_at <= end_date
    ).all()


def delete_daily_moods(db: Session, user_id: int, mood_id: int, selected_date: datetime) -> int:
    selected_date = _as_utc(selected_date)
    start_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = selected_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    entry = db.query(MoodJournaling).filter(
        MoodJournaling.mood_id == mood_id,
        MoodJournaling.user_id == user_id,
        MoodJournaling.created_at >= start_date,
        MoodJournaling.created_at <= end_date
    ).first()

    if not entry:
        return 0

    db.delete(entry)
    db.commit()
    return 1