from email.message import EmailMessage
import smtplib
from typing import List
import zipfile
import os

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


def _shorten_recipients(recipients: List[str]) -> str:
    try:
        # Ẩn phần tên người dùng, chỉ hiện domain để không lộ thông tin đầy đủ
        masked = []
        for r in recipients or []:
            r = str(r or '').strip()
            if '@' in r:
                user, dom = r.split('@', 1)
                masked.append(f"***@{dom}")
            elif r:
                masked.append("***")
        return ", ".join(masked)
    except Exception:
        return ", ".join(recipients or [])


def get_recipients_for_unit(unit_name: str) -> List[str]:
    """Trả về danh sách email cho đơn vị.
    Ưu tiên DB (unit_email_recipients.active=True), fallback settings. Lọc trùng và định dạng cơ bản.
    """
    def _normalize(emails: List[str]) -> List[str]:
        seen = set(); out = []
        import re
        pat = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        for e in emails or []:
            e = (e or '').strip()
            if not e or not pat.match(e):
                continue
            if e.lower() in seen:
                continue
            seen.add(e.lower()); out.append(e)
        return out
    try:
        # Ưu tiên DB
        from .db import SessionLocal
        from .models import Unit, UnitEmailRecipient
        s = SessionLocal()
        try:
            u = s.query(Unit).filter(Unit.name.ilike(unit_name)).first()
            if u:
                emails = [r.email.strip() for r in s.query(UnitEmailRecipient).filter(UnitEmailRecipient.unit_id == u.id, UnitEmailRecipient.active == True).all() if (r.email or '').strip()]
                emails = _normalize(emails)
                if emails:
                    return emails
        finally:
            s.close()
    except Exception:
        pass
    # Fallback settings
    try:
        if not _get_setting:
            return []
        raw = _get_setting('UNIT_EMAILS', '') or ''
        if not raw.strip():
            return []
        mapping: dict[str, list[str]] = {}
        # Thử JSON trước
        try:
            import json
            obj = json.loads(raw)
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, list):
                        emails = [str(x).strip() for x in v if str(x).strip()]
                    else:
                        emails = [e.strip() for e in str(v).split(',') if e.strip()]
                    if emails:
                        mapping[str(k).strip()] = emails
        except Exception:
            # Fallback parse dạng chuỗi
            parts = [p for p in raw.split(';') if p.strip()]
            for p in parts:
                if '=' in p:
                    name, emails = p.split('=', 1)
                    vals = [e.strip() for e in emails.split(',') if e.strip()]
                    if vals:
                        mapping[name.strip()] = vals
        if not mapping:
            return []
        def _norm(x: str) -> str:
            return (x or '').strip().lower()
        # Ưu tiên khớp chính xác
        if unit_name in mapping:
            return _normalize(mapping[unit_name])
        # Khớp không phân biệt hoa thường
        target = _norm(unit_name)
        for k, v in mapping.items():
            if _norm(k) == target:
                return _normalize(v)
        return []
    except Exception:
        return []


def send_email_with_attachment(subject: str, body: str, attachments: List[str], to: List[str] | None = None, *, suppress_log: bool = False) -> bool:
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
        # Ghi EmailLog (best-effort)
        if not suppress_log:
            try:
                from .db import SessionLocal
                from .models import EmailLog
                s = SessionLocal()
                log = EmailLog(
                    type="generic",
                    unit_name=None,
                    recipients=_shorten_recipients(to or settings.alert_emails or []),
                    subject=_apply_subject_prefix(subject),
                    body=(body or '')[:1000],
                    attachments=", ".join(attachments or [])[:2000],
                    status="sent",
                    error=None,
                    user_id=None,
                )
                s.add(log); s.commit(); s.close()
            except Exception:
                pass
        return True
    except Exception as ex:
        # Ghi log thất bại
        if not suppress_log:
            try:
                from .db import SessionLocal
                from .models import EmailLog
                s = SessionLocal()
                log = EmailLog(
                    type="generic",
                    unit_name=None,
                    recipients=_shorten_recipients(to or settings.alert_emails or []),
                    subject=_apply_subject_prefix(subject),
                    body=(body or '')[:1000],
                    attachments=", ".join(attachments or [])[:2000],
                    status="failed",
                    error=str(ex)[:500],
                    user_id=None,
                )
                s.add(log); s.commit(); s.close()
            except Exception:
                pass
        return False


def create_zip(files: list[str], out_zip: str) -> bool:
    try:
        with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                try:
                    if not f or not os.path.exists(f):
                        continue
                    zf.write(f, arcname=os.path.basename(f))
                except Exception:
                    continue
        return True
    except Exception:
        return False


def send_email_with_attachment_retry(subject: str, body: str, attachments: List[str], to: List[str] | None = None, *, retries: int = 2, delay: int = 10) -> bool:
    """Gửi email với retry. Chỉ ghi EmailLog cho lần cuối cùng (thành công/ thất bại)."""
    try:
        import time
    except Exception:
        time = None
    attempts = retries + 1 if retries and retries > 0 else 1
    for i in range(attempts):
        suppress = (i < attempts - 1)
        ok = send_email_with_attachment(subject, body, attachments, to=to, suppress_log=suppress)
        if ok:
            return True
        if i < attempts - 1 and time is not None and delay and delay > 0:
            try:
                time.sleep(delay)
            except Exception:
                pass
    return False
