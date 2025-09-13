from datetime import date
from .db import SessionLocal
from .models import Unit, Position, Person, User, SalaryRank, SalaryStep, SalaryHistory
from .security import hash_password


def seed_basic_data():
    db = SessionLocal()
    try:
        # Units
        if not db.query(Unit).first():
            u1 = Unit(name="Văn phòng")
            u2 = Unit(name="Phòng Tổ chức")
            db.add_all([u1, u2])
            db.flush()
        else:
            u1 = db.query(Unit).filter_by(name="Văn phòng").first()
            u2 = db.query(Unit).filter_by(name="Phòng Tổ chức").first()

        # Positions
        if not db.query(Position).first():
            p1 = Position(name="Chuyên viên")
            p2 = Position(name="Trưởng phòng")
            db.add_all([p1, p2])
            db.flush()
        else:
            p1 = db.query(Position).filter_by(name="Chuyên viên").first()
            p2 = db.query(Position).filter_by(name="Trưởng phòng").first()

        # Persons
        if not db.query(Person).filter_by(code="NV001").first():
            db.add(Person(code="NV001", full_name="Nguyễn Văn A", unit=u1, position=p1, dob=date(1990,1,1), gender="Nam"))
        if not db.query(Person).filter_by(code="NV002").first():
            db.add(Person(code="NV002", full_name="Trần Thị B", unit=u2, position=p2, dob=date(1985,5,20), gender="Nữ"))

        # Salary ranks/steps
        if not db.query(SalaryRank).first():
            cv = SalaryRank(code="CV", name="Chuyên viên", level="Chuyên viên trở lên")
            nv = SalaryRank(code="NV", name="Nhân viên", level="Nhân viên")
            db.add_all([cv, nv])
            db.flush()
            # Steps for CV
            db.add_all([
                SalaryStep(rank_id=cv.id, step=1, coefficient=2.34, min_months=36),
                SalaryStep(rank_id=cv.id, step=2, coefficient=2.67, min_months=36),
                SalaryStep(rank_id=cv.id, step=3, coefficient=3.00, min_months=36),
            ])
            # Steps for NV
            db.add_all([
                SalaryStep(rank_id=nv.id, step=1, coefficient=1.86, min_months=24),
                SalaryStep(rank_id=nv.id, step=2, coefficient=2.06, min_months=24),
                SalaryStep(rank_id=nv.id, step=3, coefficient=2.26, min_months=24),
            ])

        # Histories for persons
        p1 = db.query(Person).filter_by(code="NV001").first()
        p2 = db.query(Person).filter_by(code="NV002").first()
        if p1 and not db.query(SalaryHistory).filter_by(person_id=p1.id).first():
            rank_cv = db.query(SalaryRank).filter_by(code="CV").first()
            db.add(SalaryHistory(person_id=p1.id, rank_id=rank_cv.id, step=1, coefficient=2.34, effective_date=date(2022, 1, 1)))
        if p2 and not db.query(SalaryHistory).filter_by(person_id=p2.id).first():
            rank_nv = db.query(SalaryRank).filter_by(code="NV").first()
            db.add(SalaryHistory(person_id=p2.id, rank_id=rank_nv.id, step=3, coefficient=2.26, effective_date=date(2021, 8, 1)))

        # Admin user
        if not db.query(User).filter_by(username="admin").first():
            admin = User(username="admin", password_hash=hash_password("admin123"), role="admin")
            db.add(admin)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
