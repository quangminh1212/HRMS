from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Float, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from .db import Base


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey("units.id"), nullable=True)

    parent = relationship("Unit", remote_side=[id], backref="children")


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)  # Nam/Nu/Khac
    ethnicity = Column(String(100), nullable=True)
    religion = Column(String(100), nullable=True)
    hometown = Column(String(255), nullable=True)

    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)

    party_joined_date = Column(Date, nullable=True)
    llct_level = Column(String(100), nullable=True)  # Trinh do ly luan chinh tri
    professional_level = Column(String(255), nullable=True)  # hien thi ngan gon

    status = Column(String(100), nullable=True)  # Dang cong tac, nghi thai san, di hoc, ...

    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    unit = relationship("Unit")
    position = relationship("Position")


class Education(Base):
    __tablename__ = "educations"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    level = Column(String(100), nullable=False)  # DH/Sau DH/LLCT/QPAN/QLNN/Khac
    major = Column(String(255), nullable=True)
    school = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    method = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


class WorkProcess(Base):
    __tablename__ = "work_processes"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    unit = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)


class Planning(Base):
    __tablename__ = "plannings"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    job_position = Column(String(255), nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)


class SalaryRank(Base):
    __tablename__ = "salary_ranks"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    level = Column(String(100), nullable=True)  # Chuyen vien/nhan vien/thu quy...


class SalaryStep(Base):
    __tablename__ = "salary_steps"
    id = Column(Integer, primary_key=True)
    rank_id = Column(Integer, ForeignKey("salary_ranks.id"), nullable=False)
    step = Column(Integer, nullable=False)
    coefficient = Column(Float, nullable=False)
    min_months = Column(Integer, nullable=False)  # 36 or 24
    __table_args__ = (UniqueConstraint('rank_id', 'step', name='uq_rank_step'),)


class SalaryHistory(Base):
    __tablename__ = "salary_histories"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    rank_id = Column(Integer, ForeignKey("salary_ranks.id"), nullable=False)
    step = Column(Integer, nullable=False)
    coefficient = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
    note = Column(String(255), nullable=True)  # ky luat/ly do keo dai


class Allowance(Base):
    __tablename__ = "allowances"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    type = Column(String(100), nullable=False)  # chuc vu, vuot khung, khac
    percent = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


class AnnualEvaluation(Base):
    __tablename__ = "annual_evaluations"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    year = Column(Integer, nullable=False)
    level = Column(String(100), nullable=False)  # XS/ Tot / Hoan thanh / Khong hoan thanh
    __table_args__ = (UniqueConstraint('person_id', 'year', name='uq_eval_year'),)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # admin, hr, unit_manager, user
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String(500), nullable=True)


class EmailLog(Base):
    __tablename__ = "email_logs"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(String(100), nullable=False)  # salary_due, bhxh_monthly, contracts_expiring, quick_report, retirement
    unit_name = Column(String(255), nullable=True)
    recipients = Column(String(1000), nullable=True)  # comma-separated
    subject = Column(String(255), nullable=False)
    body = Column(String(1000), nullable=True)
    attachments = Column(String(2000), nullable=True)  # comma-separated paths
    status = Column(String(50), nullable=False, default="sent")  # sent/failed
    error = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(1000), nullable=True)


class UnitEmailRecipient(Base):
    __tablename__ = "unit_email_recipients"
    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    email = Column(String(255), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('unit_id', 'email', name='uq_unit_email'),)


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    contract_type = Column(String(100), nullable=False)  # ban kiem soat/nhan vien/
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    note = Column(String(255), nullable=True)


class RetirementNotice(Base):
    __tablename__ = "retirement_notices"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    planned_date = Column(Date, nullable=False)
    notice_date = Column(Date, nullable=True)  # ngày thông báo 6 tháng trước
    decision_date = Column(Date, nullable=True)  # ngày quyết định 3 tháng trước
    note = Column(String(255), nullable=True)


class InsuranceEvent(Base):
    __tablename__ = "insurance_events"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    event_type = Column(String(100), nullable=False)  # dieu chinh chuc danh/luong/phu cap; thai san; om dau;...
    event_date = Column(Date, nullable=False)
    details = Column(String(500), nullable=True)


class JobPositionRequirement(Base):
    __tablename__ = "job_position_requirements"
    id = Column(Integer, primary_key=True)
    position_name = Column(String(255), nullable=False)
    required_degree = Column(String(255), nullable=True)
    required_llct = Column(String(100), nullable=True)
    required_qlnn = Column(String(100), nullable=True)
    min_years_experience = Column(Integer, nullable=True)
    __table_args__ = (UniqueConstraint('position_name', name='uq_position_req'),)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    position_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    term_months = Column(Integer, nullable=True)  # thời hạn bổ nhiệm (nếu có)
    reappointment_due_date = Column(Date, nullable=True)
    note = Column(String(255), nullable=True)
