"""
Basic application tests for HRMS.
"""
import pytest
from app import app


class TestBasicFunctionality:
    """Test basic application functionality."""
    
    def test_app_exists(self):
        """Test that the app is created."""
        assert app is not None
    
    def test_app_in_testing_mode(self, client):
        """Test that app is in testing mode."""
        assert app.config['TESTING']
    
    def test_login_page(self, client):
        """Test login page loads."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'HỆ THỐNG QUẢN LÝ NHÂN SỰ' in response.data
    
    def test_login_redirect(self, client):
        """Test that unauthenticated users are redirected to login."""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_valid_login(self, client):
        """Test login with valid credentials."""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'dashboard' in response.data or b'Trang chủ' in response.data
    
    def test_invalid_login(self, client):
        """Test login with invalid credentials."""
        response = client.post('/login', data={
            'username': 'invalid',
            'password': 'invalid'
        })
        assert response.status_code == 200
        assert b'không đúng' in response.data or b'login' in response.data
    
    def test_logout(self, authenticated_user):
        """Test logout functionality."""
        response = authenticated_user.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'login' in response.data


class TestEmployeeRoutes:
    """Test employee-related routes."""
    
    def test_employees_page_requires_auth(self, client):
        """Test that employees page requires authentication."""
        response = client.get('/employees')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_employees_page_authenticated(self, authenticated_user):
        """Test employees page with authentication."""
        response = authenticated_user.get('/employees')
        assert response.status_code == 200
        assert b'Danh sách nhân sự' in response.data
    
    def test_add_employee_page(self, authenticated_user):
        """Test add employee page."""
        response = authenticated_user.get('/employee/add')
        assert response.status_code == 200
        assert b'Thêm nhân sự mới' in response.data


class TestSalaryRoutes:
    """Test salary-related routes."""
    
    def test_salary_management_requires_auth(self, client):
        """Test salary management requires authentication."""
        response = client.get('/salary-management')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_salary_management_authenticated(self, authenticated_user):
        """Test salary management with authentication."""
        response = authenticated_user.get('/salary-management')
        assert response.status_code == 200
        assert b'nâng lương' in response.data


class TestRetirementRoutes:
    """Test retirement-related routes."""
    
    def test_retirement_management_requires_auth(self, client):
        """Test retirement management requires authentication."""
        response = client.get('/retirement-management')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_retirement_management_authenticated(self, authenticated_user):
        """Test retirement management with authentication."""
        response = authenticated_user.get('/retirement-management')
        assert response.status_code == 200
        assert b'nghỉ hưu' in response.data


class TestReportsRoutes:
    """Test reports-related routes."""
    
    def test_reports_requires_auth(self, client):
        """Test reports requires authentication."""
        response = client.get('/reports')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_reports_authenticated(self, authenticated_user):
        """Test reports with authentication."""
        response = authenticated_user.get('/reports')
        assert response.status_code == 200
        assert b'Báo cáo' in response.data
