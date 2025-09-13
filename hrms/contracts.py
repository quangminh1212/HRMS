from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models import Contract, Person
from .excel_utils import prepare_workbook_with_template, style_header, auto_filter_and_width, set_date_format, set_header_footer


def add_contract(db: Session, person: Person, contract_type: str, start_date: date, end_date: Optional[date] = None, note: Optional[str] = None) -> Contract:
    c = Contract(person_id=person.id, contract_type=contract_type, start_date=start_date, end_date=end_date, note=note)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def export_contracts_for_person(db: Session, person: Person, path: str, template_name: Optional[str] = None, username: Optional[str] = None) -> None:
    from typing import Optional
    rows = db.query(Contract).filter(Contract.person_id == person.id).order_by(Contract.start_date).all()

    headers = ["Loại HĐ", "Từ ngày", "Đến ngày", "Ghi chú"]
    wb, ws = prepare_workbook_with_template(template_name=(template_name or 'contracts.xlsx'), title='Hop dong', headers=headers)

    for r in rows:
        ws.append([r.contract_type, r.start_date, r.end_date, r.note or ""])

    style_header(ws, header_row=1)
    from .settings_service import get_setting
    date_fmt = get_setting('XLSX_DATE_FORMAT', 'DD/MM/YYYY') or 'DD/MM/YYYY'
    set_date_format(ws, date_columns=[2,3], start_row=2, fmt=date_fmt)
    auto_filter_and_width(ws, header_row=1)
    org = get_setting('ORG_NAME', None)
    set_header_footer(ws, title=f"Hợp đồng - {person.full_name}", username=username, org=org)
    # Freeze theo cấu hình
    try:
        from openpyxl.utils import column_index_from_string
        letter = get_setting('XLSX_FREEZE_COL:contracts', None) or get_setting('XLSX_FREEZE_COL:GLOBAL', None) or 'A'
        col = column_index_from_string(letter.strip().upper())
        from .excel_utils import set_freeze
        set_freeze(ws, row=2, col=col)
    except Exception:
        pass

    wb.save(path)


def export_contracts_expiring_to_excel(db: Session, start_date: date, end_date: date, path: str, unit_id: Optional[int] = None) -> None:
    """Xuất danh sách hợp đồng có end_date trong khoảng [start_date, end_date]."""
    from .settings_service import get_setting
    headers = ["Mã NV", "Họ tên", "Loại HĐ", "Từ ngày", "Đến ngày", "Ghi chú", "Còn lại (ngày)"]
    wb, ws = prepare_workbook_with_template(template_name='contracts_expiring.xlsx', title='HD sap het han', headers=headers)
    q = (
        db.query(Contract, Person)
        .join(Person, Person.id == Contract.person_id)
        .filter(Contract.end_date != None)
        .filter(Contract.end_date >= start_date, Contract.end_date <= end_date)
    )
    if unit_id:
        q = q.filter(Person.unit_id == unit_id)
    rows = q.order_by(Contract.end_date).all()
    for c, p in rows:
        days_left = (c.end_date - start_date).days if c.end_date else ''
        ws.append([p.code or '', p.full_name or '', c.contract_type, c.start_date, c.end_date, c.note or '', days_left])
    style_header(ws, header_row=1)
    date_fmt = get_setting('XLSX_DATE_FORMAT', 'DD/MM/YYYY') or 'DD/MM/YYYY'
    set_date_format(ws, date_columns=[4,5], start_row=2, fmt=date_fmt)
    auto_filter_and_width(ws, header_row=1)
    org = get_setting('ORG_NAME', None)
    set_header_footer(ws, title='Hợp đồng sắp hết hạn', org=org)
    wb.save(path)
