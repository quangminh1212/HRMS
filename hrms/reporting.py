from datetime import date
from collections import Counter
from typing import Dict, Any, List, Tuple

from sqlalchemy.orm import Session

from .models import Person, SalaryHistory, RetirementNotice, Appointment


def age_on(dob: date, as_of: date) -> int:
    if not dob:
        return -1
    years = as_of.year - dob.year - ((as_of.month, as_of.day) < (dob.month, dob.day))
    return years


def compute_annual_summary(db: Session, year: int) -> Dict[str, Any]:
    # Nâng lương: tính theo lịch sử lương trong năm
    inc = db.query(SalaryHistory).filter(
        SalaryHistory.effective_date >= date(year, 1, 1),
        SalaryHistory.effective_date <= date(year, 12, 31),
    ).count()

    # Nghỉ hưu: theo planned_date trong năm
    retire = db.query(RetirementNotice).filter(
        RetirementNotice.planned_date >= date(year, 1, 1),
        RetirementNotice.planned_date <= date(year, 12, 31),
    ).count()

    # Bổ nhiệm: theo start_date trong năm
    appoint = db.query(Appointment).filter(
        Appointment.start_date >= date(year, 1, 1),
        Appointment.start_date <= date(year, 12, 31),
    ).count()

    # Thai sản, đi học, thôi việc: dựa vào Person.status (đếm trạng thái hiện tại)
    maternity = db.query(Person).filter(Person.status.ilike('%thai sản%')).count()
    studying = db.query(Person).filter(Person.status.ilike('%đi học%')).count()
    leaving = db.query(Person).filter(Person.status.ilike('%thôi việc%')).count()

    return {
        "year": year,
        "salary_increase": inc,
        "retirement": retire,
        "appointment": appoint,
        "maternity": maternity,
        "studying": studying,
        "leaving": leaving,
    }


def compute_demographics(db: Session, as_of: date) -> Dict[str, Any]:
    people = db.query(Person).all()

    # Nhóm tuổi
    buckets = {"<30": 0, "30-40": 0, "41-50": 0, "51-60": 0, ">60": 0, "Unknown": 0}
    for p in people:
        a = age_on(p.dob, as_of)
        if a < 0:
            buckets["Unknown"] += 1
        elif a < 30:
            buckets["<30"] += 1
        elif a <= 40:
            buckets["30-40"] += 1
        elif a <= 50:
            buckets["41-50"] += 1
        elif a <= 60:
            buckets["51-60"] += 1
        else:
            buckets[">60"] += 1

    # Dân tộc, giới tính, LLCT, chuyên môn
    ethnicity = Counter([(p.ethnicity or "Khác").strip() for p in people])
    gender = Counter([(p.gender or "Khác").strip() for p in people])
    llct = Counter([(p.llct_level or "Chưa rõ").strip() for p in people])
    prof = Counter([(p.professional_level or "Chưa rõ").strip() for p in people])

    return {
        "age_buckets": buckets,
        "ethnicity": dict(ethnicity),
        "gender": dict(gender),
        "llct": dict(llct),
        "professional": dict(prof),
    }


def export_report_to_excel(summary: Dict[str, Any], demo: Dict[str, Any], path: str) -> None:
    from openpyxl import Workbook

    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Summary"
    ws1.append(["Year", summary["year"]])
    ws1.append(["Salary Increase", summary["salary_increase"]])
    ws1.append(["Retirement", summary["retirement"]])
    ws1.append(["Appointment", summary["appointment"]])
    ws1.append(["Maternity (current)", summary["maternity"]])
    ws1.append(["Studying (current)", summary["studying"]])
    ws1.append(["Leaving (current)", summary["leaving"]])

    ws2 = wb.create_sheet("Demographics")
    ws2.append(["Bucket", "Count"])
    for k, v in demo["age_buckets"].items():
        ws2.append([k, v])

    def write_counter(sheet_name: str, data: Dict[str, int]):
        ws = wb.create_sheet(sheet_name)
        ws.append(["Category", "Count"])
        for k, v in data.items():
            ws.append([k, v])

    write_counter("Ethnicity", demo["ethnicity"])
    write_counter("Gender", demo["gender"])
    write_counter("LLCT", demo["llct"])
    write_counter("Professional", demo["professional"])

    wb.save(path)
