import pytest
from datetime import date

from hrms.db import SessionLocal
from hrms.models import Person, SalaryRank, SalaryStep, SalaryHistory
from hrms.salary import compute_next_for_person, export_salary_history_for_person
from hrms.init_db import init_db
from hrms.seed import seed_basic_data


def setup_module(module):
    init_db()
    seed_basic_data()


def test_compute_next_for_person_step_increase():
    db = SessionLocal()
    try:
        p = db.query(Person).filter_by(code="NV001").first()
        # NV001: CV step 1 effective 2022-01-01 -> as of 2025-02-01 exceeds 36 months
        info = compute_next_for_person(db, p, date(2025,2,1))
        assert info is not None
        assert info["type"] == "step"
        assert info["next_step"] == 2
    finally:
        db.close()


def test_compute_next_for_person_over_limit():
    db = SessionLocal()
    try:
        p = db.query(Person).filter_by(code="NV002").first()
        # NV002: NV step 3 (last) effective 2021-08-01 -> as of 2025-09-01 exceeds 24 months
        info = compute_next_for_person(db, p, date(2025,9,1))
        assert info is not None
        assert info["type"] == "over_limit"
        assert info["allowance_percent"] >= 5
    finally:
        db.close()


def test_export_salary_history(tmp_path):
    db = SessionLocal()
    try:
        p = db.query(Person).filter_by(code="NV001").first()
        out = tmp_path / f"salary_history_{p.code}.xlsx"
        export_salary_history_for_person(db, p, str(out))
        assert out.exists()
        assert out.stat().st_size > 0
    finally:
        db.close()


def test_export_salary_histories(tmp_path):
    db = SessionLocal()
    try:
        # Lấy 2 nhân sự bất kỳ
        people = db.query(Person).order_by(Person.id).limit(2).all()
        out = tmp_path / "salary_histories.xlsx"
        from hrms.salary import export_salary_histories_for_people
        export_salary_histories_for_people(db, people, str(out))
        assert out.exists()
        assert out.stat().st_size > 0
    finally:
        db.close()
