"""Pydantic schemas for API request/response validation"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    TokenData
)
from app.schemas.emergency_contact import (
    EmergencyContactBase,
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse,
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
