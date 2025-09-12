"""
HRMS Enhanced Models - Database cho 11 tính năng đầy đủ
Thiết kế theo yêu cầu chi tiết của người dùng
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
import enum
import os

Base = declarative_base()

# Enums
class GenderEnum(enum.Enum):
    MALE = "Nam"
    FEMALE = "Nữ"

class WorkStatusEnum(enum.Enum):
    ACTIVE = "Đang công tác"
    UNPAID_LEAVE = "Nghỉ không lương"
    STUDY_LEAVE = "Đi học"
    MATERNITY_LEAVE = "Nghỉ thai sản"
    DIPLOMATIC_SPOUSE = "Phu nhân ngoại giao"

class EducationLevelEnum(enum.Enum):
    HIGH_SCHOOL = "Phổ thông"
    COLLEGE = "Cao đẳng"
    BACHELOR = "Cử nhân"
    MASTER = "Thạc sĩ"
    DOCTOR = "Tiến sĩ"

class PoliticalTheoryEnum(enum.Enum):
    BASIC = "Sơ cấp"
    INTERMEDIATE = "Trung cấp"
    ADVANCED = "Cao cấp"

class DefenseSecurityEnum(enum.Enum):
    LEVEL_1 = "Đối tượng 1"
    LEVEL_2 = "Đối tượng 2" 
    LEVEL_3 = "Đối tượng 3"
    LEVEL_4 = "Đối tượng 4"

class StateManagementEnum(enum.Enum):
    SENIOR_SPECIALIST = "Chuyên viên cao cấp"
    PRINCIPAL_SPECIALIST = "Chuyên viên chính"
    SPECIALIST = "Chuyên viên"

class PerformanceEnum(enum.Enum):
    EXCELLENT = "Hoàn thành xuất sắc"
    GOOD = "Hoàn thành tốt"
    SATISFACTORY = "Hoàn thành"
    UNSATISFACTORY = "Không hoàn thành"

# Main Models
class Employee(Base):
    """Model nhân viên với đầy đủ thông tin theo yêu cầu"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    
    # Thông tin cơ bản
    full_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    ethnicity = Column(String(50))  # Dân tộc
    religion = Column(String(50))   # Tôn giáo
    hometown = Column(String(200))  # Quê quán
    
    # Thông tin đảng
    party_join_date = Column(Date)  # Ngày vào Đảng
    
    # Chức vụ và đơn vị
    position = Column(String(100))      # Chức vụ/chức danh
    department = Column(String(100))    # Đơn vị
    
    # Trình độ
    political_theory_level = Column(Enum(PoliticalTheoryEnum))
    education_level = Column(Enum(EducationLevelEnum))
    
    # Tình trạng công tác
    work_status = Column(Enum(WorkStatusEnum), default=WorkStatusEnum.ACTIVE)
    work_status_details = Column(Text)  # Chi tiết trạng thái
    
    # Lương và ngạch
    current_salary_grade = Column(String(20))    # Ngạch hiện hưởng
    current_salary_level = Column(Integer)       # Bậc lương
    current_salary_coefficient = Column(Float)   # Hệ số lương
    current_salary_date = Column(Date)           # Ngày hưởng lương hiện tại
    position_allowance = Column(Float)           # Phụ cấp chức vụ
    position_allowance_reserve_until = Column(Date)  # Bảo lưu phụ cấp đến
    
    # Thời gian công tác
    social_insurance_start_date = Column(Date)   # Ngày bắt đầu đóng BHXH
    organization_start_date = Column(Date)       # Ngày vào cơ quan
    
    # Quy hoạch
    current_planning = Column(String(200))       # Chức danh quy hoạch hiện tại
    
    # Liên hệ
    phone = Column(String(20))
    email = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    work_history = relationship('WorkHistory', back_populates='employee', cascade='all, delete-orphan')
    salary_history = relationship('SalaryHistory', back_populates='employee', cascade='all, delete-orphan')
    education_records = relationship('Education', back_populates='employee', cascade='all, delete-orphan')
    training_records = relationship('Training', back_populates='employee', cascade='all, delete-orphan')
    achievements = relationship('Achievement', back_populates='employee', cascade='all, delete-orphan')
    evaluations = relationship('Evaluation', back_populates='employee', cascade='all, delete-orphan')
    councils = relationship('CouncilMembership', back_populates='employee', cascade='all, delete-orphan')
    contracts = relationship('LaborContract', back_populates='employee', cascade='all, delete-orphan')
    plannings = relationship('Planning', back_populates='employee', cascade='all, delete-orphan')

class Education(Base):
    """Trình độ chuyên môn chi tiết"""
    __tablename__ = 'education'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    level = Column(Enum(EducationLevelEnum), nullable=False)
    field_of_study = Column(String(200))    # Ngành học
    institution = Column(String(200))       # Trường
    country = Column(String(100))           # Nước
    study_mode = Column(String(100))        # Hình thức (chính quy, tại chức...)
    graduation_date = Column(Date)
    
    employee = relationship('Employee', back_populates='education_records')

class Training(Base):  
    """Đào tạo, bồi dưỡng"""
    __tablename__ = 'training'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    training_type = Column(String(100))     # Loại: Lý luận chính trị, QPAN, QLNN, etc
    level = Column(String(100))             # Cấp độ: Cao cấp, Trung cấp, etc
    institution = Column(String(200))
    completion_date = Column(Date)
    certificate_number = Column(String(100))
    
    employee = relationship('Employee', back_populates='training_records')

class Achievement(Base):
    """Thành tích, khen thưởng"""  
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    award_type = Column(String(200))        # Loại khen thưởng
    award_level = Column(String(100))       # Cấp độ (Hạng nhất, nhì, ba...)
    award_year = Column(Integer)
    issuing_authority = Column(String(200))  # Cơ quan cấp
    details = Column(Text)
    
    employee = relationship('Employee', back_populates='achievements')

class Evaluation(Base):
    """Đánh giá hàng năm"""
    __tablename__ = 'evaluations'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    year = Column(Integer, nullable=False)
    performance = Column(Enum(PerformanceEnum), nullable=False)
    details = Column(Text)
    
    employee = relationship('Employee', back_populates='evaluations')

class WorkHistory(Base):
    """Quá trình công tác với timeline"""
    __tablename__ = 'work_history'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)  # NULL nếu đang công tác
    position = Column(String(200))
    department = Column(String(200))
    organization = Column(String(200))
    responsibilities = Column(Text)
    
    employee = relationship('Employee', back_populates='work_history')

class SalaryHistory(Base):
    """Lịch sử lương chi tiết"""
    __tablename__ = 'salary_history'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    effective_date = Column(Date, nullable=False)
    salary_grade = Column(String(20))       # Ngạch
    salary_level = Column(Integer)          # Bậc
    salary_coefficient = Column(Float)      # Hệ số
    position_allowance = Column(Float)      # Phụ cấp chức vụ
    seniority_allowance_percent = Column(Float, default=0)  # % Phụ cấp thâm niên
    reason = Column(String(200))            # Lý do nâng lương
    decision_number = Column(String(100))   # Số quyết định
    notes = Column(Text)
    
    employee = relationship('Employee', back_populates='salary_history')

class CouncilMembership(Base):
    """Tham gia hội đồng, ban chỉ đạo"""
    __tablename__ = 'council_memberships'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    council_name = Column(String(200), nullable=False)
    role = Column(String(100))              # Vai trò: Chủ tịch, Thành viên...
    start_date = Column(Date)
    end_date = Column(Date)
    is_internal = Column(Boolean, default=True)  # Trong hoặc ngoài cơ quan
    
    employee = relationship('Employee', back_populates='councils')

class LaborContract(Base):
    """Hợp đồng lao động"""
    __tablename__ = 'labor_contracts'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    contract_type = Column(String(100))     # Loại HĐ: Ban kiểm soát, Nhân viên...
    contract_number = Column(String(100))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    salary = Column(Float)
    position = Column(String(200))
    is_active = Column(Boolean, default=True)
    
    employee = relationship('Employee', back_populates='contracts')

class Planning(Base):  
    """Quy hoạch cán bộ"""
    __tablename__ = 'planning'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    planning_year = Column(Integer, nullable=False)
    position = Column(String(200))          # Vị trí quy hoạch
    department = Column(String(200))
    age_at_planning = Column(Integer)
    is_current = Column(Boolean, default=True)
    notes = Column(Text)
    
    employee = relationship('Employee', back_populates='plannings')

class SalaryRule(Base):
    """Quy tắc nâng lương"""
    __tablename__ = 'salary_rules'
    
    id = Column(Integer, primary_key=True)
    
    position_type = Column(String(100))     # Loại ngạch: Chuyên viên, Nhân viên...
    months_required = Column(Integer)       # Số tháng yêu cầu: 36, 24
    seniority_increase_months = Column(Integer, default=36)  # Tháng cho phụ cấp thâm niên
    seniority_increase_percent = Column(Float, default=5.0)  # % tăng đầu tiên
    yearly_increase_percent = Column(Float, default=1.0)     # % tăng hàng năm
    
class RetirementAlert(Base):
    """Cảnh báo nghỉ hưu"""  
    __tablename__ = 'retirement_alerts'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    estimated_retirement_date = Column(Date, nullable=False)
    six_month_alert_sent = Column(Boolean, default=False)
    three_month_alert_sent = Column(Boolean, default=False)
    notification_created = Column(Boolean, default=False)
    decision_created = Column(Boolean, default=False)
    
    employee = relationship('Employee')

class InsuranceReport(Base):
    """Báo bảo hiểm"""
    __tablename__ = 'insurance_reports'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    report_month = Column(Integer)
    report_year = Column(Integer)
    change_type = Column(String(100))       # Điều chỉnh chức danh/lương/phụ cấp/nghỉ hưu...
    old_value = Column(String(200))
    new_value = Column(String(200))
    effective_date = Column(Date)
    processed = Column(Boolean, default=False)
    
    employee = relationship('Employee')

# Database functions
def get_engine():
    """Tạo database engine"""
    return create_engine('sqlite:///database.db', echo=False)

def init_enhanced_database():
    """Khởi tạo database với schema mới"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    
    # Tạo session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Tạo default salary rules
    create_default_salary_rules(session)
    
    # Tạo sample data nếu chưa có
    if session.query(Employee).count() == 0:
        create_enhanced_sample_data(session)
    
    session.close()
    print("✅ Enhanced database initialized successfully!")
    return engine

def create_default_salary_rules(session):
    """Tạo quy tắc nâng lương mặc định"""
    rules = [
        SalaryRule(
            position_type="Chuyên viên và tương đương trở lên",
            months_required=36,
            seniority_increase_months=36,
            seniority_increase_percent=5.0,
            yearly_increase_percent=1.0
        ),
        SalaryRule(
            position_type="Nhân viên, thủ quỹ",
            months_required=24,
            seniority_increase_months=24, 
            seniority_increase_percent=5.0,
            yearly_increase_percent=1.0
        )
    ]
    
    for rule in rules:
        existing = session.query(SalaryRule).filter_by(position_type=rule.position_type).first()
        if not existing:
            session.add(rule)
    
    session.commit()

def create_enhanced_sample_data(session):
    """Tạo dữ liệu mẫu đầy đủ"""
    from datetime import timedelta
    
    # Tạo nhân viên mẫu với đầy đủ thông tin
    employees = [
        Employee(
            full_name="Nguyễn Văn An",
            date_of_birth=date(1985, 3, 15),
            gender=GenderEnum.MALE,
            ethnicity="Kinh",
            religion="Phật giáo",
            hometown="Hà Nội",
            party_join_date=date(2010, 7, 1),
            position="Chuyên viên chính",
            department="Phòng Tổ chức - Cán bộ",
            political_theory_level=PoliticalTheoryEnum.ADVANCED,
            education_level=EducationLevelEnum.MASTER,
            work_status=WorkStatusEnum.ACTIVE,
            current_salary_grade="A2",
            current_salary_level=5,
            current_salary_coefficient=4.5,
            current_salary_date=date(2022, 1, 1),
            position_allowance=0.8,
            social_insurance_start_date=date(2008, 1, 1),
            organization_start_date=date(2010, 1, 1),
            current_planning="Phó trưởng phòng",
            phone="0912345678",
            email="nva@company.com"
        ),
        Employee(
            full_name="Trần Thị Bình",
            date_of_birth=date(1990, 8, 22),
            gender=GenderEnum.FEMALE,
            ethnicity="Kinh", 
            religion="Công giáo",
            hometown="TP. Hồ Chí Minh",
            party_join_date=date(2015, 12, 10),
            position="Chuyên viên",
            department="Phòng Kế hoạch - Tài chính",
            political_theory_level=PoliticalTheoryEnum.INTERMEDIATE,
            education_level=EducationLevelEnum.BACHELOR,
            work_status=WorkStatusEnum.ACTIVE,
            current_salary_grade="A1",
            current_salary_level=3,
            current_salary_coefficient=3.2,
            current_salary_date=date(2021, 6, 1),
            position_allowance=0.5,
            social_insurance_start_date=date(2012, 6, 1),
            organization_start_date=date(2013, 1, 1),
            current_planning="Chuyên viên chính",
            phone="0987654321",
            email="ttb@company.com"
        )
    ]
    
    for emp in employees:
        session.add(emp)
    
    session.commit()
    print("✅ Enhanced sample data created successfully!")

if __name__ == "__main__":
    init_enhanced_database()
