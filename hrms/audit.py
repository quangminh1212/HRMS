from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .models import AuditLog


def log_action(db: Session, user_id: Optional[int], action: str, entity: str, entity_id: Optional[int] = None, details: Optional[str] = None) -> None:
    log = AuditLog(user_id=user_id, action=action, entity=entity, entity_id=entity_id, timestamp=datetime.utcnow(), details=details)
    db.add(log)
    db.commit()
