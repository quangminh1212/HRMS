from typing import List, Dict, Any
import pandas as pd

from sqlalchemy.orm import Session

from .models import Person, Unit, Position

REQUIRED_COLUMNS = [
    "code", "full_name", "dob", "gender", "ethnicity", "religion", "hometown",
    "unit", "position", "party_joined_date", "llct_level", "professional_level",
    "status", "phone", "email",
]


def import_persons_from_excel(db: Session, xlsx_path: str) -> Dict[str, Any]:
    df = pd.read_excel(xlsx_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return {"ok": False, "error": f"Thiếu cột: {', '.join(missing)}"}

    created, updated = 0, 0

    # Chuẩn bị cache đơn vị/chức danh
    unit_cache: Dict[str, Unit] = {}
    position_cache: Dict[str, Position] = {}

    def get_unit(name: str) -> Unit:
        name = (str(name) or "").strip()
        if not name:
            return None
        if name in unit_cache:
            return unit_cache[name]
        u = db.query(Unit).filter_by(name=name).first()
        if not u:
            u = Unit(name=name)
            db.add(u)
            db.flush()
        unit_cache[name] = u
        return u

    def get_position(name: str) -> Position:
        name = (str(name) or "").strip()
        if not name:
            return None
        if name in position_cache:
            return position_cache[name]
        p = db.query(Position).filter_by(name=name).first()
        if not p:
            p = Position(name=name)
            db.add(p)
            db.flush()
        position_cache[name] = p
        return p

    for _, row in df.iterrows():
        code = str(row["code"]).strip()
        if not code:
            continue
        person = db.query(Person).filter_by(code=code).first()
        unit = get_unit(row["unit"]) if not pd.isna(row["unit"]) else None
        pos = get_position(row["position"]) if not pd.isna(row["position"]) else None
        fields = dict(
            full_name=str(row.get("full_name", "")) or None,
            dob=pd.to_datetime(row.get("dob"), errors='coerce').date() if not pd.isna(row.get("dob")) else None,
            gender=str(row.get("gender", "")) or None,
            ethnicity=str(row.get("ethnicity", "")) or None,
            religion=str(row.get("religion", "")) or None,
            hometown=str(row.get("hometown", "")) or None,
            unit_id=unit.id if unit else None,
            position_id=pos.id if pos else None,
            party_joined_date=pd.to_datetime(row.get("party_joined_date"), errors='coerce').date() if not pd.isna(row.get("party_joined_date")) else None,
            llct_level=str(row.get("llct_level", "")) or None,
            professional_level=str(row.get("professional_level", "")) or None,
            status=str(row.get("status", "")) or None,
            phone=str(row.get("phone", "")) or None,
            email=str(row.get("email", "")) or None,
        )
        if person:
            for k, v in fields.items():
                setattr(person, k, v)
            updated += 1
        else:
            person = Person(code=code, **fields)
            db.add(person)
            created += 1

    db.commit()
    return {"ok": True, "created": created, "updated": updated}
