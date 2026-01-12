from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.alert import Alert
from app.crud import alert as alert_crud
from app.api.auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=List[dict])
async def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    unread_only: bool = Query(False),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all alerts for current user"""
    alerts = alert_crud.get_user_alerts(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    return alerts


@router.get("/unread-count", response_model=dict)
async def get_unread_count(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread alerts"""
    count = alert_crud.get_unread_count(db, user_id=current_user.id)
    return {"unread_count": count}


@router.get("/{alert_id}", response_model=dict)
async def get_alert(
    alert_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific alert"""
    alert = alert_crud.get_alert_by_id(db, alert_id=alert_id, user_id=current_user.id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.patch("/{alert_id}/read", response_model=dict)
async def mark_alert_read(
    alert_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark alert as read"""
    alert = alert_crud.mark_alert_read(db, alert_id=alert_id, user_id=current_user.id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.patch("/{alert_id}/resolve", response_model=dict)
async def mark_alert_resolved(
    alert_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark alert as resolved"""
    alert = alert_crud.mark_alert_resolved(db, alert_id=alert_id, user_id=current_user.id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an alert"""
    success = alert_crud.delete_alert(db, alert_id=alert_id, user_id=current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return None
