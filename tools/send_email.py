import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Load from .env
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        return True

    except Exception as e:
        print("❌ Error sending email:", str(e))
        return False


def escalate_ticket_with_email(issue: str) -> dict:
    subject = "Escalation: Unresolved IT Issue"

    body = f"""
Hello IT Support Team,

The following issue reported by a user could not be resolved by the AI Assistant:

"{issue}"

Please investigate and take further action.

Regards,  
AI Notification Agent
"""

    success = send_email(
        to_email=SENDER_EMAIL,  # send to yourself or IT team
        subject=subject,
        body=body
    )

    return {
        "content": "📧 Email sent to IT support." if success else "⚠️ Failed to send email."
    }