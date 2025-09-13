import pytest

from hrms.db import SessionLocal
from hrms.models import Person, JobPositionRequirement, WorkProcess
from hrms.appointment import check_appointment_eligibility
from datetime import date


def test_appointment_eligibility_basic():
    db = SessionLocal()
    try:
        p = db.query(Person).filter_by(code="NV001").first()
        # tạo yêu cầu tối thiểu: 1 năm kinh nghiệm
        if not db.query(JobPositionRequirement).filter_by(position_name="Trưởng phòng").first():
            db.add(JobPositionRequirement(position_name="Trưởng phòng", required_degree="Cử nhân", required_llct="Trung cấp", required_qlnn="Chuyên viên", min_years_experience=1))
            db.commit()
        # bổ sung thông tin bằng cấp/LLCT để đạt yêu cầu
        p.professional_level = "Cử nhân - Chuyên viên"
        p.llct_level = "Trung cấp"
        db.commit()
        # thêm quá trình công tác 2 năm
        db.add(WorkProcess(person_id=p.id, unit="Phòng Tổ chức", position="Chuyên viên", start_date=date(2022,1,1), end_date=date(2024,1,1)))
        db.commit()
        ok, reasons = check_appointment_eligibility(db, p, "Trưởng phòng")
        assert ok
        assert reasons == []
    finally:
        db.close()
