"""
Model tests for HRMS.
"""
import pytest
from datetime import datetime, date
from models import User, Employee, SalaryHistory, WorkHistory
from utils import calculate_retirement_date


class TestUserModel:
    """Test User model functionality."""
    
    def test_user_creation(self, app_context):
        """Test creating a new user."""
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpassword')
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.check_password('testpassword')
        assert not user.check_password('wrongpassword')
    
    def test_user_password_hashing(self, app_context):
        """Test password hashing functionality."""
        user = User(username='testuser', email='test@example.com')
        user.set_password('secret')
        
        assert user.password_hash is not None
        assert user.password_hash != 'secret'
        assert user.check_password('secret')


class TestEmployeeModel:
    """Test Employee model functionality."""
    
    def test_employee_creation(self, app_context):
        """Test creating a new employee."""
        employee = Employee(
            employee_code='NV001',
            full_name='Nguyễn Văn A',
            date_of_birth=date(1990, 1, 1),
            gender='Nam',
            position='Chuyên viên',
            department='IT',
            start_date=date(2020, 1, 1),
            current_salary_level='A1',
            current_salary_coefficient=2.34,
            status='active'
        )
        
        assert employee.employee_code == 'NV001'
        assert employee.full_name == 'Nguyễn Văn A'
        assert employee.gender == 'Nam'
        assert employee.status == 'active'
    
    def test_retirement_date_calculation(self, app_context):
        """Test retirement date calculation."""
        # Male employee born in 1990
        male_birth_date = date(1990, 1, 1)
        male_retirement = calculate_retirement_date(male_birth_date, 'Nam')
        
        # Should retire at 60 years + 3 months
        assert male_retirement.year == 2050
        assert male_retirement.month >= 4  # January + 3 months
        
        # Female employee born in 1990
        female_birth_date = date(1990, 1, 1)
        female_retirement = calculate_retirement_date(female_birth_date, 'Nữ')
        
        # Should retire at 55 years + 4 months
        assert female_retirement.year == 2045
        assert female_retirement.month >= 5  # January + 4 months


class TestSalaryHistoryModel:
    """Test SalaryHistory model functionality."""
    
    def test_salary_history_creation(self, app_context):
        """Test creating salary history record."""
        history = SalaryHistory(
            employee_id=1,
            salary_level='A1',
            salary_coefficient=2.34,
            effective_date=date(2020, 1, 1),
            end_date=date(2023, 1, 1),
            reason='Nâng lương định kỳ',
            decision_number='QD-001/2020'
        )
        
        assert history.salary_level == 'A1'
        assert history.salary_coefficient == 2.34
        assert history.reason == 'Nâng lương định kỳ'


class TestWorkHistoryModel:
    """Test WorkHistory model functionality."""
    
    def test_work_history_creation(self, app_context):
        """Test creating work history record."""
        work = WorkHistory(
            employee_id=1,
            position='Chuyên viên',
            department='IT',
            organization='Công ty ABC',
            start_date=date(2018, 1, 1),
            end_date=date(2020, 1, 1),
            description='Làm việc tại phòng IT'
        )
        
        assert work.position == 'Chuyên viên'
        assert work.department == 'IT'
        assert work.organization == 'Công ty ABC'
