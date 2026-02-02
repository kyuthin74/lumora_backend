"""API route modules"""

from app.api import auth
from app.api import user
from app.api import mood
from app.api import alerts
from app.api import charts
from app.api import chatbot
from app.api import depression_test
from app.api import depression_risk_result


__all__ = [
    "auth",
    "user",
    "mood",
    "alerts",
    "charts",
    "chatbot",
    "depression_test",
    "depression_risk_result"
]
