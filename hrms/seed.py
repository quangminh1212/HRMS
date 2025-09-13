from datetime import date
from .db import SessionLocal
from .models import Unit, Position, Person, User
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
