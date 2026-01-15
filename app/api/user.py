from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserResponse, UserUpdate, UserCreate
from app.crud import user as user_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account (JSON body: full_name, email, password, optional emergency contact prefs)."""
    existing_user = user_crud.get_user_by_email(db, email=payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    created = user_crud.create_user(db, user=payload)
    return created


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user = Depends(get_current_user)):
    """Get user profile"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # Check if email is being changed and if it's already taken
    if user_update.email and user_update.email != current_user.email:
        existing_user = user_crud.get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    updated_user = user_crud.update_user(db, user_id=current_user.id, user_update=user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    success = user_crud.delete_user(db, user_id=current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return None
