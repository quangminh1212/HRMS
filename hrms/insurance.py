from datetime import date
from typing import Dict, Any, List, Optional

from sqlalchemy.orm import Session

from .models import InsuranceEvent, Person


def add_insurance_event(db: Session, person: Person, event_type: str, event_date: date, details: str | None = None) -> InsuranceEvent:
    ev = InsuranceEvent(person_id=person.id, event_type=event_type, event_date=event_date, details=details)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


def export_insurance_to_excel(db: Session, start_date: date, end_date: date, path: str, template_name: Optional[str] = None) -> None:
    from typing import Optional
    from .excel_utils import prepare_workbook_with_template, style_header, auto_filter_and_width, set_date_format

    q = db.query(InsuranceEvent).filter(InsuranceEvent.event_date >= start_date, InsuranceEvent.event_date <= end_date)
    rows = q.all()

    headers = ["Mã NV", "Họ tên", "Loại sự kiện", "Ngày", "Ghi chú"]
    wb, ws = prepare_workbook_with_template(template_name=(template_name or 'bhxh.xlsx'), title='BHXH', headers=headers)

    # Ghi dữ liệu
    for r in rows:
        p = db.get(Person, r.person_id)
        ws.append([p.code if p else "", p.full_name if p else "", r.event_type, r.event_date, r.details or ""])

    # Định dạng chung
    style_header(ws, header_row=1)
    set_date_format(ws, date_columns=[4], start_row=2)
    auto_filter_and_width(ws, header_row=1)

    wb.save(path)
