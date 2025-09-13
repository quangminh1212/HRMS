import pytest
from datetime import date

from hrms.db import SessionLocal
from hrms.reporting import compute_annual_summary, compute_demographics


def test_reporting_summary_and_demo():
    db = SessionLocal()
    try:
        s = compute_annual_summary(db, date.today().year)
        assert set(["year","salary_increase","retirement","appointment","maternity","studying","leaving"]).issubset(s.keys())
        d = compute_demographics(db, date.today())
        for k in ["age_buckets","ethnicity","gender","llct","professional"]:
            assert k in d
    finally:
        db.close()
