from sqlalchemy.orm import Session
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency_contact import EmergencyContactCreate, EmergencyContactUpdate
from typing import Optional


def get_emergency_contact_by_user_id(db: Session, user_id: int) -> Optional[EmergencyContact]:
    """Get emergency contact by user ID"""
    return db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id).first()


def create_emergency_contact(db: Session, contact: EmergencyContactCreate) -> EmergencyContact:
    """Create new emergency contact"""
    db_contact = EmergencyContact(
        user_id=contact.user_id,
        contact_name=contact.contact_name,
        contact_email=contact.contact_email,
        contact_relationship=contact.relationship,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_emergency_contact(
    db: Session, user_id: int, contact_update: EmergencyContactUpdate
) -> Optional[EmergencyContact]:
    """Update emergency contact"""
    db_contact = get_emergency_contact_by_user_id(db, user_id)
    if not db_contact:
        return None

    update_data = contact_update.model_dump(exclude_unset=True)
    
    # Map relationship field to contact_relationship column
    if "relationship" in update_data:
        update_data["contact_relationship"] = update_data.pop("relationship")

    for field, value in update_data.items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_emergency_contact(db: Session, user_id: int) -> bool:
    """Delete emergency contact"""
    db_contact = get_emergency_contact_by_user_id(db, user_id)
    if not db_contact:
        return False

    db.delete(db_contact)
    db.commit()
    return True
