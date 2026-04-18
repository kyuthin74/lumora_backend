from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.schemas.push_notification import (
    PushNotificationStatusResponse,
    PushPreferenceUpdateRequest,
    PushTokenRegisterRequest,
)

router = APIRouter(prefix="/push-notifications", tags=["Push Notifications"])


@router.post("/register-token", response_model=PushNotificationStatusResponse)
def register_device_token(
    payload: PushTokenRegisterRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.fcm_token = payload.fcm_token
    current_user.is_push_reminder_enabled = True
    db.commit()
    db.refresh(current_user)

    return PushNotificationStatusResponse(
        push_enabled=current_user.is_push_reminder_enabled,
        token_registered=bool(current_user.fcm_token),
    )


@router.patch("/preferences", response_model=PushNotificationStatusResponse)
def update_push_preferences(
    payload: PushPreferenceUpdateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.is_push_reminder_enabled = payload.enabled
    db.commit()
    db.refresh(current_user)

    return PushNotificationStatusResponse(
        push_enabled=current_user.is_push_reminder_enabled,
        token_registered=bool(current_user.fcm_token),
    )


@router.delete("/token", response_model=PushNotificationStatusResponse)
def unregister_device_token(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.fcm_token = None
    db.commit()
    db.refresh(current_user)

    return PushNotificationStatusResponse(
        push_enabled=current_user.is_push_reminder_enabled,
        token_registered=False,
    )


@router.get("/status", response_model=PushNotificationStatusResponse)
def get_push_status(current_user=Depends(get_current_user)):
    return PushNotificationStatusResponse(
        push_enabled=current_user.is_push_reminder_enabled,
        token_registered=bool(current_user.fcm_token),
    )
