"""API route modules"""

from app.api import auth
from app.api import user
from app.api import mood
from app.api import alerts
from app.api import charts
from app.api import chatbot

__all__ = [
    "auth",
    "user",
    "mood",
    "alerts",
    "charts",
    "chatbot"
]
