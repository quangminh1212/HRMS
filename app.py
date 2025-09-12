"""
HRMS - Hệ thống Quản lý Nhân sự
Human Resource Management System

Main application module containing all routes and business logic.
"""

import os
import logging
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config
from models import db, Employee, User, SalaryHistory, WorkHistory, Training, Achievement, Contract
from utils import calculate_retirement_date, check_salary_increase_eligibility, export_to_word, export_to_excel

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Trang chủ"""
    if current_user.is_authenticated:
        # Thống kê nhanh
        total_employees = Employee.query.filter_by(status='active').count()
        retiring_soon = Employee.query.filter(
            Employee.retirement_date <= datetime.now() + timedelta(days=180),
            Employee.status == 'active'
        ).count()
        
        # Cảnh báo nâng lương
        salary_alerts = []
        employees = Employee.query.filter_by(status='active').all()
        for emp in employees:
            if check_salary_increase_eligibility(emp):
                salary_alerts.append(emp)
        
        return render_template('dashboard.html', 
                             total_employees=total_employees,
                             retiring_soon=retiring_soon,
                             salary_alerts=len(salary_alerts[:5]))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Đăng xuất"""
    logout_user()
    flash('Đã đăng xuất thành công!', 'info')
    return redirect(url_for('login'))

@app.route('/employees')
@login_required
def employees():
    """Danh sách nhân sự"""
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    
    query = Employee.query
    
    if search:
        query = query.filter(
            db.or_(
                Employee.full_name.contains(search),
                Employee.employee_code.contains(search)
            )
        )
    
    if department:
        query = query.filter_by(department=department)
    
    employees = query.all()
    departments = db.session.query(Employee.department).distinct().all()
    
    return render_template('employees.html', 
                         employees=employees, 
                         departments=[d[0] for d in departments if d[0]])

@app.route('/employee/<int:id>')
@login_required
def employee_detail(id):
    """Chi tiết nhân sự"""
    employee = Employee.query.get_or_404(id)
    salary_history = SalaryHistory.query.filter_by(employee_id=id).order_by(SalaryHistory.effective_date.desc()).all()
    work_history = WorkHistory.query.filter_by(employee_id=id).order_by(WorkHistory.start_date.desc()).all()
    trainings = Training.query.filter_by(employee_id=id).order_by(Training.start_date.desc()).all()
    achievements = Achievement.query.filter_by(employee_id=id).order_by(Achievement.date.desc()).all()
    
    return render_template('employee_detail.html', 
                         employee=employee,
                         salary_history=salary_history,
                         work_history=work_history,
                         trainings=trainings,
                         achievements=achievements)

@app.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """Thêm nhân sự mới"""
    if request.method == 'POST':
        employee = Employee(
            employee_code=request.form.get('employee_code'),
            full_name=request.form.get('full_name'),
            date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d'),
            gender=request.form.get('gender'),
            ethnicity=request.form.get('ethnicity'),
            religion=request.form.get('religion'),
            hometown=request.form.get('hometown'),
            position=request.form.get('position'),
            department=request.form.get('department'),
            party_join_date=datetime.strptime(request.form.get('party_join_date'), '%Y-%m-%d') if request.form.get('party_join_date') else None,
            political_theory_level=request.form.get('political_theory_level'),
            professional_level=request.form.get('professional_level'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'),
            current_salary_level=request.form.get('current_salary_level'),
            current_salary_coefficient=float(request.form.get('current_salary_coefficient', 0)),
            status='active'
        )
        
        # Tính ngày nghỉ hưu
        employee.retirement_date = calculate_retirement_date(employee.date_of_birth, employee.gender)
        
        db.session.add(employee)
        db.session.commit()
        
        flash('Thêm nhân sự thành công!', 'success')
        return redirect(url_for('employee_detail', id=employee.id))
    
    return render_template('employee_form.html', employee=None)

@app.route('/employee/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """Sửa thông tin nhân sự"""
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        employee.full_name = request.form.get('full_name')
        employee.position = request.form.get('position')
        employee.department = request.form.get('department')
        employee.phone = request.form.get('phone')
        employee.email = request.form.get('email')
        employee.political_theory_level = request.form.get('political_theory_level')
        employee.professional_level = request.form.get('professional_level')
        
        db.session.commit()
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('employee_detail', id=employee.id))
    
    return render_template('employee_form.html', employee=employee)

@app.route('/salary-management')
@login_required
def salary_management():
    """Quản lý nâng lương"""
    # Lấy danh sách nhân viên đủ điều kiện nâng lương
    eligible_employees = []
    employees = Employee.query.filter_by(status='active').all()
    
    for emp in employees:
        if check_salary_increase_eligibility(emp):
            # Tính toán thông tin nâng lương
            months_since_last = 0
            if emp.last_salary_increase_date:
                months_since_last = (datetime.now() - emp.last_salary_increase_date).days // 30
            
            eligible_employees.append({
                'employee': emp,
                'months_since_last': months_since_last,
                'next_level': emp.current_salary_level,
                'next_coefficient': emp.current_salary_coefficient + 0.1
            })
    
    return render_template('salary_management.html', eligible_employees=eligible_employees)

@app.route('/process-salary-increase', methods=['POST'])
@login_required
def process_salary_increase():
    """Xử lý nâng lương"""
    employee_ids = request.form.getlist('employee_ids')
    
    for emp_id in employee_ids:
        employee = Employee.query.get(emp_id)
        if employee:
            # Lưu lịch sử lương cũ
            salary_history = SalaryHistory(
                employee_id=employee.id,
                salary_level=employee.current_salary_level,
                salary_coefficient=employee.current_salary_coefficient,
                effective_date=employee.last_salary_increase_date or employee.start_date,
                end_date=datetime.now()
            )
            db.session.add(salary_history)
            
            # Cập nhật lương mới
            employee.current_salary_coefficient += 0.1
            employee.last_salary_increase_date = datetime.now()
            
    db.session.commit()
    flash(f'Đã xử lý nâng lương cho {len(employee_ids)} nhân viên!', 'success')
    
    # Xuất quyết định nâng lương
    return redirect(url_for('salary_management'))

@app.route('/retirement-management')
@login_required
def retirement_management():
    """Quản lý nghỉ hưu"""
    # Nhân viên sắp nghỉ hưu (trong 6 tháng tới)
    retiring_soon = Employee.query.filter(
        Employee.retirement_date <= datetime.now() + timedelta(days=180),
        Employee.retirement_date >= datetime.now(),
        Employee.status == 'active'
    ).order_by(Employee.retirement_date).all()
    
    return render_template('retirement_management.html', 
                         retiring_employees=retiring_soon,
                         now=datetime.now())

@app.route('/contracts')
@login_required
def contracts():
    """Quản lý hợp đồng"""
    contracts = Contract.query.all()
    return render_template('contracts.html', contracts=contracts)

@app.route('/reports')
@login_required
def reports():
    """Báo cáo thống kê"""
    # Thống kê tổng quan
    stats = {
        'total_active': Employee.query.filter_by(status='active').count(),
        'total_retired': Employee.query.filter_by(status='retired').count(),
        'by_gender': {
            'male': Employee.query.filter_by(gender='Nam', status='active').count(),
            'female': Employee.query.filter_by(gender='Nữ', status='active').count()
        },
        'by_department': {}
    }
    
    # Thống kê theo phòng ban
    departments = db.session.query(
        Employee.department, 
        db.func.count(Employee.id)
    ).filter_by(status='active').group_by(Employee.department).all()
    
    for dept, count in departments:
        if dept:
            stats['by_department'][dept] = count
    
    return render_template('reports.html', stats=stats)

@app.route('/export/<export_type>/<int:employee_id>')
@login_required
def export_document(export_type, employee_id):
    """Xuất tài liệu Word/Excel"""
    employee = Employee.query.get_or_404(employee_id)
    
    if export_type == 'word':
        file_path = export_to_word(employee)
    elif export_type == 'excel':
        file_path = export_to_excel([employee])
    else:
        flash('Loại xuất file không hợp lệ!', 'danger')
        return redirect(url_for('employee_detail', id=employee_id))
    
    return send_file(file_path, as_attachment=True)

@app.route('/api/search-employees')
@login_required
def api_search_employees():
    """API tìm kiếm nhân viên"""
    query = request.args.get('q', '')
    employees = Employee.query.filter(
        Employee.full_name.contains(query)
    ).limit(10).all()
    
    results = []
    for emp in employees:
        results.append({
            'id': emp.id,
            'name': emp.full_name,
            'code': emp.employee_code,
            'department': emp.department,
            'position': emp.position
        })
    
    return jsonify(results)

# Application factory pattern - app is configured in run.py
