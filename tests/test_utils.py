"""
Utility function tests for HRMS.
"""
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock
from utils import (
    calculate_retirement_date,
    check_salary_increase_eligibility,
    calculate_insurance_contribution,
    check_planning_eligibility
)


class TestRetirementCalculation:
    """Test retirement date calculation functions."""
    
    def test_male_retirement_date(self):
        """Test retirement date calculation for male employees."""
        birth_date = date(1990, 6, 15)
        retirement_date = calculate_retirement_date(birth_date, 'Nam')
        
        # Male: 60 years + 3 months
        expected_year = 1990 + 60
        expected_month = 6 + 3
        
        assert retirement_date.year == expected_year
        assert retirement_date.month == expected_month
        assert retirement_date.day == 15
    
    def test_female_retirement_date(self):
        """Test retirement date calculation for female employees."""
        birth_date = date(1985, 3, 10)
        retirement_date = calculate_retirement_date(birth_date, 'Nữ')
        
        # Female: 55 years + 4 months
        expected_year = 1985 + 55
        expected_month = 3 + 4
        
        assert retirement_date.year == expected_year
        assert retirement_date.month == expected_month
        assert retirement_date.day == 10


class TestSalaryIncrease:
    """Test salary increase eligibility functions."""
    
    def test_eligible_for_salary_increase(self):
        """Test employee eligible for salary increase."""
        # Create mock employee - Chuyên viên with 36+ months since last increase
        employee = Mock()
        employee.current_salary_level = 'Chuyên viên'
        employee.last_salary_increase_date = date(2020, 1, 1)  # 3+ years ago
        employee.start_date = date(2018, 1, 1)
        
        result = check_salary_increase_eligibility(employee)
        assert result == True
    
    def test_not_eligible_for_salary_increase(self):
        """Test employee not eligible for salary increase."""
        # Create mock employee - recently increased salary
        employee = Mock()
        employee.current_salary_level = 'Chuyên viên'
        employee.last_salary_increase_date = datetime.now().date() - timedelta(days=180)  # 6 months ago
        employee.start_date = date(2020, 1, 1)
        
        result = check_salary_increase_eligibility(employee)
        assert result == False
    
    def test_new_employee_not_eligible(self):
        """Test new employee without salary history."""
        # Create mock employee - new employee
        employee = Mock()
        employee.current_salary_level = 'Chuyên viên'
        employee.last_salary_increase_date = None
        employee.start_date = datetime.now().date() - timedelta(days=180)  # 6 months ago
        
        result = check_salary_increase_eligibility(employee)
        assert result == False


class TestInsuranceCalculation:
    """Test insurance contribution calculation."""
    
    def test_social_insurance_calculation(self):
        """Test social insurance contribution calculation."""
        salary = 10000000  # 10 million VND
        result = calculate_insurance_contribution(salary, 'BHXH')
        
        expected_employee = salary * 0.08  # 8%
        expected_employer = salary * 0.175  # 17.5%
        
        assert result['employee'] == expected_employee
        assert result['employer'] == expected_employer
        assert result['total'] == expected_employee + expected_employer
    
    def test_health_insurance_calculation(self):
        """Test health insurance contribution calculation."""
        salary = 10000000  # 10 million VND
        result = calculate_insurance_contribution(salary, 'BHYT')
        
        expected_employee = salary * 0.015  # 1.5%
        expected_employer = salary * 0.03   # 3%
        
        assert result['employee'] == expected_employee
        assert result['employer'] == expected_employer
    
    def test_unemployment_insurance_calculation(self):
        """Test unemployment insurance contribution calculation."""
        salary = 10000000  # 10 million VND
        result = calculate_insurance_contribution(salary, 'BHTN')
        
        expected_employee = salary * 0.01  # 1%
        expected_employer = salary * 0.01  # 1%
        
        assert result['employee'] == expected_employee
        assert result['employer'] == expected_employer
    
    def test_invalid_insurance_type(self):
        """Test invalid insurance type."""
        salary = 10000000
        result = calculate_insurance_contribution(salary, 'INVALID')
        
        assert result is None


class TestPlanningEligibility:
    """Test planning eligibility functions."""
    
    def test_eligible_for_planning(self):
        """Test employee eligible for planning."""
        employee = Mock()
        employee.date_of_birth = date(1985, 1, 1)  # 38 years old
        employee.professional_level = 'Cử nhân Đại học Kinh tế'
        employee.start_date = date(2015, 1, 1)  # 8+ years experience
        employee.political_theory_level = 'Trung cấp'
        
        result = check_planning_eligibility(employee, 'Trưởng phòng')
        
        assert result['is_eligible'] == True
        assert result['age_valid'] == True
        assert result['education_valid'] == True
        assert result['experience_valid'] == True
        assert result['political_valid'] == True
    
    def test_too_old_for_planning(self):
        """Test employee too old for planning."""
        employee = Mock()
        employee.date_of_birth = date(1960, 1, 1)  # 64 years old
        employee.professional_level = 'Cử nhân Đại học'
        employee.start_date = date(1985, 1, 1)
        employee.political_theory_level = 'Cao cấp'
        
        result = check_planning_eligibility(employee, 'Trưởng phòng')
        
        assert result['is_eligible'] == False
        assert result['age_valid'] == False
    
    def test_insufficient_education(self):
        """Test employee with insufficient education."""
        employee = Mock()
        employee.date_of_birth = date(1985, 1, 1)
        employee.professional_level = 'Trung cấp'  # Not university level
        employee.start_date = date(2015, 1, 1)
        employee.political_theory_level = 'Trung cấp'
        
        result = check_planning_eligibility(employee, 'Phó phòng')
        
        assert result['is_eligible'] == False
        assert result['education_valid'] == False
