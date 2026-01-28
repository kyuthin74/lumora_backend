"""
Read-only helpers for mood journaling.
Used for charts, weekly analysis, and chatbot context.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.mood import MoodJournaling
from app.utils import helpers

@dataclass
class MoodEntryAdapter:
    id: int
    user_id: int
    mood_level: str
    notes: Optional[str]
    created_at: datetime

def _adapt(journal: MoodJournaling) -> MoodEntryAdapter:
    """
    Convert MoodJournaling ORM object into a lightweight structure
    for charts and chatbot.
    """
    return MoodEntryAdapter(
        id=journal.mood_id,
        user_id=journal.user_id,
        mood_level=(journal.mood_type or "neutral").lower(),
        notes=journal.note,
        created_at=journal.created_at,
    )

def get_user_mood_entries(
    db: Session,
    user_id: int,
    limit: Optional[int] = None,
    days: Optional[int] = None,
) -> List[MoodEntryAdapter]:
    """
    Return mood entries for a user (newest first).
    Optional filters:
    - limit: number of records
    - days: last N days
    """

    query = db.query(MoodJournaling).filter(
        MoodJournaling.user_id == user_id
    )

    if days and days > 0:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = query.filter(MoodJournaling.created_at >= cutoff)

    query = query.order_by(MoodJournaling.created_at.desc())

    if limit and limit > 0:
        query = query.limit(limit)

    journals = query.all()
    return [_adapt(journal) for journal in journals]

def get_mood_statistics(
    db: Session,
    user_id: int,
    days: int = 30,
) -> dict:
    """
    Calculate simple mood statistics for a user.
    """

    entries = get_user_mood_entries(
        db=db,
        user_id=user_id,
        days=days,
    )

    mood_scores = [
        helpers.map_mood_to_numeric(entry.mood_level)
        for entry in entries
        if entry.mood_level
    ]

    average_mood = (
        helpers.calculate_average(mood_scores)
        if mood_scores else None
    )

    return {
        "total_entries": len(entries),
        "average_mood": average_mood,
    }
