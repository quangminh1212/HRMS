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
    from openpyxl import Workbook
    rows = db.query(Contract).filter(Contract.person_id == person.id).order_by(Contract.start_date).all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Hop dong"
    ws.append(["Loại HĐ", "Từ ngày", "Đến ngày", "Ghi chú"])
    for r in rows:
        ws.append([r.contract_type, r.start_date, r.end_date, r.note or ""])
    wb.save(path)
