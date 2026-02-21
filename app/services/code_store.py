# Simple in-memory code store for demo purposes
# In production, use Redis or a database with expiry

from typing import Dict, Optional
import time

_code_store: Dict[str, Dict[str, float]] = {}

CODE_EXPIRY_SECONDS = 10 * 60  # 10 minutes

def set_code(email: str, code: str):
    _code_store[email] = {"code": code, "timestamp": time.time(), "verified": 0.0}

def get_code(email: str) -> Optional[str]:
    entry = _code_store.get(email)
    if not entry:
        return None
    # Check expiry
    if time.time() - entry["timestamp"] > CODE_EXPIRY_SECONDS:
        del _code_store[email]
        return None
    return entry["code"]


def mark_code_verified(email: str) -> bool:
    entry = _code_store.get(email)
    if not entry:
        return False
    if time.time() - entry["timestamp"] > CODE_EXPIRY_SECONDS:
        del _code_store[email]
        return False
    entry["verified"] = 1.0
    return True


def is_code_verified(email: str) -> bool:
    entry = _code_store.get(email)
    if not entry:
        return False
    if time.time() - entry["timestamp"] > CODE_EXPIRY_SECONDS:
        del _code_store[email]
        return False
    return bool(entry.get("verified", 0.0))

def delete_code(email: str):
    _code_store.pop(email, None)
