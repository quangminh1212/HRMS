"""
Database Models cho HRMS
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Model cho người dùng hệ thống"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    """Model cho nhân viên"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))  # Nam/Nữ
    ethnicity = db.Column(db.String(30))  # Dân tộc
    religion = db.Column(db.String(30))  # Tôn giáo
    hometown = db.Column(db.String(200))  # Quê quán
    
    # Thông tin công việc
    position = db.Column(db.String(100))  # Chức vụ
    department = db.Column(db.String(100))  # Đơn vị
    party_join_date = db.Column(db.Date)  # Ngày vào Đảng
    political_theory_level = db.Column(db.String(50))  # Trình độ lý luận chính trị
    professional_level = db.Column(db.String(200))  # Trình độ chuyên môn
    
    # Thông tin lương
    current_salary_level = db.Column(db.String(20))  # Ngạch lương
    current_salary_coefficient = db.Column(db.Float)  # Hệ số lương
    last_salary_increase_date = db.Column(db.Date)  # Ngày nâng lương gần nhất
    position_allowance = db.Column(db.Float, default=0)  # Phụ cấp chức vụ
    
    # Thông tin liên hệ
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    
    # Thông tin công tác
    start_date = db.Column(db.Date)  # Ngày bắt đầu công tác
    organization_start_date = db.Column(db.Date)  # Ngày vào cơ quan
    retirement_date = db.Column(db.Date)  # Ngày nghỉ hưu dự kiến
    status = db.Column(db.String(20), default='active')  # active, retired, leave, studying
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    salary_history = db.relationship('SalaryHistory', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    work_history = db.relationship('WorkHistory', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    trainings = db.relationship('Training', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    evaluations = db.relationship('Evaluation', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    contracts = db.relationship('Contract', backref='employee', lazy='dynamic', cascade='all, delete-orphan')

class SalaryHistory(db.Model):
    """Lịch sử lương"""
    __tablename__ = 'salary_history'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    salary_level = db.Column(db.String(20))
    salary_coefficient = db.Column(db.Float)
    effective_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reason = db.Column(db.String(200))
    decision_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WorkHistory(db.Model):
    """Quá trình công tác"""
    __tablename__ = 'work_history'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Training(db.Model):
    """Đào tạo, bồi dưỡng"""
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    training_type = db.Column(db.String(50))  # Đại học, Sau đại học, LLCT, QPAN, QLNN, etc.
    training_name = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    country = db.Column(db.String(50), default='Việt Nam')
    degree = db.Column(db.String(100))
    major = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    certificate_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    """Thành tích, khen thưởng"""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    achievement_type = db.Column(db.String(100))  # Danh hiệu thi đua, Huân chương, Bằng khen, etc.
    achievement_name = db.Column(db.String(200))
    level = db.Column(db.String(50))  # Cấp Nhà nước, Cấp Bộ, Cấp Tỉnh, etc.
    date = db.Column(db.Date)
    decision_number = db.Column(db.String(50))
    issuing_authority = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Evaluation(db.Model):
    """Đánh giá hàng năm"""
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(50))  # Xuất sắc, Tốt, Hoàn thành, Không hoàn thành
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'year', name='_employee_year_uc'),
    )

class Contract(db.Model):
    """Hợp đồng lao động"""
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    contract_number = db.Column(db.String(50), unique=True)
    contract_type = db.Column(db.String(50))  # Không xác định thời hạn, Có thời hạn, Thử việc
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    salary = db.Column(db.Float)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, expired, terminated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PlanningCandidate(db.Model):
    """Quy hoạch cán bộ"""
    __tablename__ = 'planning_candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    planning_position = db.Column(db.String(100))  # Vị trí quy hoạch
    planning_period = db.Column(db.String(20))  # Giai đoạn (2020-2025)
    planning_year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='planning_positions')

class InsuranceRecord(db.Model):
    """Bảo hiểm xã hội"""
    __tablename__ = 'insurance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    insurance_type = db.Column(db.String(50))  # BHXH, BHYT, BHTN
    insurance_number = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    monthly_salary = db.Column(db.Float)
    contribution_rate = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='insurance_records')
