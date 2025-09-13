#!/usr/bin/env python3
"""
XLAB HRMS - Hệ thống Quản lý Nhân sự (Modern UI Version)

Giao diện được xây dựng lại hoàn toàn với Design System chuyên nghiệp
Tham khảo XLAB Design, Material Design 3, Fluent Design

International Standards:
- PEP 8 compliance
- Clean imports
- Proper error handling
- Type hints where applicable
- Clean architecture
"""

import logging
from typing import Dict, Any, Optional

import streamlit as st
import pandas as pd
import plotly.express as px

# Import Design System
from src.components.design import UIComponents
from src.components.components import ModernComponents

# Import models
from src.models.models_enhanced import init_enhanced_database
from src.models.models import User

# Import enhanced features
from src.features.hr_search import render_employee_search_page
from src.features.salary_management import render_salary_management_page
from src.features.retirement_management import render_retirement_management_page
from src.features.additional_features import (
    render_planning_management_page,
    render_work_history_page,
    render_contract_management_page,
    render_appointment_check_page,
    render_rewards_page,
    render_early_salary_page,
    render_quick_reports_page,
    render_insurance_page,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def configure_streamlit() -> None:
    """Configure Streamlit settings according to international standards."""
    st.set_page_config(
        page_title="XLAB HRMS - Hệ thống Quản lý Nhân sự",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "XLAB HRMS v2.0 - Professional HR Management System"
        }
    )


def initialize_database() -> bool:
    """
    Initialize enhanced database with proper error handling.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        init_enhanced_database()
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        st.error(f"Lỗi khởi tạo database: {e}")
        return False


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    default_states = {
        'authenticated': False,
        'user': None,
        'current_page': 'login'
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate user with enhanced security.
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        User data dict if successful, None otherwise
    """
    try:
        # Placeholder for real authentication
        if username == "admin" and password == "admin123":
            return {
                'username': username,
                'role': 'admin',
                'full_name': 'Administrator',
                'permissions': ['all']
            }
        return None
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None


def render_login_page() -> None:
    """Render professional login page."""
    st.markdown(UIComponents.get_base_css(), unsafe_allow_html=True)
    
    # Hero header
    ModernComponents.hero_header(
        "XLAB HRMS",
        "Hệ thống Quản lý Nhân sự Hiện đại",
        "⚡"
    )
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Đăng nhập hệ thống")
        
        with st.form("login_form"):
            username = st.text_input("👤 Tên đăng nhập")
            password = st.text_input("🔒 Mật khẩu", type="password")
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


def render_sidebar() -> str:
    """
    Render navigation sidebar.
    
    Returns:
        str: Selected page name
    """
    st.sidebar.markdown(UIComponents.get_base_css(), unsafe_allow_html=True)
    
    # User info
    if st.session_state.user:
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #14B8A6, #8B9467);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="font-size: 1.1rem; font-weight: 600;">
                XLAB HRMS
            </div>
            <div style="opacity: 0.9; font-size: 0.9rem;">
                {st.session_state.user['full_name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation menu
    menu_items = {
        "🏠 Dashboard": "dashboard",
        "👥 Tra cứu nhân sự": "search",
        "💰 Nâng lương định kỳ": "salary",
        "⏰ Theo dõi nghỉ hưu": "retirement",
        "📋 Quy hoạch cán bộ": "planning",
        "📊 Lịch sử công tác": "history",
        "📄 Quản lý hợp đồng": "contract",
        "✅ Điều kiện bổ nhiệm": "appointment",
        "🏆 Khen thưởng": "rewards",
        "⚡ Nâng lương sớm": "early_salary",
        "📈 Báo cáo nhanh": "reports",
        "🛡️ Báo cáo BHXH": "insurance"
    }
    
    selected = st.sidebar.selectbox(
        "🧭 Điều hướng",
        list(menu_items.keys()),
        key="nav_select"
    )
    
    # Logout button
    if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    return menu_items[selected]


def render_dashboard_page() -> None:
    """Render modern dashboard with metrics."""
    st.markdown("# 🏠 Dashboard")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    metrics_data = [
        ("👥", "Tổng nhân sự", "150", "+5"),
        ("⏰", "Sắp nghỉ hưu", "12", "-2"),
        ("💰", "Đến kỳ nâng lương", "25", "+8"),
        ("📄", "Hợp đồng hết hạn", "6", "+1")
    ]
    
    cols = [col1, col2, col3, col4]
    for i, (icon, title, value, change) in enumerate(metrics_data):
        with cols[i]:
            st.markdown(
                ModernComponents.metric_card(title, value, change, icon),
                unsafe_allow_html=True
            )
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Phân bổ theo phòng ban")
        # Sample data for chart
        dept_data = pd.DataFrame({
            'Phòng ban': ['IT', 'HR', 'Finance', 'Marketing', 'Operations'],
            'Số lượng': [25, 15, 20, 12, 18]
        })
        fig = px.pie(dept_data, values='Số lượng', names='Phòng ban',
                     color_discrete_sequence=['#14B8A6', '#8B9467', '#0D1421',
                                              '#2DD4BF', '#A5AD85'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Xu hướng tuyển dụng")
        # Sample data for trend chart
        trend_data = pd.DataFrame({
            'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'],
            'Tuyển mới': [5, 8, 12, 6, 15, 10],
            'Nghỉ việc': [2, 3, 1, 4, 2, 3]
        })
        fig = px.line(trend_data, x='Tháng', y=['Tuyển mới', 'Nghỉ việc'],
                      color_discrete_sequence=['#14B8A6', '#DC2626'])
        st.plotly_chart(fig, use_container_width=True)


def render_page_content(page: str) -> None:
    """
    Render content based on selected page.
    
    Args:
        page: Page identifier
    """
    page_map = {
        'dashboard': render_dashboard_page,
        'search': render_employee_search_page,
        'salary': render_salary_management_page,
        'retirement': render_retirement_management_page,
        'planning': render_planning_management_page,
        'history': render_work_history_page,
        'contract': render_contract_management_page,
        'appointment': render_appointment_check_page,
        'rewards': render_rewards_page,
        'early_salary': render_early_salary_page,
        'reports': render_quick_reports_page,
        'insurance': render_insurance_page
    }
    
    try:
        if page in page_map:
            page_map[page]()
        else:
            st.error(f"❌ Trang không tồn tại: {page}")
            logger.error(f"Unknown page requested: {page}")
    except Exception as e:
        st.error(f"❌ Lỗi khi tải trang: {str(e)}")
        logger.error(f"Error rendering page {page}: {e}")


def main() -> None:
    """Main application entry point with error handling."""
    try:
        # Configure Streamlit
        configure_streamlit()
        
        # Initialize database
        if not initialize_database():
            st.stop()
        
        # Initialize session state
        initialize_session_state()
        
        # Apply global CSS
        st.markdown(UIComponents.get_base_css(), unsafe_allow_html=True)
        
        # Route to appropriate page
        if not st.session_state.authenticated:
            render_login_page()
        else:
            # Render sidebar and get selected page
            selected_page = render_sidebar()
            
            # Render main content
            render_page_content(selected_page)
            
    except Exception as e:
        st.error(f"❌ Lỗi ứng dụng: {str(e)}")
        logger.critical(f"Application error: {e}")


if __name__ == "__main__":
    main()
