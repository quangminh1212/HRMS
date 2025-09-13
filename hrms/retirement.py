from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models import Person, RetirementNotice


def calculate_retirement_date(person: Person) -> Optional[date]:
    """Tính tuổi nghỉ hưu cơ bản theo giới tính: giả định 60 (Nam), 55 (Nữ). Có thể nâng cấp theo lộ trình.
    Trả về None nếu thiếu DOB.
    """
    if not person.dob:
        return None
    years = 60 if (person.gender or "Nam").lower().startswith("n") else 55
    return date(person.dob.year + years, person.dob.month, person.dob.day)


def ensure_retirement_notice(db: Session, person: Person) -> Optional[RetirementNotice]:
    planned = calculate_retirement_date(person)
    if not planned:
        return None
    rn = db.query(RetirementNotice).filter_by(person_id=person.id).first()
    if not rn:
        rn = RetirementNotice(person_id=person.id, planned_date=planned)
        db.add(rn)
        db.commit()
        db.refresh(rn)
    return rn
