from email.message import EmailMessage
import smtplib
from typing import List

from .config import load_settings
try:
    from .settings_service import get_setting as _get_setting
except Exception:
    _get_setting = None


def _apply_subject_prefix(subject: str) -> str:
    try:
        if _get_setting:
            prefix = _get_setting('EMAIL_SUBJECT_PREFIX', '') or ''
            if prefix:
                return f"{prefix} {subject}"
    except Exception:
        pass
    return subject


def send_alert(subject: str, body: str, to: List[str] | None = None) -> bool:
    settings = load_settings()
    recipients = to or settings.alert_emails or []
    if not settings.smtp_host or not recipients:
        return False
    msg = EmailMessage()
    msg["Subject"] = _apply_subject_prefix(subject)
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


def send_email_with_attachment(subject: str, body: str, attachments: List[str], to: List[str] | None = None) -> bool:
    settings = load_settings()
    recipients = to or settings.alert_emails or []
    if not settings.smtp_host or not recipients:
        return False
    msg = EmailMessage()
    msg["Subject"] = _apply_subject_prefix(subject)
    msg["From"] = settings.smtp_user or "no-reply@example.com"
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)
    # Đính kèm các tệp
    for path in attachments or []:
        try:
            with open(path, "rb") as f:
                data = f.read()
            # đoán MIME cho xlsx/docx cơ bản
            if path.lower().endswith(".xlsx"):
                maintype = "application"; subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif path.lower().endswith(".docx"):
                maintype = "application"; subtype = "vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                maintype = "application"; subtype = "octet-stream"
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.split("\\")[-1].split("/")[-1])
        except Exception:
            # bỏ qua tệp lỗi
            continue
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port or 25) as server:
            server.starttls()
            if settings.smtp_user and settings.smtp_password:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        return True
    except Exception:
        return False
