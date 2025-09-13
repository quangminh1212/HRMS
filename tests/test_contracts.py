import pytest
from datetime import date

from hrms.db import SessionLocal
from hrms.models import Person
from hrms.contracts import add_contract, export_contracts_for_person

def test_contracts_add_and_export(tmp_path):
    db = SessionLocal()
    try:
        p = db.query(Person).first()
        c = add_contract(db, p, "HĐ xác định thời hạn", date.today())
        out = tmp_path / f"contracts_{p.code}.xlsx"
        export_contracts_for_person(db, p, str(out))
        assert out.exists()
        assert out.stat().st_size > 0
    finally:
        db.close()
