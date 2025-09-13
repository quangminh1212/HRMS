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


def export_contracts_for_person(db: Session, person: Person, path: str, template_name: Optional[str] = None) -> None:
    from typing import Optional
    from .excel_utils import prepare_workbook_with_template, style_header, auto_filter_and_width, set_date_format
    rows = db.query(Contract).filter(Contract.person_id == person.id).order_by(Contract.start_date).all()

    headers = ["Loại HĐ", "Từ ngày", "Đến ngày", "Ghi chú"]
    wb, ws = prepare_workbook_with_template(template_name=(template_name or 'contracts.xlsx'), title='Hop dong', headers=headers)

    for r in rows:
        ws.append([r.contract_type, r.start_date, r.end_date, r.note or ""])

    style_header(ws, header_row=1)
    set_date_format(ws, date_columns=[2,3], start_row=2)
    auto_filter_and_width(ws, header_row=1)
    from .excel_utils import set_header_footer, set_freeze
    from .settings_service import get_setting
    org = get_setting('ORG_NAME', None)
    set_header_footer(ws, title=f"Hợp đồng - {person.full_name}", org=org)
    # Freeze theo cấu hình
    try:
        from openpyxl.utils import column_index_from_string
        letter = get_setting('XLSX_FREEZE_COL:contracts', None) or get_setting('XLSX_FREEZE_COL:GLOBAL', None) or 'A'
        col = column_index_from_string(letter.strip().upper())
        set_freeze(ws, row=2, col=col)
    except Exception:
        pass

    wb.save(path)
