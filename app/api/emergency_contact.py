from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.emergency_contact import (
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse,
)
from app.crud import emergency_contact as contact_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/emergency-contact", tags=["Emergency Contact"])


@router.get("/", response_model=EmergencyContactResponse)
async def get_emergency_contact(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get emergency contact for current user"""
    contact = contact_crud.get_emergency_contact_by_user_id(db, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found",
        )
    return contact


@router.post("/", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency_contact(
    contact: EmergencyContactUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an emergency contact for current user"""
    existing = contact_crud.get_emergency_contact_by_user_id(db, user_id=current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency contact already exists. Use PUT to update.",
        )

    contact_create = EmergencyContactCreate(
        user_id=current_user.id,
        contact_name=contact.contact_name,
        contact_email=contact.contact_email,
        relationship=contact.relationship,
    )
    return contact_crud.create_emergency_contact(db, contact=contact_create)


@router.put("/", response_model=EmergencyContactResponse)
async def update_emergency_contact(
    contact_update: EmergencyContactUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update emergency contact for current user"""
    updated = contact_crud.update_emergency_contact(
        db, user_id=current_user.id, contact_update=contact_update
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found",
        )
    return updated


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emergency_contact(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete emergency contact for current user"""
    success = contact_crud.delete_emergency_contact(db, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found",
        )
    return None
