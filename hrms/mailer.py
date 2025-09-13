from email.message import EmailMessage
import smtplib
from typing import List

from .config import load_settings


def send_alert(subject: str, body: str, to: List[str] | None = None) -> bool:
    settings = load_settings()
    recipients = to or settings.alert_emails or []
    if not settings.smtp_host or not recipients:
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_user or "no-reply@example.com"
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port or 25) as server:
            server.starttls()
            if settings.smtp_user and settings.smtp_password:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        return True
    except Exception:
        return False
