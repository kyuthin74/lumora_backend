from sqlalchemy.orm import Session
from app.crud import alert as alert_crud
from app.schemas.user import User
from app.services.email_service import send_alert_email
from app.config import settings
from app.utils.helpers import format_alert_message
import logging

logger = logging.getLogger(__name__)


async def process_risk_alert(
    db: Session,
    user: User,
    risk_level: str,
    risk_score: float,
    recommendation: str
) -> bool:
    """
    Process a risk alert - create alert record and send email if needed
    Returns True if alert was processed successfully
    """
    try:
        # Determine if this warrants an alert based on risk level
        should_alert = risk_level in ["High", "Critical"]
        
        if not should_alert:
            return False
        
        # Determine severity
        if risk_score >= 0.9:
            severity = "critical"
        elif risk_score >= 0.7:
            severity = "high"
        else:
            severity = "medium"
        
        # Create alert message
        message = format_alert_message(risk_level, risk_score, user.full_name)
        
        # Create alert in database
        alert = alert_crud.create_alert(
            db=db,
            user_id=user.id,
            alert_type="high_risk",
            severity=severity,
            message=message
        )
        
        # Send email if enabled and configured
        if settings.ALERT_EMAIL_ENABLED and user.email:
            email_sent = await send_alert_email(
                to_email=user.email,
                user_name=user.full_name,
                risk_level=risk_level,
                risk_score=risk_score,
                recommendation=recommendation
            )
            
            if email_sent:
                alert_crud.mark_email_sent(db, alert.id)
                logger.info(f"Alert email sent to user {user.id}")
            else:
                logger.warning(f"Failed to send alert email to user {user.id}")
        
        logger.info(f"Risk alert processed for user {user.id}: {risk_level} ({risk_score:.2f})")
        return True
        
    except Exception as e:
        logger.error(f"Error processing risk alert for user {user.id}: {str(e)}")
        return False


def check_alert_threshold(risk_score: float) -> bool:
    """Check if risk score exceeds alert threshold"""
    return risk_score >= settings.HIGH_RISK_THRESHOLD


async def send_critical_alert(db: Session, user: User, message: str) -> bool:
    """Send critical alert (highest priority)"""
    try:
        # Create critical alert
        alert = alert_crud.create_alert(
            db=db,
            user_id=user.id,
            alert_type="critical",
            severity="critical",
            message=message
        )
        
        # Always send email for critical alerts if email is configured
        if user.email and settings.SMTP_USER:
            email_sent = await send_alert_email(
                to_email=user.email,
                user_name=user.full_name,
                risk_level="Critical",
                risk_score=1.0,
                recommendation=message
            )
            
            if email_sent:
                alert_crud.mark_email_sent(db, alert.id)
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending critical alert: {str(e)}")
        return False
