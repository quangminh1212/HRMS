from datetime import date
from typing import Tuple

from sqlalchemy.orm import Session

from .models import Person, JobPositionRequirement, WorkProcess, Appointment


def check_appointment_eligibility(
    db: Session,
    person: Person,
    target_position: str,
) -> Tuple[bool, list[str]]:
    """
    Kiểm tra điều kiện bổ nhiệm: trong quy hoạch? (tạm bỏ qua nếu chưa có mapping)
    Đáp ứng bằng cấp/LLCT/QLNN?
    Kinh nghiệm tối thiểu?
    Trả về (eligible, reasons)
    """
    reasons: list[str] = []
    req = db.query(JobPositionRequirement).filter_by(position_name=target_position).first()
    if req:
        # Bằng cấp: đối chiếu với person.professional_level (đơn giản hoá)
        if req.required_degree and (person.professional_level or "").strip() == "":
            reasons.append("Thiếu văn bằng/chứng chỉ yêu cầu")
        # LLCT/QLNN: đối chiếu
        if req.required_llct and (person.llct_level or "").strip() == "":
            reasons.append("Thiếu LLCT theo yêu cầu")
        if req.required_qlnn:
            # Không có trường riêng -> giả sử lưu trong professional_level, đơn giản hoá
            if "Chuyên viên" not in (person.professional_level or ""):
                reasons.append("Thiếu QLNN theo yêu cầu")
        # Kinh nghiệm: tính năm từ quá trình công tác
        if req.min_years_experience:
            total_years = 0.0
            for w in db.query(WorkProcess).filter_by(person_id=person.id).all():
                end = w.end_date or date.today()
                days = (end - w.start_date).days
                total_years += days / 365.0
            if total_years + 1e-6 < req.min_years_experience:
                reasons.append(f"Kinh nghiệm < {req.min_years_experience} năm")
    # TODO: kiểm tra trong quy hoạch khi có dữ liệu quy hoạch chi tiết

    return (len(reasons) == 0, reasons)
