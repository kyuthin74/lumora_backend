from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship as orm_relationship
from sqlalchemy.sql import func
from app.database import Base


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    __table_args__ = (UniqueConstraint("user_id", name="uq_emergency_contacts_user_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_relationship = Column("relationship", String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = orm_relationship("User", back_populates="emergency_contact")

    @property
    def relationship(self) -> str | None:
        # Backward-compatible accessor to the contact relationship string
        return self.contact_relationship
