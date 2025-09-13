from datetime import date
from .db import SessionLocal
from .models import Unit, Position, Person, User
from .security import hash_password


def seed_basic_data():
    db = SessionLocal()
    try:
        # Units
        u1 = Unit(name="Văn phòng")
        u2 = Unit(name="Phòng Tổ chức")
        db.add_all([u1, u2])
        db.flush()

        # Positions
        p1 = Position(name="Chuyên viên")
        p2 = Position(name="Trưởng phòng")
        db.add_all([p1, p2])
        db.flush()

        # Persons
        persons = [
            Person(code="NV001", full_name="Nguyễn Văn A", unit=u1, position=p1, dob=date(1990,1,1), gender="Nam"),
            Person(code="NV002", full_name="Trần Thị B", unit=u2, position=p2, dob=date(1985,5,20), gender="Nữ"),
        ]
        db.add_all(persons)

        # Admin user
        admin = User(username="admin", password_hash=hash_password("admin123"), role="admin")
        db.add(admin)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
