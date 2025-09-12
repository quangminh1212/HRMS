"""
HRMS - Hệ thống Quản lý Nhân sự (Streamlit Version)
Frontend và Backend 100% Python
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
from io import BytesIO
import os

# Import models và utils
from models_streamlit import init_database, Employee, User, SalaryHistory, WorkHistory, Training, Achievement, Evaluation, Council, Insurance, Planning
from utils_streamlit import (
    calculate_retirement_date, 
    check_salary_increase_eligibility,
    check_appointment_eligibility,
    export_employee_word,
    export_salary_decision,
    calculate_seniority_allowance
)

# Cấu hình trang
st.set_page_config(
    page_title="HRMS - Quản lý Nhân sự",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .employee-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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

# Hàm đăng nhập
def login_page():
    st.markdown('<div class="main-header"><h1>🏢 HRMS - Hệ thống Quản lý Nhân sự</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Đăng nhập hệ thống")
        
        with st.form("login_form"):
            username = st.text_input("👤 Tên đăng nhập", placeholder="admin")
            password = st.text_input("🔒 Mật khẩu", type="password", placeholder="admin123")
            submit = st.form_submit_button("Đăng nhập", use_container_width=True)
            
            if submit:
                # Đăng nhập đơn giản (có thể mở rộng với database)
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.success("✅ Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
        
        st.markdown("---")
        st.info("**Tài khoản mặc định:**\n- Tên đăng nhập: admin\n- Mật khẩu: admin123")

# Main app
def main_app():
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👋 Xin chào, {st.session_state.current_user}!")
        
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        
        st.markdown("---")
        
        # Menu chính
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
        
        selected_menu = st.selectbox("🧭 Chọn chức năng:", menu_options)
        st.session_state.current_page = selected_menu
    
    # Main content area
    if st.session_state.current_page == "🏠 Trang chủ":
        dashboard_page()
    elif st.session_state.current_page == "👥 Tra cứu nhân sự":
        employee_search_page()
    elif st.session_state.current_page == "💰 Nâng lương định kỳ":
        salary_management_page()
    elif st.session_state.current_page == "⏰ Theo dõi nghỉ hưu":
        retirement_page()
    elif st.session_state.current_page == "📋 Kiểm tra quy hoạch":
        planning_page()
    elif st.session_state.current_page == "💼 Quá trình công tác":
        work_history_page()
    elif st.session_state.current_page == "📄 Hợp đồng lao động":
        contract_page()
    elif st.session_state.current_page == "✅ Điều kiện bổ nhiệm":
        appointment_page()
    elif st.session_state.current_page == "🏆 Điều kiện khen thưởng":
        award_page()
    elif st.session_state.current_page == "⚡ Nâng lương trước hạn":
        early_salary_page()
    elif st.session_state.current_page == "📊 Báo cáo thống kê":
        reports_page()
    elif st.session_state.current_page == "🏥 Báo bảo hiểm":
        insurance_page()

# Dashboard page
def dashboard_page():
    st.markdown('<div class="main-header"><h1>🏠 Bảng điều khiển HRMS</h1></div>', unsafe_allow_html=True)
    
    # Thống kê tổng quan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("👥 Tổng nhân sự", "150", "5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⏰ Sắp nghỉ hưu", "12", "-2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💰 Đến kỳ nâng lương", "25", "8")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📄 Hợp đồng hết hạn", "6", "1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Biểu đồ
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Cơ cấu theo độ tuổi")
        age_data = pd.DataFrame({
            'Độ tuổi': ['<30', '30-40', '40-50', '50-60', '>60'],
            'Số lượng': [25, 45, 40, 30, 10]
        })
        fig1 = px.bar(age_data, x='Độ tuổi', y='Số lượng', color='Số lượng')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Cơ cấu theo giới tính")
        gender_data = pd.DataFrame({
            'Giới tính': ['Nam', 'Nữ'],
            'Số lượng': [85, 65]
        })
        fig2 = px.pie(gender_data, names='Giới tính', values='Số lượng')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Cảnh báo nhanh
    st.subheader("⚠️ Cảnh báo và nhắc nhở")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-box">
            <h4>💰 Nâng lương sắp tới</h4>
            <p>Có 25 nhân viên đủ điều kiện nâng lương trong quý này.</p>
            <small>Cần xử lý trước ngày 15/12/2024</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>⏰ Nghỉ hưu</h4>
            <p>12 nhân viên sẽ nghỉ hưu trong 6 tháng tới.</p>
            <small>Cần chuẩn bị thủ tục</small>
        </div>
        """, unsafe_allow_html=True)

# Tra cứu nhân sự page
def employee_search_page():
    st.markdown('<div class="main-header"><h1>👥 Tra cứu thông tin nhân sự</h1></div>', unsafe_allow_html=True)
    
    # Tìm kiếm
    search_term = st.text_input("🔍 Nhập tên nhân viên cần tìm:", placeholder="VD: Nguyễn Văn A")
    
    if search_term:
        # Giả lập dữ liệu tìm kiếm
        st.success(f"✅ Tìm thấy nhân viên: **{search_term}**")
        
        # Tabs chi tiết
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Thông tin cơ bản", "💼 Công việc", "💰 Lương & Phụ cấp", "🎓 Đào tạo", "🏆 Thành tích"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👤 Thông tin cá nhân")
                st.write("**Mã nhân viên:** NV001")
                st.write("**Họ tên:** Nguyễn Văn A")
                st.write("**Ngày sinh:** 15/06/1985")
                st.write("**Giới tính:** Nam")
                st.write("**Dân tộc:** Kinh")
                st.write("**Tôn giáo:** Không")
                st.write("**Quê quán:** Hà Nội, Việt Nam")
            
            with col2:
                st.markdown("### 📞 Liên hệ")
                st.write("**Điện thoại:** 0901234567")
                st.write("**Email:** nguyenvana@company.vn")
                st.write("**Địa chỉ:** 123 Phố Huế, Hà Nội")
        
        with tab2:
            st.markdown("### 💼 Thông tin công việc")
            st.write("**Chức vụ:** Chuyên viên chính")
            st.write("**Đơn vị:** Phòng Tổ chức - Hành chính")
            st.write("**Ngày vào Đảng:** 10/05/2010")
            st.write("**Trình độ LLCT:** Trung cấp")
            st.write("**Trình độ chuyên môn:** Cử nhân Luật, Đại học Luật Hà Nội")
            st.write("**Ngày bắt đầu công tác:** 01/08/2008")
            st.write("**Ngày vào cơ quan:** 15/03/2015")
            st.write("**Ngày nghỉ hưu dự kiến:** 15/09/2048")
        
        with tab3:
            st.markdown("### 💰 Thông tin lương")
            st.write("**Ngạch lương:** A2")
            st.write("**Hệ số lương:** 3.45")
            st.write("**Phụ cấp chức vụ:** 0.5")
            st.write("**Ngày nâng lương gần nhất:** 01/04/2021")
            
            # Cảnh báo nâng lương
            st.markdown("""
            <div class="success-box">
                <h4>✅ Đủ điều kiện nâng lương</h4>
                <p>Nhân viên đã đủ 36 tháng kể từ lần nâng lương gần nhất.</p>
                <p><strong>Dự kiến nâng lên:</strong> Hệ số 3.66</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### 🎓 Đào tạo & Bồi dưỡng")
            training_data = pd.DataFrame({
                'Loại': ['Đại học', 'LLCT Trung cấp', 'Ngoại ngữ'],
                'Tên khóa học': ['Cử nhân Luật', 'Lý luận chính trị', 'Tiếng Anh B1'],
                'Cơ sở': ['ĐH Luật Hà Nội', 'Học viện Chính trị', 'Trung tâm Ngoại ngữ'],
                'Thời gian': ['2003-2007', '2010-2012', '2020-2021']
            })
            st.dataframe(training_data, use_container_width=True)
        
        with tab5:
            st.markdown("### 🏆 Thành tích & Khen thưởng")
            achievement_data = pd.DataFrame({
                'Loại': ['Lao động tiên tiến', 'Bằng khen', 'Chiến sỹ thi đua'],
                'Tên/Danh hiệu': ['Lao động tiên tiến 2023', 'Bằng khen Thủ tướng', 'Chiến sỹ thi đua cơ sở'],
                'Cấp': ['Cơ quan', 'Nhà nước', 'Cơ quan'],
                'Ngày': ['15/11/2023', '20/08/2022', '01/05/2021']
            })
            st.dataframe(achievement_data, use_container_width=True)
        
        # Nút thao tác
        st.markdown("---")
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

# Các page khác sẽ được implement tương tự...
def salary_management_page():
    st.markdown('<div class="main-header"><h1>💰 Quản lý nâng lương định kỳ</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def retirement_page():
    st.markdown('<div class="main-header"><h1>⏰ Theo dõi nghỉ hưu</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def planning_page():
    st.markdown('<div class="main-header"><h1>📋 Kiểm tra quy hoạch</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def work_history_page():
    st.markdown('<div class="main-header"><h1>💼 Quá trình công tác</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def contract_page():
    st.markdown('<div class="main-header"><h1>📄 Hợp đồng lao động</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def appointment_page():
    st.markdown('<div class="main-header"><h1>✅ Điều kiện bổ nhiệm</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def award_page():
    st.markdown('<div class="main-header"><h1>🏆 Điều kiện khen thưởng</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def early_salary_page():
    st.markdown('<div class="main-header"><h1>⚡ Nâng lương trước thời hạn</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def reports_page():
    st.markdown('<div class="main-header"><h1>📊 Báo cáo thống kê</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

def insurance_page():
    st.markdown('<div class="main-header"><h1>🏥 Báo bảo hiểm</h1></div>', unsafe_allow_html=True)
    st.info("Chức năng đang được phát triển...")

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
