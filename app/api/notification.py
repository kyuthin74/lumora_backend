from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.crud.notification import (
    create_notification,
    get_notifications,
    mark_all_notifications_as_read,
    delete_notification,
    delete_all_notifications
)
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post("/", response_model=NotificationResponse)
def create_new_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Create a new notification for the current user
    """
    return create_notification(db, user_id=current_user.id, notification=notification)


@router.get("/", response_model=List[NotificationResponse])
def read_notifications(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get all notifications for the current user
    """
    return get_notifications(db, user_id=current_user.id, skip=skip, limit=limit)


@router.patch("/read-all", response_model=Dict[str, int])
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Mark all notifications as read for the current user
    """
    count = mark_all_notifications_as_read(db, user_id=current_user.id)
    return {"marked_as_read": count}


@router.delete("/{notification_id}", response_model=Dict[str, bool])
def delete_single_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Delete a specific notification
    """
    deleted = delete_notification(db, notification_id=notification_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"deleted": True}


@router.delete("/", response_model=Dict[str, int])
def delete_all_user_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Delete all notifications for the current user
    """
    count = delete_all_notifications(db, user_id=current_user.id)
    return {"deleted": count}
