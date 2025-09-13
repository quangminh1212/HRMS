#!/usr/bin/env python3
"""
HRMS Simple - Hệ thống Quản lý Nhân sự Đơn giản
App HRMS hoàn chỉnh nhưng không có import phức tạp
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, date
import hashlib

# Configure page
st.set_page_config(
    page_title="HRMS - Hệ thống Quản lý Nhân sự",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #14B8A6 0%, #0891B2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #14B8A6;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_database():
    """Initialize simple database."""
    conn = sqlite3.connect('hrms_simple.db')
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date DATE NOT NULL,
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Insert default admin user
    admin_password = hashlib.md5("admin123".encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    ''', ("admin", admin_password, "admin"))
    
    # Insert sample employees if empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        sample_employees = [
            ("Nguyễn Văn An", "NV001", "Phòng IT", "Lập trình viên", 15000000, "2023-01-15", "0901234567", "an@company.com"),
            ("Trần Thị Bình", "NV002", "Phòng HR", "Chuyên viên HR", 12000000, "2023-02-01", "0901234568", "binh@company.com"),
            ("Lê Văn Cường", "NV003", "Phòng Kế toán", "Kế toán viên", 11000000, "2023-03-10", "0901234569", "cuong@company.com"),
            ("Phạm Thị Dung", "NV004", "Phòng Marketing", "Marketing Manager", 18000000, "2023-01-20", "0901234570", "dung@company.com"),
            ("Hoàng Văn Em", "NV005", "Phòng IT", "System Admin", 16000000, "2023-04-05", "0901234571", "em@company.com"),
        ]
        
        cursor.executemany('''
            INSERT INTO employees (full_name, employee_id, department, position, salary, hire_date, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_employees)
    
    conn.commit()
    conn.close()

# Authentication functions
def authenticate_user(username, password):
    """Authenticate user."""
    conn = sqlite3.connect('hrms_simple.db')
    cursor = conn.cursor()
    
    password_hash = hashlib.md5(password.encode()).hexdigest()
    cursor.execute('''
        SELECT id, username, role FROM users 
        WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"id": user[0], "username": user[1], "role": user[2]}
    return None

# Initialize session state
def init_session_state():
    """Initialize session state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'

# Login page
def render_login_page():
    """Render login page."""
    st.markdown('<div class="main-header"><h1>🏢 HRMS - Hệ thống Quản lý Nhân sự</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Đăng nhập hệ thống")
        
        with st.form("login_form"):
            username = st.text_input("👤 Tên đăng nhập", placeholder="Nhập tên đăng nhập")
            password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Nhập mật khẩu")
            submit = st.form_submit_button("🚀 Đăng nhập", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Vui lòng nhập đầy đủ thông tin")
                else:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success("✅ Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error("❌ Thông tin đăng nhập không chính xác")
        
        st.info("💡 **Demo Account**: admin / admin123")

# Dashboard page
def render_dashboard():
    """Render dashboard."""
    st.markdown('<div class="main-header"><h1>📊 Dashboard - Tổng quan hệ thống</h1></div>', unsafe_allow_html=True)
    
    # Get data
    conn = sqlite3.connect('hrms_simple.db')
    df = pd.read_sql_query("SELECT * FROM employees WHERE status = 'active'", conn)
    conn.close()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Tổng nhân viên", len(df), "5")
    
    with col2:
        avg_salary = df['salary'].mean() if not df.empty else 0
        st.metric("💰 Lương trung bình", f"{avg_salary:,.0f} VNĐ", "2M")
    
    with col3:
        departments = df['department'].nunique() if not df.empty else 0
        st.metric("🏢 Số phòng ban", departments, "1")
    
    with col4:
        st.metric("📈 Hiệu suất", "95%", "3%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if not df.empty:
            dept_count = df['department'].value_counts()
            fig = px.pie(values=dept_count.values, names=dept_count.index, 
                        title="📊 Phân bố nhân viên theo phòng ban")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not df.empty:
            salary_by_dept = df.groupby('department')['salary'].mean().reset_index()
            fig = px.bar(salary_by_dept, x='department', y='salary',
                        title="💰 Lương trung bình theo phòng ban")
            st.plotly_chart(fig, use_container_width=True)

# Employee management page
def render_employee_management():
    """Render employee management."""
    st.markdown('<div class="main-header"><h1>👥 Quản lý Nhân viên</h1></div>', unsafe_allow_html=True)
    
    # Get data
    conn = sqlite3.connect('hrms_simple.db')
    df = pd.read_sql_query("SELECT * FROM employees WHERE status = 'active'", conn)
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Tìm kiếm nhân viên", placeholder="Nhập tên hoặc mã nhân viên")
    
    with col2:
        departments = ["Tất cả"] + list(df['department'].unique()) if not df.empty else ["Tất cả"]
        selected_dept = st.selectbox("🏢 Phòng ban", departments)
    
    # Filter data
    if not df.empty:
        if search_term:
            df = df[df['full_name'].str.contains(search_term, case=False, na=False) | 
                   df['employee_id'].str.contains(search_term, case=False, na=False)]
        
        if selected_dept != "Tất cả":
            df = df[df['department'] == selected_dept]
    
    # Display data
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📝 Không tìm thấy nhân viên nào")
    
    conn.close()

# Salary management page  
def render_salary_management():
    """Render salary management."""
    st.markdown('<div class="main-header"><h1>💰 Quản lý Lương</h1></div>', unsafe_allow_html=True)
    
    # Get data
    conn = sqlite3.connect('hrms_simple.db')
    df = pd.read_sql_query("SELECT * FROM employees WHERE status = 'active'", conn)
    conn.close()
    
    if not df.empty:
        # Salary statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Tổng quỹ lương", f"{df['salary'].sum():,.0f} VNĐ")
        
        with col2:
            st.metric("📊 Lương cao nhất", f"{df['salary'].max():,.0f} VNĐ")
        
        with col3:
            st.metric("📉 Lương thấp nhất", f"{df['salary'].min():,.0f} VNĐ")
        
        # Salary chart
        fig = px.histogram(df, x='salary', nbins=10, title="📊 Phân bố mức lương")
        st.plotly_chart(fig, use_container_width=True)
        
        # Salary table
        st.subheader("📋 Bảng lương nhân viên")
        salary_df = df[['full_name', 'employee_id', 'department', 'position', 'salary']].copy()
        salary_df['salary'] = salary_df['salary'].apply(lambda x: f"{x:,.0f} VNĐ")
        st.dataframe(salary_df, use_container_width=True)
    else:
        st.info("📝 Không có dữ liệu lương")

# Reports page
def render_reports():
    """Render reports page."""
    st.markdown('<div class="main-header"><h1>📈 Báo cáo & Thống kê</h1></div>', unsafe_allow_html=True)
    
    # Get data
    conn = sqlite3.connect('hrms_simple.db')
    df = pd.read_sql_query("SELECT * FROM employees WHERE status = 'active'", conn)
    conn.close()
    
    if not df.empty:
        # Department analysis
        st.subheader("🏢 Phân tích theo phòng ban")
        dept_stats = df.groupby('department').agg({
            'full_name': 'count',
            'salary': ['mean', 'sum']
        }).round(0)
        
        dept_stats.columns = ['Số nhân viên', 'Lương TB', 'Tổng lương']
        st.dataframe(dept_stats, use_container_width=True)
        
        # Position analysis
        st.subheader("💼 Phân tích theo vị trí")
        position_stats = df.groupby('position').agg({
            'full_name': 'count',
            'salary': 'mean'
        }).round(0)
        
        position_stats.columns = ['Số người', 'Lương TB']
        st.dataframe(position_stats, use_container_width=True)
    else:
        st.info("📝 Không có dữ liệu để tạo báo cáo")

# Main app
def main():
    """Main application."""
    # Initialize
    init_database()
    init_session_state()
    
    # Check authentication
    if not st.session_state.authenticated:
        render_login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👋 Xin chào, {st.session_state.user['username']}!")
        
        pages = {
            "📊 Dashboard": "dashboard",
            "👥 Quản lý Nhân viên": "employees", 
            "💰 Quản lý Lương": "salary",
            "📈 Báo cáo": "reports"
        }
        
        for page_name, page_key in pages.items():
            if st.button(page_name, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Render current page
    if st.session_state.current_page == "dashboard":
        render_dashboard()
    elif st.session_state.current_page == "employees":
        render_employee_management()
    elif st.session_state.current_page == "salary":
        render_salary_management()
    elif st.session_state.current_page == "reports":
        render_reports()

if __name__ == "__main__":
    main()
