from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # App Info
    APP_NAME: str = "Lumora Mental Health API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    TIMEZONE: str = "UTC"
    
    # Database
    DATABASE_URL: str
    # For PostgreSQL: "postgresql://user:password@localhost/lumora_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # ML Models
    MODEL_PATH: str = "saved_models/logistic_model.pkl"
    ENCODERS_PATH: str = "saved_models/label_encoders.pkl"
    
    # Email Configuration
    SMTP_HOST: str = "smtp-relay.brevo.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = "a2f9bf001@smtp-brevo.com"
    SMTP_PASSWORD: Optional[str] = None  # Loaded from .env
    SMTP_FROM_EMAIL: Optional[str] = "lumorauserservice@gmail.com"
    SMTP_FROM_NAME: str = "Lumora Mental Health"
    
    # Alert Thresholds
    HIGH_RISK_THRESHOLD: float = 0.7  # Probability threshold for high risk
    ALERT_EMAIL_ENABLED: bool = False  # Enable/disable email alerts
    
    # Chatbot Configuration
    OPENAI_API_KEY: Optional[str] = None
    CHATBOT_MODEL: str = "gpt-3.5-turbo"
    CHATBOT_MAX_TOKENS: int = 500
    CHATBOT_TEMPERATURE: float = 0.7
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
