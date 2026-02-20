"""Pydantic schemas for API request/response validation"""

# ---------- User ----------
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    TokenData,
)

# ---------- Emergency Contact ----------
from app.schemas.emergency_contact import (
    EmergencyContactBase,
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse,
)

# ---------- Mood ----------
# from app.models.mood import (
#     MoodEntryBase,
#     MoodEntryCreate,
#     MoodEntryUpdate,
#     MoodEntryResponse,
#     MoodStats,
#     MoodLevel,
#     SleepQuality,
# )

# ---------- Depression Test ----------
from app.schemas.depression_test import (
    DepressionTestCreate,
    DepressionTestResponse,
)

# ---------- Depression Risk Result (GET only) ----------
from app.schemas.depression_risk_result import (
    DepressionRiskResultResponse,
)



# ---------- Chatbot ----------
from app.models.chatbot import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ConversationContext,
)
