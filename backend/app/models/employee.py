"""Employee model"""

from sqlalchemy import Column, String, Date, Enum, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.models.base import BaseModel


class Gender(enum.Enum):
    """Gender enum"""
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class EmployeeType(enum.Enum):
    """Employee type enum"""
    CADRE = "CADRE"  # Cán bộ
    CIVIL_SERVANT = "CIVIL_SERVANT"  # Công chức
    PUBLIC_EMPLOYEE = "PUBLIC_EMPLOYEE"  # Viên chức
    LABORER = "LABORER"  # Người lao động


class EmployeeStatus(enum.Enum):
    """Employee status enum"""
    ACTIVE = "ACTIVE"  # Đang làm việc
    ON_LEAVE = "ON_LEAVE"  # Nghỉ phép
    UNPAID_LEAVE = "UNPAID_LEAVE"  # Nghỉ không lương
    MATERNITY_LEAVE = "MATERNITY_LEAVE"  # Nghỉ thai sản
    STUDYING = "STUDYING"  # Đi học
    DIPLOMATIC_SPOUSE = "DIPLOMATIC_SPOUSE"  # Phu nhân ngoại giao
    RETIRED = "RETIRED"  # Nghỉ hưu
    RESIGNED = "RESIGNED"  # Thôi việc
    TRANSFERRED = "TRANSFERRED"  # Chuyển công tác
    SUSPENDED = "SUSPENDED"  # Tạm đình chỉ
    DISPATCHED = "DISPATCHED"  # Biệt phái
    ROTATED = "ROTATED"  # Luân chuyển


class Employee(BaseModel):
    """Employee model"""
    
    __tablename__ = "employees"
    
    # Basic Information
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    # Personal Information
    citizen_id = Column(String(20), unique=True, nullable=False)
    citizen_id_issue_date = Column(Date)
    citizen_id_issue_place = Column(String(255))
    
    # Contact Information
    phone_number = Column(String(20))
    email = Column(String(255), unique=True, index=True)
    permanent_address = Column(Text)
    temporary_address = Column(Text)
    hometown = Column(String(255))  # Quê quán
    
    # Cultural Information
    ethnicity = Column(String(50))  # Dân tộc
    religion = Column(String(50))  # Tôn giáo
    
    # Party Information
    party_member = Column(Date, nullable=True)  # Ngày vào Đảng
    
    # Employment Information
    employee_type = Column(Enum(EmployeeType), nullable=False)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE, nullable=False)
    start_date = Column(Date, nullable=False)  # Ngày bắt đầu làm việc
    social_insurance_start_date = Column(Date)  # Ngày bắt đầu đóng BHXH
    
    # Department and Position
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"))
    
    # Education
    education_level = Column(String(100))  # Trình độ chuyên môn
    political_theory_level = Column(String(100))  # Trình độ lý luận chính trị
    state_management_level = Column(String(100))  # Trình độ quản lý nhà nước
    
    # Profile Picture
    avatar_url = Column(String(500))
    
    # Additional fields
    notes = Column(Text)
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    contracts = relationship("Contract", back_populates="employee", cascade="all, delete-orphan")
    salary_histories = relationship("SalaryHistory", back_populates="employee", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="employee", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="employee", cascade="all, delete-orphan")
    work_histories = relationship("WorkHistory", back_populates="employee", cascade="all, delete-orphan")
    rewards = relationship("Reward", back_populates="employee", cascade="all, delete-orphan")
    disciplines = relationship("Discipline", back_populates="employee", cascade="all, delete-orphan")
    annual_reviews = relationship("AnnualReview", back_populates="employee", cascade="all, delete-orphan")
    languages = relationship("Language", back_populates="employee", cascade="all, delete-orphan")
    it_skills = relationship("ITSkill", back_populates="employee", cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="employee", cascade="all, delete-orphan")
    plannings = relationship("Planning", back_populates="employee", cascade="all, delete-orphan")
    insurances = relationship("Insurance", back_populates="employee", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Employee {self.employee_code}: {self.full_name}>">