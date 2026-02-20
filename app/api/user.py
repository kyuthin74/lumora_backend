from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserResponse, UserUpdate, UserProfileResponse, EmergencyContactInfo
from app.crud import user as user_crud
from app.crud import emergency_contact as emergency_contact_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile with emergency contact"""
    # Get emergency contact
    emergency_contact = emergency_contact_crud.get_emergency_contact_by_user_id(db, current_user.id)
    
    emergency_contact_info = None
    if emergency_contact:
        emergency_contact_info = EmergencyContactInfo(
            contact_name=emergency_contact.contact_name,
            contact_email=emergency_contact.contact_email,
            relationship=emergency_contact.contact_relationship
        )
    
    return UserProfileResponse(
        full_name=current_user.full_name,
        email=current_user.email,
        is_notify_enabled=current_user.is_notify_enabled,
        is_risk_alert_enabled=current_user.is_risk_alert_enabled,
        emergency_contact=emergency_contact_info
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    # Check if email is being changed and if it's already taken
    if user_update.email and user_update.email != current_user.email:
        existing_user = user_crud.get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    updated_user = user_crud.update_user(db, user_id=current_user.id, user_update=user_update)
    
    return updated_user


@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user account and all related data (mood journals, depression tests, alerts, emergency contact)"""
    user_crud.delete_user(db, user_id=current_user.id)
    return None
