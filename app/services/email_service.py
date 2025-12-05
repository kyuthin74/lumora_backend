import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Send email using SMTP
    Returns True if successful, False otherwise
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("Email credentials not configured")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL or settings.SMTP_USER}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add plain text part
        text_part = MIMEText(body, "plain")
        message.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True
        )
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


async def send_alert_email(
    to_email: str,
    user_name: str,
    risk_level: str,
    risk_score: float,
    recommendation: str
) -> bool:
    """Send alert email for high-risk detection"""
    subject = f"Mental Health Alert - {risk_level} Risk Detected"
    
    body = f"""
Dear {user_name},

This is an automated alert from Lumora Mental Health App.

Risk Assessment:
- Risk Level: {risk_level}
- Risk Score: {risk_score:.2%}

{recommendation}

If you are in crisis or having thoughts of self-harm, please:
- Call the National Suicide Prevention Lifeline: 988
- Text "HELLO" to 741741 (Crisis Text Line)
- Go to your nearest emergency room

Please take care of yourself and reach out for support.

Best regards,
Lumora Mental Health Team

---
This is an automated message. Please do not reply to this email.
"""
    
    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #d32f2f;">Mental Health Alert</h2>
    
    <p>Dear <strong>{user_name}</strong>,</p>
    
    <p>This is an automated alert from Lumora Mental Health App.</p>
    
    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
        <h3 style="margin-top: 0;">Risk Assessment:</h3>
        <ul style="margin-bottom: 0;">
            <li><strong>Risk Level:</strong> <span style="color: #d32f2f;">{risk_level}</span></li>
            <li><strong>Risk Score:</strong> {risk_score:.2%}</li>
        </ul>
    </div>
    
    <div style="background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0;">
        <p style="margin: 0;"><strong>Recommendation:</strong></p>
        <p style="margin: 10px 0 0 0;">{recommendation}</p>
    </div>
    
    <div style="background-color: #ffebee; padding: 15px; border-left: 4px solid #f44336; margin: 20px 0;">
        <p style="margin: 0;"><strong>Crisis Resources:</strong></p>
        <ul style="margin: 10px 0 0 0;">
            <li>National Suicide Prevention Lifeline: <strong>988</strong></li>
            <li>Crisis Text Line: Text <strong>"HELLO"</strong> to <strong>741741</strong></li>
            <li>Emergency: Go to your nearest emergency room</li>
        </ul>
    </div>
    
    <p>Please take care of yourself and reach out for support.</p>
    
    <p>Best regards,<br><strong>Lumora Mental Health Team</strong></p>
    
    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
    <p style="font-size: 12px; color: #666;">
        This is an automated message. Please do not reply to this email.
    </p>
</body>
</html>
"""
    
    return await send_email(to_email, subject, body, html_body)


async def send_welcome_email(to_email: str, user_name: str) -> bool:
    """Send welcome email to new users"""
    subject = "Welcome to Lumora Mental Health App"
    
    body = f"""
Dear {user_name},

Welcome to Lumora Mental Health App!

We're glad you've joined us on your mental wellness journey. Our app is designed to help you:
- Track your daily mood and well-being
- Monitor patterns in your mental health
- Get personalized insights and recommendations
- Access support when you need it

Getting Started:
1. Complete your daily mood check-ins
2. Review your mental health trends
3. Use our AI chatbot for support and guidance
4. Set reminders to maintain consistency

Remember, taking care of your mental health is a sign of strength.

Best regards,
Lumora Mental Health Team
"""
    
    return await send_email(to_email, subject, body)
