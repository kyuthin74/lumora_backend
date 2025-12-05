"""Pydantic models for request/response validation"""

from app.models.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    TokenData
)
from app.models.mood import (
    MoodLevel,
    SleepQuality,
    MoodEntryBase,
    MoodEntryCreate,
    MoodEntryUpdate,
    MoodEntryResponse,
    MoodStats
)
from app.models.depression_risk import (
    DepressionRiskInput,
    DepressionRiskResult,
    DepressionRiskResponse,
    RiskTrend
)
from app.models.chart import (
    ChartDataPoint,
    MoodChartData,
    ActivityChartData,
    RiskChartData,
    ComprehensiveChartData
)
from app.models.chatbot import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ConversationContext
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserLogin", "UserUpdate", "UserResponse", "Token", "TokenData",
    # Mood
    "MoodLevel", "SleepQuality", "MoodEntryBase", "MoodEntryCreate", "MoodEntryUpdate", 
    "MoodEntryResponse", "MoodStats",
    # Risk
    "DepressionRiskInput", "DepressionRiskResult", "DepressionRiskResponse", "RiskTrend",
    # Charts
    "ChartDataPoint", "MoodChartData", "ActivityChartData", "RiskChartData", "ComprehensiveChartData",
    # Chatbot
    "ChatMessage", "ChatRequest", "ChatResponse", "ConversationContext"
]
