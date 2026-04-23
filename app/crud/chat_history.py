from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory
from typing import Optional, List, Dict, Any
from datetime import datetime


def get_or_create_user_chat_history(db: Session, user_id: int) -> ChatHistory:
    """Get existing chat history for user or create if not exists"""
    chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()
    
    if not chat_history:
        chat_history = ChatHistory(user_id=user_id, messages=[])
        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)
    
    return chat_history


def get_user_chat_history(db: Session, user_id: int) -> Optional[ChatHistory]:
    """Get chat history for user"""
    return db.query(ChatHistory).filter(ChatHistory.user_id == user_id).first()


def update_chat_history(db: Session, user_id: int, messages: List[Dict[str, Any]]) -> Optional[ChatHistory]:
    """Update chat history with new messages"""
    chat_history = get_or_create_user_chat_history(db, user_id)
    chat_history.messages = messages
    chat_history.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chat_history)
    return chat_history


def append_to_chat_history(db: Session, user_id: int, new_messages: List[Dict[str, Any]]) -> Optional[ChatHistory]:
    """Append new messages to existing chat history"""
    chat_history = get_or_create_user_chat_history(db, user_id)
    
    # Ensure messages is a list
    if not isinstance(chat_history.messages, list):
        chat_history.messages = []
    
    # Append new messages
    chat_history.messages.extend(new_messages)
    chat_history.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chat_history)
    return chat_history


def clear_chat_history(db: Session, user_id: int) -> Optional[ChatHistory]:
    """Clear all messages from user's chat history"""
    chat_history = get_user_chat_history(db, user_id)
    
    if chat_history:
        chat_history.messages = []
        chat_history.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(chat_history)
    
    return chat_history
