from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(db: Session, user_id: int, notification: NotificationCreate) -> Notification:
    """Create a new notification for a user"""
    new_notification = Notification(
        user_id=user_id,
        type=notification.type,
        title=notification.title,
        message=notification.message
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    """Get all notifications for a user"""
    return db.query(Notification)\
        .filter(Notification.user_id == user_id)\
        .order_by(Notification.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_notification_by_id(db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
    """Get a specific notification by ID for a user"""
    return db.query(Notification)\
        .filter(Notification.id == notification_id, Notification.user_id == user_id)\
        .first()


def get_unread_notifications(db: Session, user_id: int) -> List[Notification]:
    """Get all unread notifications for a user"""
    return db.query(Notification)\
        .filter(Notification.user_id == user_id, Notification.is_read == False)\
        .order_by(Notification.created_at.desc())\
        .all()


def mark_notification_as_read(db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
    """Mark a notification as read"""
    notification = get_notification_by_id(db, notification_id, user_id)
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification


def mark_all_notifications_as_read(db: Session, user_id: int) -> int:
    """Mark all notifications as read for a user"""
    result = db.query(Notification)\
        .filter(Notification.user_id == user_id, Notification.is_read == False)\
        .update({"is_read": True})
    db.commit()
    return result


def delete_notification(db: Session, notification_id: int, user_id: int) -> bool:
    """Delete a specific notification"""
    notification = get_notification_by_id(db, notification_id, user_id)
    if notification:
        db.delete(notification)
        db.commit()
        return True
    return False


def delete_all_notifications(db: Session, user_id: int) -> int:
    """Delete all notifications for a user"""
    result = db.query(Notification)\
        .filter(Notification.user_id == user_id)\
        .delete()
    db.commit()
    return result
