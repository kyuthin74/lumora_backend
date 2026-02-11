from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserResponse, UserUpdate, UserProfileResponse, EmergencyContactInfo
from app.crud import user as user_crud
from app.crud import emergency_contact as emergency_contact_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user profile with emergency contact by user ID"""
    # Get user
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get emergency contact
    emergency_contact = emergency_contact_crud.get_emergency_contact_by_user_id(db, user_id)
    
    emergency_contact_info = None
    if emergency_contact:
        emergency_contact_info = EmergencyContactInfo(
            contact_name=emergency_contact.contact_name,
            contact_email=emergency_contact.contact_email,
            relationship=emergency_contact.contact_relationship
        )
    
    return UserProfileResponse(
        full_name=user.full_name,
        email=user.email,
        is_notify_enabled=user.is_notify_enabled,
        is_risk_alert_enabled=user.is_risk_alert_enabled,
        emergency_contact=emergency_contact_info
    )


@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_profile(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user profile by user ID"""
    # Get user first to check if exists and validate email change
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is being changed and if it's already taken
    if user_update.email and user_update.email != user.email:
        existing_user = user_crud.get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    updated_user = user_crud.update_user(db, user_id=user_id, user_update=user_update)
    
    return updated_user


@router.delete("/profile/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete user account and all related data (mood journals, depression tests, alerts, emergency contact)"""
    success = user_crud.delete_user(db, user_id=user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return None
