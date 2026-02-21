from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from app.services.email_service import send_forgot_password_email, send_emergency_contact_alert, generate_reset_code
from app.services.code_store import (
    set_code,
    get_code,
    delete_code,
    mark_code_verified,
    is_code_verified,
)
from app.api.auth import get_current_user
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email
from app.database import get_db
from app.utils.security import get_password_hash

router = APIRouter(prefix="/email", tags=["Email"])

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class EmergencyContactAlertRequest(BaseModel):
    email: EmailStr
    user_name: str
    risk_level: str

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def send_forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    code = generate_reset_code()
    set_code(request.email, code)
    try:
        send_forgot_password_email(request.email, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
    # For testing/demo: return code in response. In production, do NOT return code!
    return {"detail": "Email sent", "code": code}

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6)


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: constr(min_length=8, max_length=100)

@router.post("/verify-code", status_code=status.HTTP_200_OK)
def verify_code(request: VerifyCodeRequest):
    stored_code = get_code(request.email)
    if not stored_code:
        return {"success": False, "reason": "Code expired or not found"}
    if request.code == stored_code:
        mark_code_verified(request.email)
        return {"success": True}
    else:
        return {"success": False, "reason": "Invalid code"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    if not is_code_verified(request.email):
        raise HTTPException(status_code=400, detail="Email code not verified")

    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    delete_code(request.email)

    return {"detail": "Password reset successful"}

@router.post("/emergency-contact-alert", status_code=status.HTTP_204_NO_CONTENT)
def send_emergency_contact_alert_api(request: EmergencyContactAlertRequest, current_user=Depends(get_current_user)):
    try:
        send_emergency_contact_alert(request.email, request.user_name, request.risk_level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
    return None
