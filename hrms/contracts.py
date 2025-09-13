from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models import Contract, Person


def add_contract(db: Session, person: Person, contract_type: str, start_date: date, end_date: Optional[date] = None, note: Optional[str] = None) -> Contract:
    c = Contract(person_id=person.id, contract_type=contract_type, start_date=start_date, end_date=end_date, note=note)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def export_contracts_for_person(db: Session, person: Person, path: str) -> None:
    from .excel_utils import prepare_workbook_with_template, style_header, auto_filter_and_width, set_date_format
    rows = db.query(Contract).filter(Contract.person_id == person.id).order_by(Contract.start_date).all()

    headers = ["Loại HĐ", "Từ ngày", "Đến ngày", "Ghi chú"]
    wb, ws = prepare_workbook_with_template(template_name='contracts.xlsx', title='Hop dong', headers=headers)

    for r in rows:
        ws.append([r.contract_type, r.start_date, r.end_date, r.note or ""])

    style_header(ws, header_row=1)
    set_date_format(ws, date_columns=[2,3], start_row=2)
    auto_filter_and_width(ws, header_row=1)

    wb.save(path)
