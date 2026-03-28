import os
import smtplib
import datetime
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Load from .env
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
ESCALATION_EMAIL = os.getenv("ESCALATION_EMAIL")

def generate_ticket_id():
    date_part = datetime.datetime.now().strftime("%Y%m%d")
    unique_part = uuid.uuid4().hex[:6].upper()
    return f"TKT-{date_part}-{unique_part}"

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
    ticket_id = generate_ticket_id()   # 🔥 ADD THIS

    subject = f"[{ticket_id}] Escalation: Unresolved IT Issue"

    body = f"""
Hello IT Support Team,

Ticket ID: {ticket_id}

Issue:
"{issue}"

Please investigate and resolve.

Regards,
AI Support System
"""

    success = send_email(
        to_email=ESCALATION_EMAIL,
        subject=subject,
        body=body
    )

    return {
        "content": f"📧 Ticket {ticket_id} created and sent to IT support."
        if success else "⚠️ Failed to send email."
    }