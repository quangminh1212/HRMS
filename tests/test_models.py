#!/usr/bin/env python3
"""
XLAB HRMS Models Testing Suite

Comprehensive testing for database models and operations.
Following international testing standards.
"""

import pytest
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models_enhanced import (
    Base, Employee, Education, WorkHistory, SalaryHistory,
    GenderEnum, EducationLevelEnum, WorkStatusEnum
)
from src.models.models import User


class TestEmployeeModel:
    """Test suite for Employee model."""
    
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    @pytest.fixture
    def sample_employee(self):
        """Create sample employee for testing."""
        return Employee(
            full_name="Nguyễn Văn Test",
            date_of_birth=date(1990, 1, 1),
            gender=GenderEnum.MALE,
            ethnicity="Kinh",
            hometown="Hà Nội",
            position="Chuyên viên",
            department="Phòng IT",
            education_level=EducationLevelEnum.BACHELOR,
            work_status=WorkStatusEnum.ACTIVE,
            current_salary_coefficient=3.5,
            current_salary_level=5,
            current_salary_date=date(2023, 1, 1),
            organization_start_date=date(2022, 1, 1),
            social_insurance_start_date=date(2022, 1, 1),
            phone="0123456789",
            email="test@company.com"
        )
    
    def test_employee_creation(self, db_session, sample_employee):
        """Test employee creation and persistence."""
        db_session.add(sample_employee)
        db_session.commit()
        
        retrieved = db_session.query(Employee).filter_by(
            full_name="Nguyễn Văn Test"
        ).first()
        
        assert retrieved is not None
        assert retrieved.full_name == "Nguyễn Văn Test"
        assert retrieved.gender == GenderEnum.MALE
        assert retrieved.position == "Chuyên viên"
    
    def test_employee_validation(self):
        """Test employee model validation."""
        # Test required fields
        employee = Employee()
        
        # Should not raise error for optional fields
        assert employee.full_name is None
        assert employee.date_of_birth is None
    
    def test_employee_relationships(self, db_session, sample_employee):
        """Test employee relationships with other models."""
        db_session.add(sample_employee)
        db_session.commit()
        
        # Add education record
        education = Education(
            employee_id=sample_employee.id,
            level=EducationLevelEnum.BACHELOR,
            field_of_study="Computer Science",
            institution="University of Technology",
            country="Vietnam"
        )
        
        db_session.add(education)
        db_session.commit()
        
        # Test relationship
        assert len(sample_employee.education_records) == 1
        assert sample_employee.education_records[0].field_of_study == "Computer Science"


class TestUserModel:
    """Test suite for User model."""
    
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        engine = create_engine("sqlite:///:memory:")
        # Import and create User table
        from src.models.models import Base as UserBase
        UserBase.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    def test_user_creation(self, db_session):
        """Test user creation and authentication."""
        user = User(
            username="testuser",
            full_name="Test User",
            role="admin"
        )
        user.set_password("testpassword123")
        
        db_session.add(user)
        db_session.commit()
        
        retrieved = db_session.query(User).filter_by(username="testuser").first()
        
        assert retrieved is not None
        assert retrieved.username == "testuser"
        assert retrieved.check_password("testpassword123") is True
        assert retrieved.check_password("wrongpassword") is False


class TestModelPerformance:
    """Performance tests for database models."""
    
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    def test_bulk_employee_operations(self, db_session):
        """Test bulk operations performance."""
        import time
        
        # Create 100 employees
        employees = []
        start_time = time.time()
        
        for i in range(100):
            employee = Employee(
                full_name=f"Employee {i}",
                date_of_birth=date(1990, 1, 1),
                gender=GenderEnum.MALE if i % 2 == 0 else GenderEnum.FEMALE,
                position=f"Position {i}",
                department="Test Department",
                current_salary_coefficient=3.0 + (i * 0.01)
            )
            employees.append(employee)
        
        db_session.add_all(employees)
        db_session.commit()
        
        creation_time = time.time() - start_time
        
        # Query performance test
        start_time = time.time()
        all_employees = db_session.query(Employee).all()
        query_time = time.time() - start_time
        
        assert len(all_employees) == 100
        assert creation_time < 5.0  # Should create 100 employees in under 5 seconds
        assert query_time < 1.0     # Should query 100 employees in under 1 second


if __name__ == "__main__":
    pytest.main([__file__])
