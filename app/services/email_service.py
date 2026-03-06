
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)

import random

def generate_reset_code() -> str:
        return f"{random.randint(100000, 999999)}"

def send_forgot_password_email(to_email: str, code: str):
        subject = "Password Reset Verification Code"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
            <div style="max-width: 480px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px 24px;">
                <h2 style="color: #1976d2; margin-bottom: 16px;">Password Reset Request</h2>
                <p style="font-size: 16px; color: #333;">We received a request to reset your password. Please use the code below to verify your request:</p>
                <div style="background: #1976d2; color: #fff; font-size: 2.2em; font-weight: bold; letter-spacing: 0.3em; text-align: center; border-radius: 8px; padding: 18px 0; margin: 24px 0;">
                    {code}
                </div>
                <p style="font-size: 15px; color: #333;">Enter this code in the app to continue with resetting your password.</p>
                <p style="font-size: 13px; color: #888;">If you did not request this, you can safely ignore this email.</p>
                <p style="font-size: 15px; color: #333; margin-top: 32px;">Best regards,<br>{settings.SMTP_FROM_NAME}</p>
            </div>
        </body>
        </html>
        """
        _send_email(to_email, subject, body, html=True)

def send_emergency_contact_alert(to_email: str, user_name: str, risk_level: str, contact_name: str = None):
    subject = f"Urgent: High Risk Wellbeing Alert for {user_name}"
    greeting = contact_name if contact_name else "Emergency Contact"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="background: #d32f2f; color: #fff; padding: 24px; text-align: center;">
                <h2 style="margin: 0; font-size: 20px;">⚠️ Urgent Wellbeing Alert</h2>
            </div>
            <div style="padding: 32px 24px;">
                <p style="font-size: 16px; color: #333; margin-bottom: 20px;">Dear {greeting},</p>
                
                <p style="font-size: 15px; color: #333; line-height: 1.6;">
                    This message is being sent to inform you of a wellbeing alert concerning <strong>{user_name}</strong>.
                </p>
                
                <div style="background: #ffebee; border-left: 4px solid #d32f2f; padding: 16px; margin: 24px 0; border-radius: 4px;">
                    <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.6;">
                        Based on recent assessment results in the {settings.SMTP_FROM_NAME} monitoring system, <strong>{user_name}</strong> has been identified as being at a <strong>high risk level</strong> over the past seven days.
                    </p>
                </div>
                
                <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
                    <p style="font-size: 15px; color: #333; margin: 0 0 12px 0; font-weight: bold;">
                        Recommended Action:
                    </p>
                    <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.6;">
                        We recommend that you check in with them as soon as possible to ensure their safety and wellbeing.
                    </p>
                </div>
                
                <p style="font-size: 15px; color: #333; line-height: 1.6;">
                    Your support and prompt attention may be very important at this time. Please consider contacting them directly or reaching out to appropriate support services if you believe additional assistance is required.
                </p>
                
                <p style="font-size: 15px; color: #333; line-height: 1.6;">
                    If you have any questions regarding this alert, please contact our support team.
                </p>
                
                <p style="font-size: 15px; color: #333; margin-top: 32px;">
                    Thank you for your understanding and cooperation.
                </p>
                
                <p style="font-size: 15px; color: #333; margin-top: 32px;">
                    Sincerely,<br>
                    <strong>{settings.SMTP_FROM_NAME} Support Team</strong>
                </p>
            </div>
            <div style="background: #f5f5f5; padding: 16px 24px; text-align: center; border-top: 1px solid #e0e0e0;">
                <p style="font-size: 13px; color: #666; margin: 0;">
                    This is an automated alert message for emergency contacts.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    _send_email(to_email, subject, body, html=True)


def _send_email(to_email: str, subject: str, body: str, html: bool = False):
    msg = MIMEMultipart()
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    if html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    try:
        logger.info(f"Connecting to SMTP server {settings.SMTP_HOST}:{settings.SMTP_PORT} as {settings.SMTP_USER}")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            logger.info(f"Sending email to {to_email} with subject '{subject}'")
            server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())
        logger.info("Email sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
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
