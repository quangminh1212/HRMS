#!/usr/bin/env python3
"""
XLAB HRMS Utilities Testing Suite

Comprehensive testing for utility functions.
Following international testing standards.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock

from src.utils.utils import (
    calculate_retirement_date,
    check_salary_increase_eligibility,
    calculate_seniority_allowance,
    calculate_months_difference
)
from src.models.models_enhanced import Employee, GenderEnum


class TestRetirementCalculations:
    """Test suite for retirement-related calculations."""
    
    def test_male_retirement_age(self):
        """Test retirement age calculation for males."""
        birth_date = date(1980, 5, 15)
        retirement_date = calculate_retirement_date(birth_date, GenderEnum.MALE)
        expected_date = date(2042, 5, 15)  # 62 years old
        
        assert retirement_date == expected_date
    
    def test_female_retirement_age(self):
        """Test retirement age calculation for females."""
        birth_date = date(1980, 5, 15)
        retirement_date = calculate_retirement_date(birth_date, GenderEnum.FEMALE)
        expected_date = date(2040, 5, 15)  # 60 years old
        
        assert retirement_date == expected_date
    
    def test_leap_year_retirement(self):
        """Test retirement calculation for leap year birthdays."""
        birth_date = date(1980, 2, 29)  # Leap year
        retirement_date = calculate_retirement_date(birth_date, GenderEnum.MALE)
        expected_date = date(2042, 2, 28)  # Non-leap year, adjusted
        
        assert retirement_date == expected_date
    
    @pytest.mark.parametrize("birth_year,gender,expected_retirement_year", [
        (1960, GenderEnum.MALE, 2022),
        (1960, GenderEnum.FEMALE, 2020),
        (1990, GenderEnum.MALE, 2052),
        (1990, GenderEnum.FEMALE, 2050),
    ])
    def test_retirement_year_parametrized(self, birth_year, gender, expected_retirement_year):
        """Parametrized test for various retirement scenarios."""
        birth_date = date(birth_year, 1, 1)
        retirement_date = calculate_retirement_date(birth_date, gender)
        
        assert retirement_date.year == expected_retirement_year


class TestSalaryCalculations:
    """Test suite for salary-related calculations."""
    
    def create_mock_employee(self, position: str, salary_date: date, 
                           start_date: date = None) -> Mock:
        """Create mock employee for testing."""
        employee = Mock(spec=Employee)
        employee.position = position
        employee.current_salary_date = salary_date
        employee.organization_start_date = start_date or salary_date
        return employee
    
    def test_salary_increase_eligibility_chuyenvien(self):
        """Test salary increase eligibility for Chuyên viên (36 months)."""
        # Employee eligible (over 36 months)
        employee = self.create_mock_employee(
            "Chuyên viên",
            date(2021, 1, 1)  # Over 36 months ago
        )
        
        eligible, months = check_salary_increase_eligibility(employee)
        assert eligible is True
        assert months >= 36
    
    def test_salary_increase_eligibility_nhanvien(self):
        """Test salary increase eligibility for Nhân viên (24 months)."""
        # Employee eligible (over 24 months)
        employee = self.create_mock_employee(
            "Nhân viên",
            date(2022, 1, 1)  # Over 24 months ago
        )
        
        eligible, months = check_salary_increase_eligibility(employee)
        assert eligible is True
        assert months >= 24
    
    def test_salary_increase_not_eligible(self):
        """Test employee not eligible for salary increase."""
        # Recent salary increase
        employee = self.create_mock_employee(
            "Chuyên viên",
            date(2024, 1, 1)  # Too recent
        )
        
        eligible, months = check_salary_increase_eligibility(employee)
        assert eligible is False
    
    def test_seniority_allowance_calculation(self):
        """Test seniority allowance calculation."""
        employee = Mock(spec=Employee)
        employee.current_salary_date = date(2020, 1, 1)  # 4+ years ago
        employee.current_salary_coefficient = 4.5  # Above 4.0 threshold
        employee.position = "Chuyên viên"
        
        allowance = calculate_seniority_allowance(employee)
        
        # Should get base 5% plus additional years
        assert allowance >= 5.0  # At least 5%
        assert allowance <= 20.0  # Reasonable upper limit
    
    def test_seniority_allowance_not_eligible(self):
        """Test employee not eligible for seniority allowance."""
        employee = Mock(spec=Employee)
        employee.current_salary_date = date(2023, 1, 1)  # Too recent
        employee.current_salary_coefficient = 3.0  # Below threshold
        employee.position = "Nhân viên"
        
        allowance = calculate_seniority_allowance(employee)
        assert allowance == 0.0


class TestDateUtilities:
    """Test suite for date utility functions."""
    
    def test_months_difference_same_year(self):
        """Test months difference calculation within same year."""
        start_date = date(2023, 1, 15)
        end_date = date(2023, 6, 20)
        
        months = calculate_months_difference(start_date, end_date)
        assert months == 5
    
    def test_months_difference_across_years(self):
        """Test months difference calculation across years."""
        start_date = date(2022, 10, 1)
        end_date = date(2023, 3, 1)
        
        months = calculate_months_difference(start_date, end_date)
        assert months == 5
    
    def test_months_difference_multiple_years(self):
        """Test months difference calculation for multiple years."""
        start_date = date(2020, 1, 1)
        end_date = date(2023, 1, 1)
        
        months = calculate_months_difference(start_date, end_date)
        assert months == 36
    
    def test_months_difference_negative(self):
        """Test months difference with end date before start date."""
        start_date = date(2023, 6, 1)
        end_date = date(2023, 1, 1)
        
        months = calculate_months_difference(start_date, end_date)
        assert months == -5


class TestErrorHandling:
    """Test suite for error handling in utility functions."""
    
    def test_retirement_with_none_values(self):
        """Test retirement calculation with None values."""
        with pytest.raises((TypeError, AttributeError)):
            calculate_retirement_date(None, GenderEnum.MALE)
    
    def test_salary_eligibility_with_none_employee(self):
        """Test salary eligibility with None employee."""
        with pytest.raises(AttributeError):
            check_salary_increase_eligibility(None)
    
    def test_salary_eligibility_with_none_dates(self):
        """Test salary eligibility with None dates."""
        employee = Mock(spec=Employee)
        employee.current_salary_date = None
        employee.organization_start_date = None
        employee.position = "Chuyên viên"
        
        eligible, months = check_salary_increase_eligibility(employee)
        assert eligible is False
        assert months == 0  # Or appropriate default value


class TestPerformance:
    """Performance tests for utility functions."""
    
    def test_retirement_calculation_performance(self):
        """Test performance of retirement calculations."""
        import time
        
        birth_dates = [date(1980 + i, 1, 1) for i in range(100)]
        
        start_time = time.time()
        
        for birth_date in birth_dates:
            calculate_retirement_date(birth_date, GenderEnum.MALE)
        
        execution_time = time.time() - start_time
        
        # Should calculate 100 retirement dates in under 0.1 seconds
        assert execution_time < 0.1
    
    def test_salary_calculations_performance(self):
        """Test performance of salary calculations."""
        import time
        
        employees = []
        for i in range(100):
            employee = self.create_mock_employee(
                "Chuyên viên",
                date(2020 + (i % 4), 1, 1)
            )
            employees.append(employee)
        
        start_time = time.time()
        
        for employee in employees:
            check_salary_increase_eligibility(employee)
        
        execution_time = time.time() - start_time
        
        # Should process 100 employees in under 0.1 seconds
        assert execution_time < 0.1


if __name__ == "__main__":
    pytest.main([__file__])
