from datetime import date
from typing import Dict, Any, List

from sqlalchemy.orm import Session

from .models import InsuranceEvent, Person


def add_insurance_event(db: Session, person: Person, event_type: str, event_date: date, details: str | None = None) -> InsuranceEvent:
    ev = InsuranceEvent(person_id=person.id, event_type=event_type, event_date=event_date, details=details)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


def export_insurance_to_excel(db: Session, start_date: date, end_date: date, path: str) -> None:
    from openpyxl import Workbook

    q = db.query(InsuranceEvent).filter(InsuranceEvent.event_date >= start_date, InsuranceEvent.event_date <= end_date)
    rows = q.all()

    wb = Workbook()
    ws = wb.active
    ws.title = "BHXH"
    ws.append(["Mã NV", "Họ tên", "Loại sự kiện", "Ngày", "Ghi chú"])
    for r in rows:
        p = db.get(Person, r.person_id)
        ws.append([p.code if p else "", p.full_name if p else "", r.event_type, r.event_date, r.details or ""])
    wb.save(path)
