from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from app.models.chat_history import ChatHistory
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def _is_missing_chat_history_table(exc: Exception) -> bool:
    """Detect PostgreSQL undefined table errors for chat_history."""
    return 'relation "chat_history" does not exist' in str(exc)


def get_or_create_user_chat_history(db: Session, user_id: int) -> ChatHistory:
    """Get existing chat history for user or create if not exists"""
    try:
        chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()

        if not chat_history:
            chat_history = ChatHistory(user_id=user_id, messages=[])
            db.add(chat_history)
            db.commit()
            db.refresh(chat_history)

        return chat_history
    except ProgrammingError as exc:
        db.rollback()
        if _is_missing_chat_history_table(exc):
            logger.warning("chat_history table is missing; returning empty history placeholder")
            return ChatHistory(user_id=user_id, messages=[])
        raise


def get_user_chat_history(db: Session, user_id: int) -> Optional[ChatHistory]:
    """Get chat history for user"""
    try:
        return db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
    except ProgrammingError as exc:
        db.rollback()
        if _is_missing_chat_history_table(exc):
            logger.warning("chat_history table is missing; returning no history")
            return None
        raise


def update_chat_history(db: Session, user_id: int, messages: List[Dict[str, Any]]) -> Optional[ChatHistory]:
    """Update chat history with new messages"""
    try:
        chat_history = get_or_create_user_chat_history(db, user_id)
        if chat_history is None:
            return None
        chat_history.messages = messages
        chat_history.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(chat_history)
        return chat_history
    except ProgrammingError as exc:
        db.rollback()
        if _is_missing_chat_history_table(exc):
            logger.warning("chat_history table is missing; skipping history update")
            return None
        raise


def append_to_chat_history(db: Session, user_id: int, new_messages: List[Dict[str, Any]]) -> Optional[ChatHistory]:
    """Append new messages to existing chat history"""
    try:
        chat_history = get_or_create_user_chat_history(db, user_id)
        if chat_history is None:
            return None

        # Ensure messages is a list
        if not isinstance(chat_history.messages, list):
            chat_history.messages = []

        # Append new messages
        chat_history.messages.extend(new_messages)
        chat_history.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(chat_history)
        return chat_history
    except ProgrammingError as exc:
        db.rollback()
        if _is_missing_chat_history_table(exc):
            logger.warning("chat_history table is missing; skipping history append")
            return None
        raise


def clear_chat_history(db: Session, user_id: int) -> Optional[ChatHistory]:
    """Clear all messages from user's chat history"""
    try:
        chat_history = get_user_chat_history(db, user_id)

        if chat_history:
            chat_history.messages = []
            chat_history.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(chat_history)

        return chat_history
    except ProgrammingError as exc:
        db.rollback()
        if _is_missing_chat_history_table(exc):
            logger.warning("chat_history table is missing; skipping history clear")
            return None
        raise
