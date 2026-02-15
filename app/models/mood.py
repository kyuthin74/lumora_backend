from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class MoodJournaling(Base):
    __tablename__ = "mood_journaling"

    mood_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    mood_type = Column(String(length=50), nullable=False)

    activities = Column(
        ARRAY(String(length=100)),
        nullable=False,
        default=list
    )

    note = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationship with User
    user = relationship("User", back_populates="mood_journals")
