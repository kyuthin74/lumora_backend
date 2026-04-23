from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message schema"""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=5000)
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[ChatMessage]] = None
    context: Optional[dict] = None  # Additional context like recent mood, risk level


class ChatResponse(BaseModel):
    """Chat response schema"""
    message: str
    timestamp: datetime
    suggestions: Optional[List[str]] = None  # Suggested follow-up questions or actions
    

class ConversationContext(BaseModel):
    """Context for chatbot conversation"""
    user_id: int
    recent_mood_level: Optional[str] = None
    recent_risk_score: Optional[float] = None
    total_entries: int = 0
    average_mood: Optional[float] = None


class FrontendChatBootstrapResponse(BaseModel):
    """Initial chatbot payload for frontend chat screen."""
    session_id: str
    welcome_message: str
    suggestions: List[str]
    context_summary: Optional[dict] = None


class FrontendChatMessageRequest(BaseModel):
    """Frontend message payload."""
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    conversation_history: Optional[List[ChatMessage]] = None


class FrontendChatMessageResponse(BaseModel):
    """Frontend structured message response."""
    session_id: str
    user_message: ChatMessage
    assistant_message: ChatMessage
    suggestions: List[str] = []
