import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None


def validate_mood_level(level: int) -> bool:
    """Validate mood level (1-5)"""
    return 1 <= level <= 5


def validate_stress_level(level: int) -> bool:
    """Validate stress level (1-10)"""
    return 1 <= level <= 10


def validate_sleep_hours(hours: float) -> bool:
    """Validate sleep hours (0-24)"""
    return 0 <= hours <= 24


def validate_activity_minutes(minutes: int) -> bool:
    """Validate physical activity minutes (0-1440)"""
    return 0 <= minutes <= 1440


def validate_social_interaction(level: int) -> bool:
    """Validate social interaction level (1-5)"""
    return 1 <= level <= 5


def sanitize_text_input(text: str, max_length: int = 1000) -> str:
    """Sanitize text input by removing potentially harmful content"""
    if not text:
        return ""
    
    # Remove any script tags or HTML
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length
    text = text[:max_length]
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
