"""
Database Models cho HRMS Streamlit Version
Bao gồm tất cả các thông tin chi tiết theo yêu cầu
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """Model người dùng hệ thống"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False) 
    password_hash = Column(String(200))
    role = Column(String(20), default='user')  # admin, manager, user
    created_at = Column(DateTime, default=datetime.utcnow)

class Employee(Base):
    """Model nhân viên với đầy đủ thông tin theo yêu cầu"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    employee_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    
    # Thông tin cá nhân chi tiết
    date_of_birth = Column(Date)
    gender = Column(String(10))  # Nam/Nữ
    ethnicity = Column(String(50))  # Dân tộc
    religion = Column(String(50))  # Tôn giáo
    hometown = Column(String(200))  # Quê quán
    id_number = Column(String(20))  # Số CCCD/CMND
    id_issue_date = Column(Date)  # Ngày cấp
    id_issue_place = Column(String(100))  # Nơi cấp
    
    # Thông tin công việc
    position = Column(String(100))  # Chức vụ/chức danh
    department = Column(String(100))  # Đơn vị
    party_join_date = Column(Date)  # Ngày vào Đảng
    political_theory_level = Column(String(50))  # Trình độ lý luận chính trị
    professional_level = Column(String(300))  # Trình độ chuyên môn chi tiết
    
    # Thông tin lương chi tiết
    current_salary_level = Column(String(20))  # Ngạch lương hiện tại
    current_salary_coefficient = Column(Float)  # Hệ số lương hiện tại
    last_salary_increase_date = Column(Date)  # Ngày nâng lương gần nhất
    position_allowance = Column(Float, default=0)  # Phụ cấp chức vụ
    seniority_allowance = Column(Float, default=0)  # Phụ cấp thâm niên vượt khung
    position_allowance_preserve_until = Column(Date)  # Bảo lưu phụ cấp đến
    
    # Tình trạng công tác chi tiết
    work_status = Column(String(50), default='active')  # active, on_leave, studying, maternity, diplomatic_spouse
    work_status_details = Column(Text)  # Chi tiết tình trạng
    work_status_start_date = Column(Date)  # Ngày bắt đầu tình trạng hiện tại
    work_status_end_date = Column(Date)  # Ngày kết thúc dự kiến
    salary_percentage = Column(Integer, default=100)  # % lương hưởng (40% khi đi học >3 tháng)
    
    # Thông tin liên hệ
    phone = Column(String(20))
    email = Column(String(120))
    address = Column(String(300))
    emergency_contact = Column(String(100))  # Người liên hệ khẩn cấp
    emergency_phone = Column(String(20))  # SĐT người liên hệ khẩn cấp
    
    # Thông tin công tác
    start_date = Column(Date)  # Ngày bắt đầu công tác (tính BHXH)
    organization_start_date = Column(Date)  # Ngày vào cơ quan hiện tại
    retirement_date = Column(Date)  # Ngày nghỉ hưu dự kiến
    
    # Quy hoạch
    current_planning_position = Column(String(100))  # Chức danh quy hoạch hiện tại
    planning_period = Column(String(20))  # Giai đoạn quy hoạch
    
    # Trạng thái
    status = Column(String(20), default='active')  # active, retired, resigned, deceased
    notes = Column(Text)  # Ghi chú đặc biệt
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    salary_history = relationship('SalaryHistory', back_populates='employee', cascade='all, delete-orphan')
    work_history = relationship('WorkHistory', back_populates='employee', cascade='all, delete-orphan')
    trainings = relationship('Training', back_populates='employee', cascade='all, delete-orphan')
    achievements = relationship('Achievement', back_populates='employee', cascade='all, delete-orphan')
    evaluations = relationship('Evaluation', back_populates='employee', cascade='all, delete-orphan')
    councils = relationship('Council', back_populates='employee', cascade='all, delete-orphan')
    insurances = relationship('Insurance', back_populates='employee', cascade='all, delete-orphan')
    plannings = relationship('Planning', back_populates='employee', cascade='all, delete-orphan')

class SalaryHistory(Base):
    """Lịch sử lương chi tiết"""
    __tablename__ = 'salary_history'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    salary_level = Column(String(20))  # Ngạch lương
    salary_coefficient = Column(Float)  # Hệ số lương
    position_allowance = Column(Float, default=0)  # Phụ cấp chức vụ
    seniority_allowance = Column(Float, default=0)  # Phụ cấp thâm niên
    effective_date = Column(Date)  # Ngày hiệu lực
    end_date = Column(Date)  # Ngày kết thúc
    reason = Column(String(200))  # Lý do (định kỳ, trước thời hạn, thăng chức...)
    decision_number = Column(String(50))  # Số quyết định
    decision_date = Column(Date)  # Ngày ký quyết định
    is_early_increase = Column(Boolean, default=False)  # Nâng lương trước thời hạn
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='salary_history')

class WorkHistory(Base):
    """Quá trình công tác chi tiết"""
    __tablename__ = 'work_history'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    position = Column(String(100))  # Chức vụ
    department = Column(String(100))  # Phòng ban
    organization = Column(String(200))  # Cơ quan/Đơn vị
    location = Column(String(100))  # Địa điểm công tác
    start_date = Column(Date)
    end_date = Column(Date)
    responsibilities = Column(Text)  # Nhiệm vụ được giao
    achievements = Column(Text)  # Thành tích đạt được
    reason_for_change = Column(String(200))  # Lý do thay đổi
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='work_history')

class Training(Base):
    """Đào tạo bồi dưỡng chi tiết"""
    __tablename__ = 'trainings'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    # Phân loại đào tạo
    training_type = Column(String(50))  # Đại học, Sau đại học, LLCT, QPAN, QLNN, Theo YCUT, Khác
    training_name = Column(String(200))  # Tên khóa học
    institution = Column(String(200))  # Cơ sở đào tạo
    country = Column(String(50), default='Việt Nam')  # Nước đào tạo
    
    # Thông tin bằng cấp
    degree = Column(String(100))  # Loại bằng (Cử nhân, Thạc sĩ, Tiến sĩ...)
    major = Column(String(100))  # Chuyên ngành
    classification = Column(String(50))  # Loại tốt nghiệp (Xuất sắc, Giỏi, Khá...)
    
    # Thời gian
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Hình thức đào tạo
    training_mode = Column(String(50))  # Chính quy, Tại chức, Từ xa, Liên thông...
    funding_source = Column(String(50))  # Nguồn kinh phí (Nhà nước, Cá nhân...)
    
    # Chứng chỉ
    certificate_number = Column(String(100))
    certificate_date = Column(Date)
    
    # LLCT cụ thể
    political_level = Column(String(50))  # Sơ cấp, Trung cấp, Cao cấp, Cử nhân
    
    # QPAN cụ thể  
    defense_level = Column(String(50))  # Đối tượng 1, 2, 3, 4
    
    # QLNN cụ thể
    management_level = Column(String(50))  # Chuyên viên, Chuyên viên chính, Chuyên viên cao cấp
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='trainings')

class Achievement(Base):
    """Thành tích khen thưởng chi tiết"""
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    # Phân loại thành tích
    achievement_category = Column(String(50))  # Danh hiệu thi đua, Huân chương, Bằng khen, Kỷ niệm chương, Khác
    achievement_type = Column(String(100))  # Chi tiết loại
    achievement_name = Column(String(200))  # Tên cụ thể
    
    # Cấp khen thưởng
    level = Column(String(50))  # Nhà nước, Bộ/Tỉnh, Cơ quan, Cơ sở
    
    # Đối với Huân chương
    medal_class = Column(String(20))  # Hạng Nhất, Hạng Nhì, Hạng Ba
    
    # Thông tin quyết định
    date = Column(Date)  # Ngày được tặng/phong
    decision_number = Column(String(100))  # Số quyết định
    decision_date = Column(Date)  # Ngày ký quyết định
    issuing_authority = Column(String(200))  # Cơ quan ban hành
    
    # Lý do khen thưởng
    reason = Column(Text)  # Căn cứ khen thưởng
    year_for = Column(Integer)  # Năm được khen thưởng (nếu có)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='achievements')

class Evaluation(Base):
    """Đánh giá hàng năm"""
    __tablename__ = 'evaluations'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(String(50))  # Hoàn thành xuất sắc, Hoàn thành tốt, Hoàn thành, Không hoàn thành
    
    # Chi tiết đánh giá
    work_performance = Column(Text)  # Kết quả thực hiện nhiệm vụ
    discipline = Column(Text)  # Ý thức chấp hành kỷ luật
    ethics = Column(Text)  # Đạo đức, lối sống
    relationships = Column(Text)  # Quan hệ với đồng nghiệp
    
    # Điểm số (nếu có)
    score = Column(Float)  # Điểm tổng kết
    rank_in_unit = Column(Integer)  # Xếp hạng trong đơn vị
    
    # Ý kiến nhận xét
    supervisor_comment = Column(Text)  # Nhận xét của cấp trên
    self_assessment = Column(Text)  # Tự đánh giá
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='evaluations')
    
    __table_args__ = tuple([])

class Council(Base):
    """Tham gia hội đồng, ban chỉ đạo"""
    __tablename__ = 'councils'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    council_name = Column(String(200))  # Tên hội đồng/ban chỉ đạo
    council_type = Column(String(50))  # Hội đồng, Ban chỉ đạo, Tổ biên tập...
    position_in_council = Column(String(100))  # Chức vụ trong hội đồng
    scope = Column(String(50))  # Trong cơ quan, Ngoài cơ quan
    
    start_date = Column(Date)  # Ngày bắt đầu tham gia
    end_date = Column(Date)  # Ngày kết thúc
    
    decision_number = Column(String(100))  # Số quyết định thành lập
    decision_date = Column(Date)  # Ngày quyết định
    
    responsibilities = Column(Text)  # Nhiệm vụ được giao
    status = Column(String(20), default='active')  # active, completed, terminated
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='councils')

class Insurance(Base):
    """Thông tin bảo hiểm"""
    __tablename__ = 'insurances'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    # Loại bảo hiểm
    insurance_type = Column(String(20))  # BHXH, BHYT, BHTN
    insurance_number = Column(String(50))  # Số sổ/thẻ BHXH
    
    # Thông tin đóng
    monthly_salary = Column(Float)  # Lương đóng bảo hiểm
    start_date = Column(Date)  # Ngày bắt đầu đóng
    end_date = Column(Date)  # Ngày kết thúc (nếu có)
    
    # Tình trạng
    status = Column(String(20), default='active')  # active, suspended, terminated
    suspension_reason = Column(String(200))  # Lý do tạm dừng (nếu có)
    suspension_start = Column(Date)
    suspension_end = Column(Date)
    
    # Ghi chú
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='insurances')

class Planning(Base):
    """Lịch sử quy hoạch cán bộ"""
    __tablename__ = 'plannings'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    
    planning_position = Column(String(100))  # Vị trí quy hoạch
    planning_level = Column(String(50))  # Cấp quy hoạch (Trung ương, Bộ, Tỉnh...)
    planning_period = Column(String(20))  # Giai đoạn (2020-2025)
    planning_year = Column(Integer)  # Năm quy hoạch
    
    # Trạng thái quy hoạch
    status = Column(String(20), default='active')  # active, completed, cancelled, promoted
    
    # Thông tin quyết định
    decision_number = Column(String(100))
    decision_date = Column(Date)
    approving_authority = Column(String(200))  # Cơ quan phê duyệt
    
    # Điều kiện khi quy hoạch
    age_when_planned = Column(Integer)  # Tuổi khi được quy hoạch
    position_when_planned = Column(String(100))  # Chức vụ khi được quy hoạch
    
    # Kết quả
    completion_date = Column(Date)  # Ngày hoàn thành quy hoạch
    actual_position = Column(String(100))  # Chức vụ thực tế được bổ nhiệm
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employee', back_populates='plannings')

# Database initialization
def init_database():
    """Khởi tạo database"""
    if not os.path.exists('database.db'):
        engine = create_engine('sqlite:///database.db', echo=False)
        Base.metadata.create_all(engine)
        
        # Tạo session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Tạo dữ liệu mẫu
        create_sample_data(session)
        
        session.close()
        print("✅ Database initialized successfully!")
    
    return create_engine('sqlite:///database.db', echo=False)

def create_sample_data(session):
    """Tạo dữ liệu mẫu"""
    # Tạo một vài nhân viên mẫu
    employees_data = [
        {
            'employee_code': 'NV001',
            'full_name': 'Nguyễn Văn A',
            'date_of_birth': datetime(1985, 6, 15).date(),
            'gender': 'Nam',
            'ethnicity': 'Kinh',
            'religion': 'Không',
            'hometown': 'Hà Nội, Việt Nam',
            'position': 'Chuyên viên chính',
            'department': 'Phòng Tổ chức - Hành chính',
            'current_salary_level': 'A2',
            'current_salary_coefficient': 3.45,
            'phone': '0901234567',
            'email': 'nguyenvana@company.vn',
            'start_date': datetime(2008, 8, 1).date(),
            'organization_start_date': datetime(2015, 3, 15).date()
        },
        {
            'employee_code': 'NV002', 
            'full_name': 'Trần Thị B',
            'date_of_birth': datetime(1990, 3, 20).date(),
            'gender': 'Nữ',
            'ethnicity': 'Kinh',
            'religion': 'Phật giáo',
            'hometown': 'TP.HCM, Việt Nam',
            'position': 'Chuyên viên',
            'department': 'Phòng Tài chính - Kế toán',
            'current_salary_level': 'A1',
            'current_salary_coefficient': 2.67,
            'phone': '0901234568',
            'email': 'tranthib@company.vn',
            'start_date': datetime(2012, 4, 15).date(),
            'organization_start_date': datetime(2012, 4, 15).date()
        }
    ]
    
    for emp_data in employees_data:
        employee = Employee(**emp_data)
        # Tính ngày nghỉ hưu
        if employee.gender == 'Nam':
            retirement_age = 60
            additional_months = 3
        else:
            retirement_age = 55
            additional_months = 4
            
        retirement_date = employee.date_of_birth.replace(year=employee.date_of_birth.year + retirement_age)
        employee.retirement_date = retirement_date
        
        session.add(employee)
    
    session.commit()
    print("✅ Sample data created successfully!")
