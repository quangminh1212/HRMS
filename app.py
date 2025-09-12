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

# Components hiện đại
class ModernComponents:
    
    @staticmethod
    def hero_header(title: str, subtitle: str, icon: str = "🏢"):
        """Hero header với glassmorphism effect"""
        st.markdown(f"""
        <div class="hero-header animate-fade-scale">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod 
    def metric_card(icon: str, title: str, value: str, change: str = None, color_class: str = "icon-primary"):
        """Modern metric card với hover effects"""
        change_html = ""
        if change:
            change_color = "#4CAF50" if change.startswith("+") else "#F44336" 
            change_html = f'<div style="color: {change_color}; font-weight: 500; font-size: 0.875rem;">{change}</div>'
        
        return f"""
        <div class="metric-card animate-slide-up">
            <div class="icon-container {color_class}">{icon}</div>
            <div class="title-large" style="color: #1C1B1F; margin: 0 0 0.5rem 0;">{value}</div>
            <div class="body-large" style="color: #49454F; margin: 0 0 0.5rem 0;">{title}</div>
            {change_html}
        </div>
        """
    
    @staticmethod
    def modern_alert(type: str, title: str, content: str, details: str = None):
        """Modern alert box với icons"""
        icons = {
            "warning": "⚡",
            "success": "✅", 
            "info": "💡",
            "error": "❌"
        }
        
        icon = icons.get(type, "💡")
        details_html = f'<div class="label-medium" style="opacity: 0.8; margin-top: 0.5rem;"><i>{details}</i></div>' if details else ""
        
        return f"""
        <div class="alert alert-{type} animate-slide-up">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="flex: 1;">
                    <div class="title-medium" style="margin: 0 0 0.5rem 0;">{title}</div>
                    <div class="body-medium" style="margin: 0;">{content}</div>
                    {details_html}
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def surface_container(content: str, level: str = "container"):
        """Surface container với different elevation levels"""
        return f"""
        <div class="surface-{level} animate-fade-scale">
            {content}
        </div>
        """
    
    @staticmethod
    def data_table(df: pd.DataFrame, title: str = None):
        """Modern data table với styling"""
        if title:
            st.markdown(f'<div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">{title}</div>', unsafe_allow_html=True)
        
        # Style the dataframe
        styled_df = df.style.set_properties(**{
            'background-color': 'rgba(255, 255, 255, 0.95)',
            'color': '#1C1B1F',
            'border': '1px solid rgba(255, 255, 255, 0.2)',
            'padding': '8px 12px',
            'font-family': 'Inter'
        })
        
        st.dataframe(styled_df, use_container_width=True)

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

# Employee Search Page với Modern Design
def employee_search_page():
    ModernComponents.hero_header(
        "Tra cứu nhân sự",
        "Tìm kiếm và quản lý thông tin nhân viên",
        "👥"
    )
    
    # Modern Search Section
    st.markdown(ModernComponents.surface_container("""
        <div style="padding: 1.5rem;">
            <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                🔍 Tìm kiếm nhân viên
            </div>
        </div>
    """, "container-high"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "Nhập tên nhân viên",
            placeholder="VD: Nguyễn Văn A",
            help="Nhập tên để tìm kiếm thông tin nhân viên"
        )
    
    with col2:
        st.markdown('<div style="height: 1.75rem;"></div>', unsafe_allow_html=True)
        search_button = st.button("🔍 Tìm kiếm", use_container_width=True)
    
    if search_term and search_button:
        # Success message
        st.markdown(ModernComponents.modern_alert(
            "success",
            "Tìm kiếm thành công",
            f"Đã tìm thấy thông tin nhân viên: {search_term}",
            "Hiển thị kết quả chi tiết bên dưới"
        ), unsafe_allow_html=True)
        
        # Modern Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Thông tin cơ bản", 
            "💼 Công việc", 
            "💰 Lương & Phụ cấp", 
            "🎓 Đào tạo", 
            "🏆 Thành tích"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(ModernComponents.surface_container("""
                    <div style="padding: 1.5rem;">
                        <div class="title-medium" style="margin-bottom: 1rem; color: #1C1B1F;">
                            👤 Thông tin cá nhân
                        </div>
                        <div class="body-medium" style="line-height: 1.8; color: #49454F;">
                            <strong>Mã nhân viên:</strong> NV001<br>
                            <strong>Họ tên:</strong> Nguyễn Văn A<br>
                            <strong>Ngày sinh:</strong> 15/06/1985<br>
                            <strong>Giới tính:</strong> Nam<br>
                            <strong>Dân tộc:</strong> Kinh<br>
                            <strong>Tôn giáo:</strong> Không<br>
                            <strong>Quê quán:</strong> Hà Nội, Việt Nam
                        </div>
                    </div>
                """, "container"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(ModernComponents.surface_container("""
                    <div style="padding: 1.5rem;">
                        <div class="title-medium" style="margin-bottom: 1rem; color: #1C1B1F;">
                            📞 Thông tin liên hệ
                        </div>
                        <div class="body-medium" style="line-height: 1.8; color: #49454F;">
                            <strong>Điện thoại:</strong> 0901234567<br>
                            <strong>Email:</strong> nguyenvana@company.vn<br>
                            <strong>Địa chỉ:</strong> 123 Phố Huế, Hà Nội
                        </div>
                    </div>
                """, "container"), unsafe_allow_html=True)
        
        with tab2:
            st.markdown(ModernComponents.surface_container("""
                <div style="padding: 1.5rem;">
                    <div class="title-medium" style="margin-bottom: 1rem; color: #1C1B1F;">
                        💼 Thông tin công việc
                    </div>
                    <div class="body-medium" style="line-height: 1.8; color: #49454F;">
                        <strong>Chức vụ:</strong> Chuyên viên chính<br>
                        <strong>Đơn vị:</strong> Phòng Tổ chức - Hành chính<br>
                        <strong>Ngày vào Đảng:</strong> 10/05/2010<br>
                        <strong>Trình độ LLCT:</strong> Trung cấp<br>
                        <strong>Trình độ chuyên môn:</strong> Cử nhân Luật, Đại học Luật Hà Nội<br>
                        <strong>Ngày bắt đầu công tác:</strong> 01/08/2008<br>
                        <strong>Ngày vào cơ quan:</strong> 15/03/2015<br>
                        <strong>Ngày nghỉ hưu dự kiến:</strong> 15/09/2048
                    </div>
                </div>
            """, "container"), unsafe_allow_html=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(ModernComponents.surface_container("""
                    <div style="padding: 1.5rem;">
                        <div class="title-medium" style="margin-bottom: 1rem; color: #1C1B1F;">
                            💰 Thông tin lương hiện tại
                        </div>
                        <div class="body-medium" style="line-height: 1.8; color: #49454F;">
                            <strong>Ngạch lương:</strong> A2<br>
                            <strong>Hệ số lương:</strong> 3.45<br>
                            <strong>Phụ cấp chức vụ:</strong> 0.5<br>
                            <strong>Ngày nâng lương gần nhất:</strong> 01/04/2021
                        </div>
                    </div>
                """, "container"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(ModernComponents.modern_alert(
                    "success",
                    "Đủ điều kiện nâng lương",
                    "Nhân viên đã đủ 36 tháng kể từ lần nâng lương gần nhất",
                    "🔼 Dự kiến nâng lên hệ số: 3.66"
                ), unsafe_allow_html=True)
        
        with tab4:
            training_data = pd.DataFrame({
                'Loại': ['Đại học', 'LLCT Trung cấp', 'Ngoại ngữ'],
                'Tên khóa học': ['Cử nhân Luật', 'Lý luận chính trị', 'Tiếng Anh B1'],
                'Cơ sở': ['ĐH Luật Hà Nội', 'Học viện Chính trị', 'Trung tâm Ngoại ngữ'],
                'Thời gian': ['2003-2007', '2010-2012', '2020-2021']
            })
            ModernComponents.data_table(training_data, "🎓 Lịch sử đào tạo & bồi dưỡng")
        
        with tab5:
            achievement_data = pd.DataFrame({
                'Loại': ['Lao động tiên tiến', 'Bằng khen', 'Chiến sỹ thi đua'],
                'Tên/Danh hiệu': ['Lao động tiên tiến 2023', 'Bằng khen Thủ tướng', 'Chiến sỹ thi đua cơ sở'],
                'Cấp': ['Cơ quan', 'Nhà nước', 'Cơ quan'],
                'Ngày': ['15/11/2023', '20/08/2022', '01/05/2021']
            })
            ModernComponents.data_table(achievement_data, "🏆 Thành tích & khen thưởng")
        
        # Action buttons
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Xuất file Word", use_container_width=True):
                st.success("✅ Đã xuất file Word thành công!")
        
        with col2:
            if st.button("⏰ Kiểm tra nghỉ hưu", use_container_width=True):
                st.info("ℹ️ Nhân viên nghỉ hưu vào: 15/09/2048 (còn 24 năm)")
        
        with col3:
            if st.button("💰 Kiểm tra nâng lương", use_container_width=True):
                st.success("✅ Đủ điều kiện nâng lương!")

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
        employee_search_page()
    elif st.session_state.current_page == "💰 Nâng lương định kỳ":
        ModernPages.salary_management_page()
    elif st.session_state.current_page == "⏰ Theo dõi nghỉ hưu":
        ModernPages.retirement_tracking_page()
    elif st.session_state.current_page == "📊 Báo cáo thống kê":
        ModernPages.reports_dashboard()
    elif st.session_state.current_page == "📋 Kiểm tra quy hoạch":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện",
            "Trang kiểm tra quy hoạch cán bộ sẽ được cập nhật trong phiên bản tiếp theo",
            "🚧 Đang phát triển thêm tính năng nâng cao"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "💼 Quá trình công tác":
        st.markdown(ModernComponents.modern_alert(
            "info", 
            "Chức năng đang hoàn thiện",
            "Trang quá trình công tác sẽ được cập nhật trong phiên bản tiếp theo",
            "🚧 Đang tích hợp timeline và workflow"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "📄 Hợp đồng lao động":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện", 
            "Trang hợp đồng lao động sẽ được cập nhật trong phiên bản tiếp theo",
            "🚧 Đang phát triển quản lý hợp đồng điện tử"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "✅ Điều kiện bổ nhiệm":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện",
            "Trang kiểm tra điều kiện bổ nhiệm sẽ được cập nhật trong phiên bản tiếp theo", 
            "🚧 Đang tích hợp AI để tự động kiểm tra điều kiện"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "🏆 Điều kiện khen thưởng":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện",
            "Trang điều kiện khen thưởng sẽ được cập nhật trong phiên bản tiếp theo",
            "🚧 Đang phát triển hệ thống đánh giá tự động"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "⚡ Nâng lương trước hạn":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện", 
            "Trang nâng lương trước hạn do thành tích sẽ được cập nhật trong phiên bản tiếp theo",
            "🚧 Đang tích hợp workflow phê duyệt"
        ), unsafe_allow_html=True)
    elif st.session_state.current_page == "🏥 Báo bảo hiểm":
        st.markdown(ModernComponents.modern_alert(
            "info",
            "Chức năng đang hoàn thiện",
            "Trang báo bảo hiểm xã hội sẽ được cập nhật trong phiên bản tiếp theo", 
            "🚧 Đang tích hợp API Bảo hiểm xã hội"
        ), unsafe_allow_html=True)
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
