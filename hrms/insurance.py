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


def export_insurance_to_excel(db: Session, start_date: date, end_date: date, path: str, template_name: Optional[str] = None, username: Optional[str] = None) -> None:
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
    from .settings_service import get_setting
    date_fmt = get_setting('XLSX_DATE_FORMAT', 'DD/MM/YYYY') or 'DD/MM/YYYY'
    set_date_format(ws, date_columns=[4], start_row=2, fmt=date_fmt)
    auto_filter_and_width(ws, header_row=1)
    from .excel_utils import set_header_footer, set_freeze
    org = get_setting('ORG_NAME', None)
    set_header_footer(ws, title='Danh sách sự kiện BHXH', username=username, org=org)
    # Freeze theo cấu hình
    try:
        from openpyxl.utils import column_index_from_string
        letter = get_setting('XLSX_FREEZE_COL:bhxh', None) or get_setting('XLSX_FREEZE_COL:GLOBAL', None) or 'A'
        col = column_index_from_string(letter.strip().upper())
        set_freeze(ws, row=2, col=col)
    except Exception:
        pass

    wb.save(path)
