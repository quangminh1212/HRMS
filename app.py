#!/usr/bin/env python3
"""
HRMS - Hệ thống Quản lý Nhân sự (Modern UI Version)
Giao diện được xây dựng lại hoàn toàn với Design System chuyên nghiệp
Tham khảo Material Design 3, Fluent Design, Ant Design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
from io import BytesIO
import os

# Import Design System
from design import DesignTokens, UIComponents

# Import models và utils
from models import init_database, Employee, User, SalaryHistory, WorkHistory, Training, Achievement, Evaluation, Council, Insurance, Planning
from utils import (
    calculate_retirement_date, 
    check_salary_increase_eligibility,
    check_appointment_eligibility,
    export_employee_word,
    export_salary_decision,
    calculate_seniority_allowance
)

# Import additional modern pages
from pages import ModernPages

# Import components
from components import ModernComponents

# Import enhanced features  
from hr_search import render_employee_search_page
from salary_management import render_salary_management_page
from retirement_management import render_retirement_management_page
from additional_features import (
    render_planning_management_page,
    render_work_history_page,
    render_contract_management_page,
    render_appointment_check_page,
    render_rewards_page,
    render_early_salary_page,
    render_quick_reports_page,
    render_insurance_page
)

# Cấu hình trang với theme hiện đại
st.set_page_config(
    page_title="HRMS - Hệ thống Quản lý Nhân sự",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/hrms',
        'Report a bug': "https://github.com/your-repo/hrms/issues",
        'About': "HRMS - Hệ thống Quản lý Nhân sự hiện đại với Python"
    }
)

# Apply Design System CSS
st.markdown(UIComponents.get_base_css(), unsafe_allow_html=True)

# Khởi tạo database
@st.cache_resource
def init_db():
    return init_database()

# Khởi tạo session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Trang chủ"

# Components đã được chuyển sang components.py để tránh circular import

# Login Page với Modern Design
def login_page():
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    ModernComponents.hero_header(
        "HRMS", 
        "Hệ thống Quản lý Nhân sự Hiện đại",
        "🏢"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(ModernComponents.surface_container("""
            <div style="padding: 2rem;">
                <div class="title-large" style="text-align: center; margin-bottom: 2rem; color: #1C1B1F;">
                    🔐 Đăng nhập hệ thống
                </div>
            </div>
        """, "container-highest"), unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "👤 Tên đăng nhập", 
                placeholder="admin",
                help="Sử dụng tài khoản demo: admin"
            )
            password = st.text_input(
                "🔒 Mật khẩu", 
                type="password", 
                placeholder="admin123",
                help="Mật khẩu demo: admin123"
            )
            
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit = st.form_submit_button(
                    "🚀 Đăng nhập", 
                    use_container_width=True,
                    help="Nhấn để truy cập hệ thống"
                )
            
            if submit:
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.success("✅ Đăng nhập thành công! Đang chuyển hướng...")
                    st.rerun()
                else:
                    st.error("❌ Thông tin đăng nhập không chính xác!")
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        # Demo credentials info
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Thông tin đăng nhập demo",
            "Username: admin | Password: admin123",
            "Sử dụng thông tin này để truy cập hệ thống demo"
        ), unsafe_allow_html=True)

# Main Dashboard với Modern Design
def dashboard_page():
    ModernComponents.hero_header(
        "Bảng điều khiển",
        "Tổng quan hệ thống quản lý nhân sự",
        "📊"
    )
    
    # Modern Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("👥", "Tổng nhân sự", "150", "+5", "icon-primary"),
        ("⏰", "Sắp nghỉ hưu", "12", "-2", "icon-warning"), 
        ("💰", "Đến kỳ nâng lương", "25", "+8", "icon-success"),
        ("📄", "Hợp đồng hết hạn", "6", "+1", "icon-error")
    ]
    
    cols = [col1, col2, col3, col4]
    for i, (icon, title, value, change, color_class) in enumerate(metrics_data):
        with cols[i]:
            st.markdown(
                ModernComponents.metric_card(icon, title, value, change, color_class),
                unsafe_allow_html=True
            )
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    # Charts Section với Modern Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(ModernComponents.surface_container("""
            <div style="padding: 1.5rem;">
                <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                    📊 Cơ cấu theo độ tuổi
                </div>
            </div>
        """, "container"), unsafe_allow_html=True)
        
        # Create beautiful chart
        age_data = pd.DataFrame({
            'Độ tuổi': ['<30', '30-40', '40-50', '50-60', '>60'],
            'Số lượng': [25, 45, 40, 30, 10]
        })
        
        fig1 = px.bar(
            age_data, 
            x='Độ tuổi', 
            y='Số lượng',
            color='Số lượng',
            color_continuous_scale='Viridis',
            title=""
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', 
            font_family="Inter",
            font_color="#1C1B1F",
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown(ModernComponents.surface_container("""
            <div style="padding: 1.5rem;">
                <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                    🎯 Cơ cấu theo giới tính
                </div>
            </div>
        """, "container"), unsafe_allow_html=True)
        
        gender_data = pd.DataFrame({
            'Giới tính': ['Nam', 'Nữ'],
            'Số lượng': [85, 65]
        })
        
        fig2 = px.pie(
            gender_data, 
            names='Giới tính', 
            values='Số lượng',
            color_discrete_sequence=['#6750A4', '#7F67BE'],
            title=""
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Inter",
            font_color="#1C1B1F"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    # Alerts Section
    st.markdown(ModernComponents.surface_container("""
        <div style="padding: 1.5rem;">
            <div class="title-large" style="margin-bottom: 1.5rem; color: #1C1B1F;">
                ⚠️ Cảnh báo và nhắc nhở
            </div>
        </div>
    """, "container"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(ModernComponents.modern_alert(
            "warning",
            "Nâng lương sắp tới",
            "25 nhân viên đủ điều kiện nâng lương trong quý này",
            "📅 Cần xử lý trước ngày 15/12/2024"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(ModernComponents.modern_alert(
            "info", 
            "Nghỉ hưu",
            "12 nhân viên sẽ nghỉ hưu trong 6 tháng tới",
            "📋 Cần chuẩn bị thủ tục và hồ sơ"
        ), unsafe_allow_html=True)

# Old employee_search_page() removed - using enhanced hr_search.py module

# Main App với Modern Sidebar
def main_app():
    # Modern Sidebar với Glass effect
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👋</div>
            <div class="title-medium" style="color: #1C1B1F;">Xin chào, {st.session_state.current_user}!</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # Modern Menu
        menu_options = [
            "🏠 Trang chủ",
            "👥 Tra cứu nhân sự",
            "💰 Nâng lương định kỳ", 
            "⏰ Theo dõi nghỉ hưu",
            "📋 Kiểm tra quy hoạch",
            "💼 Quá trình công tác",
            "📄 Hợp đồng lao động",
            "✅ Điều kiện bổ nhiệm",
            "🏆 Điều kiện khen thưởng",
            "⚡ Nâng lương trước hạn",
            "📊 Báo cáo thống kê",
            "🏥 Báo bảo hiểm"
        ]
        
        selected_menu = st.selectbox(
            "🧭 Chọn chức năng:",
            menu_options,
            help="Chọn chức năng để điều hướng"
        )
        st.session_state.current_page = selected_menu
    
    # Main Content với animation
    if st.session_state.current_page == "🏠 Trang chủ":
        dashboard_page()
    elif st.session_state.current_page == "👥 Tra cứu nhân sự":
        render_employee_search_page()
    elif st.session_state.current_page == "💰 Nâng lương định kỳ":
        render_salary_management_page()
    elif st.session_state.current_page == "⏰ Theo dõi nghỉ hưu":
        render_retirement_management_page()
    elif st.session_state.current_page == "📊 Báo cáo thống kê":
        render_quick_reports_page()
    elif st.session_state.current_page == "📋 Kiểm tra quy hoạch":
        render_planning_management_page()
    elif st.session_state.current_page == "💼 Quá trình công tác":
        render_work_history_page()
    elif st.session_state.current_page == "📄 Hợp đồng lao động":
        render_contract_management_page()
    elif st.session_state.current_page == "✅ Điều kiện bổ nhiệm":
        render_appointment_check_page()
    elif st.session_state.current_page == "🏆 Điều kiện khen thưởng":
        render_rewards_page()
    elif st.session_state.current_page == "⚡ Nâng lương trước hạn":
        render_early_salary_page()
    elif st.session_state.current_page == "🏥 Báo bảo hiểm":
        render_insurance_page()
    else:
        # Placeholder cho các trang khác
        ModernComponents.hero_header(
            "Đang phát triển",
            f"Chức năng {st.session_state.current_page} sẽ được cập nhật sớm",
            "🚧"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "warning",
            "Tính năng đang được hoàn thiện", 
            f"Chức năng {st.session_state.current_page} đang trong quá trình phát triển và sẽ được cập nhật trong phiên bản tiếp theo.",
            "💡 Vui lòng sử dụng các tính năng khác đã hoàn thành"
        ), unsafe_allow_html=True)

# Main execution
def main():
    init_db()
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
