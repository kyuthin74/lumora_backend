from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.depression_risk_result import EmergencyAlertRequest
from app.crud import emergency_contact as contact_crud
from app.crud.user import get_user_by_id
from app.api.auth import get_current_user
from app.services.email_service import send_emergency_contact_alert

router = APIRouter(prefix="/emergency-alert", tags=["Emergency Alert"])


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_emergency_alert(
    request: EmergencyAlertRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Send an emergency alert to the user's emergency contact.
    
    Args:
        request: Emergency alert request with user_id and alert_type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    # Check if current user has permission to send alert for this user
    if current_user.id != request.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to send an alert for this user"
        )
    
    # Get the user
    user = get_user_by_id(db, request.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {request.user_id} not found"
        )
    
    # Get the user's emergency contact
    emergency_contact = contact_crud.get_emergency_contact_by_user_id(db, request.user_id)
    if not emergency_contact:
        raise HTTPException(
            status_code=404,
            detail="No emergency contact found for this user"
        )
    
    if not emergency_contact.contact_email:
        raise HTTPException(
            status_code=400,
            detail="Emergency contact has no email address"
        )
    
    # Send the alert email
    try:
        send_emergency_contact_alert(
            to_email=emergency_contact.contact_email,
            user_name=user.full_name or user.email,
            risk_level=request.alert_type,
            contact_name=emergency_contact.contact_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send emergency alert: {str(e)}"
        )
    
    return {"detail": "Emergency alert sent successfully"}
