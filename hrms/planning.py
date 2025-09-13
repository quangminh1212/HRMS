from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models import Planning, Person


def is_in_planning(db: Session, person_id: int, position_name: str, year: int) -> bool:
    q = (
        db.query(Planning)
        .filter(Planning.person_id == person_id)
        .filter(Planning.job_position == position_name)
        .filter(Planning.start_year <= year)
        .filter(Planning.end_year >= year)
    )
    return db.query(q.exists()).scalar()


def add_planning(db: Session, person: Person, position_name: str, start_year: int, end_year: int) -> Planning:
    pl = Planning(person_id=person.id, job_position=position_name, start_year=start_year, end_year=end_year)
    db.add(pl)
    db.commit()
    db.refresh(pl)
    return pl
