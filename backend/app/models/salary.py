"""Salary related models"""

from sqlalchemy import Column, String, Float, Integer, Date, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.models.base import BaseModel


class SalaryGradeType(enum.Enum):
    """Salary grade type enum - Loại ngạch lương"""
    A3_1 = "A3.1"  # Chuyên viên cao cấp
    A2_1 = "A2.1"  # Chuyên viên chính
    A1 = "A1"      # Chuyên viên
    A0 = "A0"      # Cán sự
    B = "B"        # Nhân viên
    C1 = "C1"      # Nhân viên kỹ thuật


class SalaryGrade(BaseModel):
    """Salary grade model - Ngạch lương"""
    
    __tablename__ = "salary_grades"
    
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    grade_type = Column(Enum(SalaryGradeType), nullable=False)
    description = Column(Text)
    
    # Thời gian nâng lương (tháng)
    raise_period_months = Column(Integer, nullable=False, default=36)
    
    # Bậc lương tối thiểu và tối đa
    min_level = Column(Integer, default=1)
    max_level = Column(Integer, nullable=False)
    
    # Relationships
    salary_levels = relationship("SalaryLevel", back_populates="salary_grade", cascade="all, delete-orphan")
    salary_histories = relationship("SalaryHistory", back_populates="salary_grade")
    
    def __repr__(self):
        return f"<SalaryGrade {self.code}: {self.name}>"


class SalaryLevel(BaseModel):
    """Salary level model - Bậc lương"""
    
    __tablename__ = "salary_levels"
    
    salary_grade_id = Column(UUID(as_uuid=True), ForeignKey("salary_grades.id"), nullable=False)
    level = Column(Integer, nullable=False)  # Bậc (1, 2, 3, ...)
    coefficient = Column(Float, nullable=False)  # Hệ số lương
    
    # Relationships
    salary_grade = relationship("SalaryGrade", back_populates="salary_levels")
    
    def __repr__(self):
        return f"<SalaryLevel Grade:{self.salary_grade_id} Level:{self.level} Coef:{self.coefficient}>"


class SalaryHistory(BaseModel):
    """Salary history model - Lịch sử lương"""
    
    __tablename__ = "salary_histories"
    
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    salary_grade_id = Column(UUID(as_uuid=True), ForeignKey("salary_grades.id"), nullable=False)
    
    # Salary information
    salary_level = Column(Integer, nullable=False)  # Bậc lương
    salary_coefficient = Column(Float, nullable=False)  # Hệ số lương
    
    # Dates
    effective_date = Column(Date, nullable=False)  # Ngày có hiệu lực
    next_raise_date = Column(Date)  # Ngày nâng lương tiếp theo
    
    # Decision information
    decision_number = Column(String(100))  # Số quyết định
    decision_date = Column(Date)  # Ngày quyết định
    
    # Raise type
    is_early_raise = Column(Boolean, default=False)  # Nâng lương trước thời hạn
    early_raise_reason = Column(Text)  # Lý do nâng lương trước thời hạn
    
    # Seniority allowance - Phụ cấp thâm niên vượt khung
    seniority_allowance_percent = Column(Float, default=0)  # % phụ cấp thâm niên
    
    # Other allowances
    position_allowance = Column(Float, default=0)  # Phụ cấp chức vụ
    responsibility_allowance = Column(Float, default=0)  # Phụ cấp trách nhiệm
    hazard_allowance = Column(Float, default=0)  # Phụ cấp độc hại
    other_allowances = Column(Float, default=0)  # Phụ cấp khác
    
    # Status
    is_current = Column(Boolean, default=True)  # Là mức lương hiện tại
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    employee = relationship("Employee", back_populates="salary_histories")
    salary_grade = relationship("SalaryGrade", back_populates="salary_histories")
    
    def __repr__(self):
        return f"<SalaryHistory Employee:{self.employee_id} Grade:{self.salary_grade_id} Level:{self.salary_level}>">