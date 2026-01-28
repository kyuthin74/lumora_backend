from sqlalchemy.orm import Session

from app.models.mood import MoodJournaling
from app.schemas.mood import MoodCreate

def create_mood(db: Session, user_id: int, mood: MoodCreate):
    new_mood = MoodJournaling(
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
