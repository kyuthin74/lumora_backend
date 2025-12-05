from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.schemas.alert import Alert
from typing import List, Optional
from datetime import datetime


def create_alert(
    db: Session,
    user_id: int,
    alert_type: str,
    severity: str,
    message: str
) -> Alert:
    """Create new alert"""
    db_alert = Alert(
        user_id=user_id,
        alert_type=alert_type,
        severity=severity,
        message=message
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alert_by_id(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
    """Get alert by ID"""
    return db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user_id
    ).first()


def get_user_alerts(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False
) -> List[Alert]:
    """Get all alerts for a user"""
    query = db.query(Alert).filter(Alert.user_id == user_id)
    
    if unread_only:
        query = query.filter(Alert.is_read == False)
    
    return query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()


def mark_alert_read(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
    """Mark alert as read"""
    db_alert = get_alert_by_id(db, alert_id, user_id)
    if not db_alert:
        return None
    
    db_alert.is_read = True
    db.commit()
    db.refresh(db_alert)
    return db_alert


def mark_alert_resolved(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
    """Mark alert as resolved"""
    db_alert = get_alert_by_id(db, alert_id, user_id)
    if not db_alert:
        return None
    
    db_alert.is_resolved = True
    db_alert.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert


def mark_email_sent(db: Session, alert_id: int) -> Optional[Alert]:
    """Mark that email notification was sent"""
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        return None
    
    db_alert.email_sent = True
    db_alert.email_sent_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert


def delete_alert(db: Session, alert_id: int, user_id: int) -> bool:
    """Delete alert"""
    db_alert = get_alert_by_id(db, alert_id, user_id)
    if not db_alert:
        return False
    
    db.delete(db_alert)
    db.commit()
    return True


def get_unread_count(db: Session, user_id: int) -> int:
    """Get count of unread alerts"""
    return db.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.is_read == False
    ).count()
