import logging
from typing import Dict, Optional

import firebase_admin
from firebase_admin import credentials, messaging

from app.config import settings

logger = logging.getLogger(__name__)


class PushSendResult:
    SENT = "sent"
    INVALID_TOKEN = "invalid_token"
    FAILED = "failed"


def _ensure_firebase_initialized() -> bool:
    if firebase_admin._apps:
        return True

    if not settings.FIREBASE_CREDENTIALS_PATH:
        logger.warning("Firebase credentials path is not configured")
        return False

    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        return True
    except Exception as exc:
        logger.error("Failed to initialize Firebase Admin SDK: %s", exc)
        return False


def send_push_notification(
    token: str,
    title: str,
    body: str,
    data: Optional[Dict[str, str]] = None,
) -> str:
    if not _ensure_firebase_initialized():
        return PushSendResult.FAILED

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
        data=data or {},
    )

    try:
        messaging.send(message)
        return PushSendResult.SENT
    except Exception as exc:
        error_text = str(exc).lower()
        if "unregistered" in error_text or "not a valid fcm registration token" in error_text:
            logger.warning("Invalid or unregistered FCM token")
            return PushSendResult.INVALID_TOKEN

        logger.error("Failed to send push notification: %s", exc)
        return PushSendResult.FAILED
