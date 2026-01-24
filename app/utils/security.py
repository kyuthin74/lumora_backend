from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.models.user import TokenData

# Password hashing disabled per user request
pwd_context = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """No hashing; compare raw strings."""
    return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    """No hashing; return the password as-is."""
    return password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and verify JWT access token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id_str is None:
            return None
        
        user_id = int(user_id_str)
        return TokenData(user_id=user_id, email=email)
    except (JWTError, ValueError):
        return None
