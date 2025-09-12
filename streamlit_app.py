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
    
    # Tabs cho các chức năng con
    tab1, tab2, tab3 = st.tabs(["📅 Lịch cảnh báo", "👥 Danh sách nâng lương", "📄 Xuất file"])
    
    with tab1:
        st.subheader("📅 Lịch cảnh báo nâng lương")
        
        # Hiển thị lịch cảnh báo theo quý
        current_year = datetime.now().year
        alert_schedule = [
            {"quarter": "Q1", "alert_date": "15/02", "review_date": "31/03", "status": "completed" if datetime.now().month > 3 else "upcoming"},
            {"quarter": "Q2", "alert_date": "15/05", "review_date": "30/06", "status": "completed" if datetime.now().month > 6 else "upcoming"},
            {"quarter": "Q3", "alert_date": "15/08", "review_date": "30/09", "status": "completed" if datetime.now().month > 9 else "upcoming"},
            {"quarter": "Q4", "alert_date": "15/11", "review_date": "31/12", "status": "completed" if datetime.now().month > 12 else "upcoming"}
        ]
        
        for schedule in alert_schedule:
            status_icon = "✅" if schedule["status"] == "completed" else "⏰"
            status_color = "success" if schedule["status"] == "completed" else "info"
            
            st.markdown(f"""
            <div class="{'success-box' if schedule['status'] == 'completed' else 'warning-box'}">
                <h4>{status_icon} {schedule['quarter']}/{current_year}</h4>
                <p><strong>Cảnh báo:</strong> {schedule['alert_date']}/{current_year}</p>
                <p><strong>Xét nâng lương:</strong> {schedule['review_date']}/{current_year}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        **📋 Quy tắc nâng lương thường xuyên:**
        - **Chuyên viên và tương đương trở lên**: 36 tháng
        - **Nhân viên, Thủ quỹ**: 24 tháng
        - **Phụ cấp thâm niên vượt khung**: 5% (năm đầu) + 1%/năm tiếp theo
        
        **📖 Căn cứ pháp lý:** Thông tư 08/2013/TT-BNV
        """)
    
    with tab2:
        st.subheader("👥 Danh sách nhân viên đủ điều kiện nâng lương")
        
        # Bộ lọc
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_department = st.selectbox("🏢 Lọc theo đơn vị", 
                ["Tất cả", "Phòng Tổ chức - Hành chính", "Phòng Tài chính - Kế toán", "Phòng Kinh doanh"])
        
        with col2:
            filter_position = st.selectbox("💼 Lọc theo chức vụ",
                ["Tất cả", "Chuyên viên cao cấp", "Chuyên viên chính", "Chuyên viên", "Nhân viên"])
        
        with col3:
            filter_level = st.selectbox("📊 Lọc theo ngạch",
                ["Tất cả", "A1", "A2", "A3", "B1", "B2", "B3"])
        
        if st.button("🔍 Tính toán danh sách", use_container_width=True):
            # Dữ liệu mẫu - trong thực tế sẽ query từ database
            eligible_employees = [
                {
                    "name": "Nguyễn Văn A",
                    "position": "Chuyên viên chính", 
                    "department": "Phòng Tổ chức - Hành chính",
                    "current_level": "A2",
                    "current_coefficient": 3.45,
                    "last_increase_date": "01/04/2021",
                    "expected_level": "A2",
                    "expected_coefficient": 3.66,
                    "next_increase_date": "01/04/2024",
                    "months_left": 4,
                    "is_eligible": True,
                    "notes": ""
                },
                {
                    "name": "Trần Thị B",
                    "position": "Chuyên viên",
                    "department": "Phòng Tài chính - Kế toán", 
                    "current_level": "A1",
                    "current_coefficient": 2.67,
                    "last_increase_date": "15/01/2022",
                    "expected_level": "A1",
                    "expected_coefficient": 2.89,
                    "next_increase_date": "15/01/2025",
                    "months_left": 8,
                    "is_eligible": True,
                    "notes": ""
                },
                {
                    "name": "Lê Văn C",
                    "position": "Nhân viên",
                    "department": "Phòng Kinh doanh",
                    "current_level": "B1", 
                    "current_coefficient": 2.10,
                    "last_increase_date": "10/06/2022",
                    "expected_level": "B1",
                    "expected_coefficient": 2.25,
                    "next_increase_date": "10/06/2024",
                    "months_left": 6,
                    "is_eligible": True,
                    "notes": "Bị kéo dài do kỷ luật 3 tháng"
                }
            ]
            
            # Hiển thị danh sách
            st.success(f"✅ Tìm thấy {len(eligible_employees)} nhân viên đủ điều kiện nâng lương")
            
            for idx, emp in enumerate(eligible_employees, 1):
                with st.expander(f"👤 {emp['name']} - {emp['position']}", expanded=True if idx <= 2 else False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Thông tin hiện tại:**")
                        st.write(f"• Đơn vị: {emp['department']}")
                        st.write(f"• Ngạch/Hệ số: {emp['current_level']}/{emp['current_coefficient']}")
                        st.write(f"• Nâng lương gần nhất: {emp['last_increase_date']}")
                    
                    with col2:
                        st.write("**Dự kiến nâng lương:**")
                        st.write(f"• Ngạch/Hệ số mới: {emp['expected_level']}/{emp['expected_coefficient']}")
                        st.write(f"• Ngày dự kiến: {emp['next_increase_date']}")
                        
                        if emp['months_left'] <= 3:
                            st.error(f"⚠️ Còn {emp['months_left']} tháng")
                        elif emp['months_left'] <= 6:
                            st.warning(f"🔔 Còn {emp['months_left']} tháng")
                        else:
                            st.info(f"📅 Còn {emp['months_left']} tháng")
                    
                    with col3:
                        st.write("**Trạng thái:**")
                        if emp['is_eligible']:
                            st.success("✅ Đủ điều kiện")
                        else:
                            st.error("❌ Chưa đủ điều kiện")
                        
                        if emp['notes']:
                            st.warning(f"📝 {emp['notes']}")
                        
                        # Ghi chú đặc biệt
                        special_note = st.text_input(f"📝 Ghi chú đặc biệt cho {emp['name']}:", 
                                                   value=emp['notes'], key=f"note_{idx}")
    
    with tab3:
        st.subheader("📄 Xuất file báo cáo")
        
        st.markdown("**Chọn loại file cần xuất:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Công văn rà soát", use_container_width=True):
                st.success("✅ Đã xuất file: CV_RaSoat_NangLuong_Q4_2024.docx")
                st.download_button(
                    label="📥 Tải xuống",
                    data="Nội dung công văn rà soát...",
                    file_name="CV_RaSoat_NangLuong_Q4_2024.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        
        with col2:
            if st.button("📢 Thông báo kết quả", use_container_width=True):
                st.success("✅ Đã xuất file: ThongBao_KetQua_NangLuong_Q4_2024.docx")
                st.download_button(
                    label="📥 Tải xuống",
                    data="Nội dung thông báo kết quả...",
                    file_name="ThongBao_KetQua_NangLuong_Q4_2024.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        
        with col3:
            if st.button("⚖️ Quyết định nâng lương", use_container_width=True):
                st.success("✅ Đã xuất file: QuyetDinh_NangLuong_Q4_2024.docx")
                st.download_button(
                    label="📥 Tải xuống", 
                    data="Nội dung quyết định nâng lương...",
                    file_name="QuyetDinh_NangLuong_Q4_2024.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        
        st.markdown("---")
        
        # Danh sách Excel kèm theo
        st.markdown("**📊 File Excel kèm theo:**")
        
        if st.button("📊 Xuất danh sách Excel", use_container_width=True):
            # Tạo dữ liệu Excel mẫu
            excel_data = pd.DataFrame({
                'STT': [1, 2, 3],
                'Họ tên': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C'],
                'Chức vụ': ['Chuyên viên chính', 'Chuyên viên', 'Nhân viên'],
                'Đơn vị': ['Phòng TCHC', 'Phòng TCKT', 'Phòng KD'],
                'Ngạch hiện tại': ['A2', 'A1', 'B1'],
                'Hệ số hiện tại': [3.45, 2.67, 2.10],
                'Ngạch mới': ['A2', 'A1', 'B1'],
                'Hệ số mới': [3.66, 2.89, 2.25],
                'Thời điểm hưởng': ['01/04/2024', '15/01/2025', '10/06/2024'],
                'Ghi chú': ['', '', 'Kéo dài do kỷ luật']
            })
            
            st.success("✅ Đã tạo file Excel thành công!")
            st.dataframe(excel_data, use_container_width=True)
            
            # Convert to CSV for download
            csv_data = excel_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Tải danh sách Excel",
                data=csv_data,
                file_name="DanhSach_NangLuong_Q4_2024.csv", 
                mime="text/csv"
            )

def retirement_page():
    st.markdown('<div class="main-header"><h1>⏰ Theo dõi nghỉ hưu</h1></div>', unsafe_allow_html=True)
    
    # Tabs cho các chức năng con
    tab1, tab2, tab3, tab4 = st.tabs(["⏰ Danh sách nghỉ hưu", "📢 Cảnh báo", "💰 Nâng lương trước hạn", "📄 Xuất file"])
    
    with tab1:
        st.subheader("⏰ Danh sách nhân viên sắp nghỉ hưu")
        
        # Dữ liệu mẫu nghỉ hưu
        retirement_employees = [
            {
                "name": "Nguyễn Văn D", "birth_date": "15/03/1964", "gender": "Nam",
                "position": "Chuyên viên cao cấp", "department": "Phòng Tổ chức - Hành chính",
                "retirement_date": "15/06/2025", "days_left": 185, "months_left": 6.1,
                "current_salary": "A3/4.2", "years_of_service": 35,
                "eligible_for_early_increase": True, "notification_sent": False, "decision_sent": False
            },
            {
                "name": "Trần Thị E", "birth_date": "10/01/1970", "gender": "Nữ", 
                "position": "Chuyên viên chính", "department": "Phòng Tài chính - Kế toán",
                "retirement_date": "10/05/2025", "days_left": 149, "months_left": 4.9,
                "current_salary": "A2/3.8", "years_of_service": 28,
                "eligible_for_early_increase": True, "notification_sent": True, "decision_sent": False
            },
            {
                "name": "Lê Văn F", "birth_date": "20/02/1965", "gender": "Nam",
                "position": "Trưởng phòng", "department": "Phòng Kinh doanh", 
                "retirement_date": "20/02/2025", "days_left": 70, "months_left": 2.3,
                "current_salary": "A4/5.1", "years_of_service": 40,
                "eligible_for_early_increase": False, "notification_sent": True, "decision_sent": True
            }
        ]
        
        # Thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Tổng số", len(retirement_employees))
        with col2:
            need_notification = len([emp for emp in retirement_employees if emp['days_left'] <= 180 and not emp['notification_sent']])
            st.metric("📢 Cần thông báo", need_notification)
        with col3:
            need_decision = len([emp for emp in retirement_employees if emp['days_left'] <= 90 and not emp['decision_sent']])  
            st.metric("⚖️ Cần quyết định", need_decision)
        with col4:
            eligible_salary = len([emp for emp in retirement_employees if emp['eligible_for_early_increase']])
            st.metric("💰 Đủ điều kiện nâng lương", eligible_salary)
        
        # Hiển thị danh sách
        for emp in retirement_employees:
            if emp['days_left'] <= 30:
                priority, background = "🔴 Khẩn cấp", "#ffebee"
            elif emp['days_left'] <= 90:
                priority, background = "🟡 Quan trọng", "#fff3e0"
            elif emp['days_left'] <= 180:
                priority, background = "🟢 Theo dõi", "#e8f5e8"
            else:
                priority, background = "⚪ Bình thường", "#f5f5f5"
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid #1976d2; padding: 1rem; margin: 1rem 0; 
                           background: {background}; border-radius: 8px;">
                    <h4>👤 {emp['name']} ({priority}) - Còn {emp['days_left']} ngày</h4>
                    <p><strong>Nghỉ hưu:</strong> {emp['retirement_date']} | <strong>Thâm niên:</strong> {emp['years_of_service']} năm</p>
                    <p><strong>Trạng thái:</strong> 
                       {'✅ Đã thông báo' if emp['notification_sent'] else '❌ Chưa thông báo'} | 
                       {'✅ Có quyết định' if emp['decision_sent'] else '❌ Chưa có quyết định'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📢 Hệ thống cảnh báo")
        
        warning_6_months = [emp for emp in retirement_employees if 150 <= emp['days_left'] <= 180 and not emp['notification_sent']]
        warning_3_months = [emp for emp in retirement_employees if 60 <= emp['days_left'] <= 90 and not emp['decision_sent']]
        warning_1_month = [emp for emp in retirement_employees if emp['days_left'] <= 30]
        
        if warning_6_months:
            st.error(f"⚠️ **Cảnh báo 6 tháng**: {len(warning_6_months)} nhân viên cần thông báo nghỉ hưu")
        if warning_3_months:
            st.error(f"🚨 **Cảnh báo 3 tháng**: {len(warning_3_months)} nhân viên cần quyết định nghỉ hưu")  
        if warning_1_month:
            st.error(f"🔥 **Khẩn cấp**: {len(warning_1_month)} nhân viên nghỉ hưu trong tháng")
        
        if not any([warning_6_months, warning_3_months, warning_1_month]):
            st.success("✅ Tất cả thủ tục nghỉ hưu đã được xử lý đúng thời hạn!")
    
    with tab3:
        st.subheader("💰 Nâng lương trước thời hạn")
        eligible = [emp for emp in retirement_employees if emp['eligible_for_early_increase']]
        
        if eligible:
            st.info(f"📋 {len(eligible)} nhân viên đủ điều kiện nâng lương trước thời hạn")
            for emp in eligible:
                st.write(f"• **{emp['name']}**: {emp['current_salary']} → Dự kiến tăng")
        else:
            st.warning("ℹ️ Không có nhân viên đủ điều kiện nâng lương trước thời hạn")
    
    with tab4:
        st.subheader("📄 Xuất văn bản nghỉ hưu")
        
        selected_emp = st.selectbox("👤 Chọn nhân viên:", 
            [f"{emp['name']} (nghỉ hưu {emp['retirement_date']})" for emp in retirement_employees])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📢 Thông báo (6 tháng)", use_container_width=True):
                st.success("✅ Đã tạo thông báo nghỉ hưu!")
        
        with col2:
            if st.button("⚖️ Quyết định (3 tháng)", use_container_width=True):
                st.success("✅ Đã tạo quyết định nghỉ hưu!")

def planning_page():
    st.markdown('<div class="main-header"><h1>📋 Kiểm tra quy hoạch cán bộ</h1></div>', unsafe_allow_html=True)
    
    # Tabs cho các chức năng con
    tab1, tab2, tab3 = st.tabs(["👥 Danh sách quy hoạch", "📊 Phân tích", "⚙️ Cài đặt"])
    
    with tab1:
        st.subheader("👥 Danh sách cán bộ quy hoạch")
        
        # Bộ lọc
        col1, col2, col3 = st.columns(3)
        
        with col1:
            position_filter = st.selectbox("🎯 Lọc theo vị trí quy hoạch",
                ["Tất cả", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên cao cấp"])
        
        with col2:
            department_filter = st.selectbox("🏢 Lọc theo đơn vị",
                ["Tất cả", "Phòng TCHC", "Phòng TCKT", "Phòng KD"])
        
        with col3:
            age_filter = st.selectbox("📅 Lọc theo độ tuổi",
                ["Tất cả", "Còn trong quy hoạch", "Sắp quá tuổi", "Đã quá tuổi"])
        
        # Dữ liệu quy hoạch mẫu
        planning_data = [
            {
                "name": "Nguyễn Văn A", "birth_date": "15/06/1985", "age": 38,
                "current_position": "Chuyên viên chính", "planning_position": "Phó Trưởng phòng",
                "department": "Phòng TCHC", "planning_period": "2020-2025",
                "max_age_for_position": 45, "years_left": 7, "is_valid": True,
                "education": "Thạc sĩ Luật", "experience_years": 15,
                "planning_status": "active", "notes": ""
            },
            {
                "name": "Trần Thị B", "birth_date": "20/03/1978", "age": 45,
                "current_position": "Chuyên viên", "planning_position": "Trưởng phòng",
                "department": "Phòng TCKT", "planning_period": "2021-2026",
                "max_age_for_position": 50, "years_left": 5, "is_valid": True,
                "education": "Cử nhân Tài chính", "experience_years": 20,
                "planning_status": "active", "notes": ""
            },
            {
                "name": "Lê Văn C", "birth_date": "10/08/1970", "age": 53,
                "current_position": "Phó Trưởng phòng", "planning_position": "Trưởng phòng",
                "department": "Phòng KD", "planning_period": "2019-2024", 
                "max_age_for_position": 52, "years_left": -1, "is_valid": False,
                "education": "Cử nhân Kinh tế", "experience_years": 25,
                "planning_status": "expired", "notes": "Đã quá tuổi quy hoạch"
            }
        ]
        
        # Thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_planned = len(planning_data)
            st.metric("👥 Tổng quy hoạch", total_planned)
        
        with col2:
            active_planning = len([p for p in planning_data if p['is_valid']])
            st.metric("✅ Còn hiệu lực", active_planning)
        
        with col3:
            near_expiry = len([p for p in planning_data if p['is_valid'] and p['years_left'] <= 2])
            st.metric("⚠️ Sắp hết hạn", near_expiry)
        
        with col4:
            expired = len([p for p in planning_data if not p['is_valid']])
            st.metric("❌ Đã hết hạn", expired)
        
        st.markdown("---")
        
        # Hiển thị danh sách
        for person in planning_data:
            # Xác định màu sắc và trạng thái
            if not person['is_valid']:
                status_color = "#ffebee"
                status_text = "❌ Hết hạn"
                border_color = "#f44336"
            elif person['years_left'] <= 1:
                status_color = "#fff3e0"
                status_text = "⚠️ Sắp hết hạn"
                border_color = "#ff9800"
            elif person['years_left'] <= 2:
                status_color = "#e3f2fd"
                status_text = "🔔 Cần theo dõi"
                border_color = "#2196f3"
            else:
                status_color = "#e8f5e8"
                status_text = "✅ Bình thường"
                border_color = "#4caf50"
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid {border_color}; padding: 1rem; margin: 1rem 0; 
                           background: {status_color}; border-radius: 8px;">
                    <h4>👤 {person['name']} ({status_text})</h4>
                    <p><strong>Quy hoạch:</strong> {person['planning_position']} | <strong>Giai đoạn:</strong> {person['planning_period']}</p>
                    <p><strong>Tuổi:</strong> {person['age']} (giới hạn: {person['max_age_for_position']}) | 
                       <strong>Còn:</strong> {person['years_left']} năm</p>
                    {'<p><strong>Ghi chú:</strong> ' + person['notes'] + '</p>' if person['notes'] else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Nút hành động
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button(f"📋 Chi tiết", key=f"detail_{person['name']}"):
                        st.info(f"**Học vấn:** {person['education']}\n**Kinh nghiệm:** {person['experience_years']} năm")
                
                with col_b:
                    if person['years_left'] <= 2 and person['is_valid']:
                        if st.button(f"🔄 Gia hạn quy hoạch", key=f"extend_{person['name']}"):
                            st.success(f"✅ Đã khởi tạo gia hạn quy hoạch cho {person['name']}")
                
                with col_c:
                    if person['is_valid']:
                        if st.button(f"⬆️ Đề xuất bổ nhiệm", key=f"promote_{person['name']}"):
                            st.success(f"✅ Đã chuyển {person['name']} sang kiểm tra điều kiện bổ nhiệm")
    
    with tab2:
        st.subheader("📊 Phân tích quy hoạch")
        
        # Biểu đồ phân tích
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Phân bố theo độ tuổi")
            age_data = pd.DataFrame({
                'Độ tuổi': ['30-35', '36-40', '41-45', '46-50', '51-55'],
                'Số lượng': [1, 1, 1, 0, 0]
            })
            st.bar_chart(age_data.set_index('Độ tuổi'))
        
        with col2:
            st.markdown("#### 🎯 Trạng thái quy hoạch")
            status_data = pd.DataFrame({
                'Trạng thái': ['Còn hiệu lực', 'Sắp hết hạn', 'Đã hết hạn'],
                'Số lượng': [1, 1, 1]
            })
            st.bar_chart(status_data.set_index('Trạng thái'))
        
        st.markdown("---")
        
        # Quota check (Số lượng quy hoạch)
        st.markdown("#### 📋 Kiểm tra định mức quy hoạch")
        
        quota_data = [
            {"position": "Trưởng phòng", "current": 2, "max_quota": 3, "available": 1},
            {"position": "Phó Trưởng phòng", "current": 1, "max_quota": 4, "available": 3},
            {"position": "Chuyên viên cao cấp", "current": 0, "max_quota": 5, "available": 5}
        ]
        
        for quota in quota_data:
            col_pos, col_cur, col_max, col_avail = st.columns(4)
            
            with col_pos:
                st.write(f"**{quota['position']}**")
            
            with col_cur:
                st.metric("Hiện có", quota['current'])
            
            with col_max:
                st.metric("Định mức", quota['max_quota'])
            
            with col_avail:
                if quota['available'] > 0:
                    st.success(f"✅ Còn {quota['available']} suất")
                else:
                    st.error("❌ Đã đầy")
    
    with tab3:
        st.subheader("⚙️ Cài đặt quy hoạch")
        
        # Thiết lập độ tuổi giới hạn
        st.markdown("#### 📅 Giới hạn độ tuổi theo vị trí")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input("Trưởng phòng (tuổi tối đa)", value=50, min_value=40, max_value=60)
            st.number_input("Phó Trưởng phòng (tuổi tối đa)", value=45, min_value=35, max_value=55)
        
        with col2:
            st.number_input("Chuyên viên cao cấp (tuổi tối đa)", value=40, min_value=30, max_value=50)
            st.number_input("Chuyên viên chính (tuổi tối đa)", value=35, min_value=25, max_value=45)
        
        st.markdown("---")
        
        # Thiết lập định mức
        st.markdown("#### 📊 Định mức quy hoạch theo đơn vị")
        
        department_quotas = st.data_editor(
            pd.DataFrame({
                "Đơn vị": ["Phòng TCHC", "Phòng TCKT", "Phòng KD"],
                "Trưởng phòng": [1, 1, 1],
                "Phó Trưởng phòng": [2, 1, 1], 
                "Chuyên viên cao cấp": [2, 2, 1]
            }),
            use_container_width=True
        )
        
        if st.button("💾 Lưu cài đặt", use_container_width=True):
            st.success("✅ Đã lưu cài đặt quy hoạch thành công!")
        
        st.markdown("---")
        
        # Xuất báo cáo
        st.markdown("#### 📄 Xuất báo cáo quy hoạch")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Báo cáo tổng hợp", use_container_width=True):
                st.success("✅ Đã tạo báo cáo tổng hợp quy hoạch!")
        
        with col2:
            if st.button("📋 Danh sách Excel", use_container_width=True):
                export_data = pd.DataFrame([
                    {
                        "STT": i+1, "Họ tên": p["name"], "Tuổi": p["age"],
                        "Chức vụ hiện tại": p["current_position"],
                        "Vị trí quy hoạch": p["planning_position"],
                        "Đơn vị": p["department"], "Giai đoạn": p["planning_period"],
                        "Trạng thái": "Còn hiệu lực" if p["is_valid"] else "Hết hạn"
                    } for i, p in enumerate(planning_data)
                ])
                
                st.success("✅ Đã tạo danh sách Excel!")
                st.dataframe(export_data, use_container_width=True)

def work_history_page():
    st.markdown('<div class="main-header"><h1>💼 Quản lý quá trình công tác</h1></div>', unsafe_allow_html=True)
    
    # Chọn nhân viên
    selected_employee = st.selectbox("👤 Chọn nhân viên:", 
        ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"])
    
    tab1, tab2, tab3 = st.tabs(["📅 Timeline công tác", "➕ Thêm giai đoạn", "📄 Xuất file"])
    
    with tab1:
        st.subheader(f"📅 Quá trình công tác của {selected_employee}")
        
        # Dữ liệu timeline mẫu
        timeline_data = [
            {
                "period": "08/2008 - 03/2015",
                "position": "Nhân viên",
                "department": "Công ty ABC",
                "location": "Hà Nội",
                "responsibilities": "Xử lý hồ sơ, làm báo cáo",
                "achievements": "Hoàn thành tốt nhiệm vụ",
                "status": "completed"
            },
            {
                "period": "03/2015 - 12/2020", 
                "position": "Chuyên viên",
                "department": "Phòng Tổ chức - Hành chính",
                "location": "Hà Nội",
                "responsibilities": "Quản lý hồ sơ nhân sự, tổ chức đào tạo",
                "achievements": "Đạt danh hiệu lao động tiên tiến 2019",
                "status": "completed"
            },
            {
                "period": "12/2020 - Hiện tại",
                "position": "Chuyên viên chính", 
                "department": "Phòng Tổ chức - Hành chính",
                "location": "Hà Nội",
                "responsibilities": "Phụ trách công tác quy hoạch và đào tạo cán bộ",
                "achievements": "Bằng khen Thủ tướng 2022",
                "status": "current"
            }
        ]
        
        # Hiển thị timeline
        for i, period in enumerate(timeline_data):
            is_current = period['status'] == 'current'
            
            st.markdown(f"""
            <div style="border-left: 4px solid {'#4caf50' if is_current else '#2196f3'}; 
                       padding: 1rem; margin: 1rem 0; 
                       background: {'#e8f5e8' if is_current else '#f8f9fa'}; 
                       border-radius: 8px;">
                <h4>{"🟢" if is_current else "🔵"} {period['period']}</h4>
                <p><strong>Chức vụ:</strong> {period['position']}</p>
                <p><strong>Đơn vị:</strong> {period['department']}</p>
                <p><strong>Địa điểm:</strong> {period['location']}</p>
                <p><strong>Nhiệm vụ:</strong> {period['responsibilities']}</p>
                <p><strong>Thành tích:</strong> {period['achievements']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Nút sửa/xóa
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if st.button("✏️", key=f"edit_{i}"):
                    st.info(f"Chỉnh sửa giai đoạn {period['period']}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.success(f"Đã xóa giai đoạn {period['period']}")
    
    with tab2:
        st.subheader("➕ Thêm giai đoạn công tác mới")
        
        with st.form("add_work_period"):
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("📅 Từ ngày:")
                end_date = st.date_input("📅 Đến ngày:")
                position = st.text_input("💼 Chức vụ:")
                department = st.text_input("🏢 Đơn vị:")
            
            with col2:
                location = st.text_input("📍 Địa điểm:")
                responsibilities = st.text_area("📋 Nhiệm vụ:", height=100)
                achievements = st.text_area("🏆 Thành tích:", height=100)
            
            if st.form_submit_button("➕ Thêm giai đoạn"):
                st.success("✅ Đã thêm giai đoạn công tác mới!")
    
    with tab3:
        st.subheader("📄 Xuất file quá trình công tác")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Xuất Word", use_container_width=True):
                st.success(f"✅ Đã xuất quá trình công tác của {selected_employee}!")
        
        with col2:
            if st.button("📊 Xuất Excel", use_container_width=True):
                st.success(f"✅ Đã xuất Excel quá trình công tác!")

def contract_page():
    st.markdown('<div class="main-header"><h1>📄 Quản lý hợp đồng lao động</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Danh sách hợp đồng", "➕ Tạo hợp đồng mới", "⚠️ Cảnh báo hết hạn"])
    
    with tab1:
        st.subheader("📋 Danh sách hợp đồng hiện tại")
        
        # Dữ liệu hợp đồng mẫu
        contract_data = [
            {
                "employee": "Nguyễn Văn A", "type": "Hợp đồng không thời hạn",
                "start_date": "15/03/2020", "end_date": "Không thời hạn",
                "position": "Chuyên viên chính", "salary": "3.45",
                "status": "active", "days_to_expire": None
            },
            {
                "employee": "Trần Thị B", "type": "Hợp đồng có thời hạn", 
                "start_date": "01/06/2023", "end_date": "31/05/2025",
                "position": "Chuyên viên", "salary": "2.67",
                "status": "active", "days_to_expire": 162
            },
            {
                "employee": "Lê Văn C (BKS)", "type": "Hợp đồng Ban kiểm soát",
                "start_date": "01/01/2024", "end_date": "31/12/2026", 
                "position": "Thành viên BKS", "salary": "Theo quy định",
                "status": "active", "days_to_expire": 730
            }
        ]
        
        # Thống kê
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Tổng hợp đồng", len(contract_data))
        
        with col2:
            active_contracts = len([c for c in contract_data if c['status'] == 'active'])
            st.metric("✅ Đang hiệu lực", active_contracts)
        
        with col3:
            expiring_soon = len([c for c in contract_data if c['days_to_expire'] and c['days_to_expire'] <= 90])
            st.metric("⚠️ Sắp hết hạn", expiring_soon)
        
        with col4:
            bks_contracts = len([c for c in contract_data if "BKS" in c['employee']])
            st.metric("👥 Hợp đồng BKS", bks_contracts)
        
        # Hiển thị danh sách
        for contract in contract_data:
            # Xác định màu sắc
            if contract['days_to_expire'] is None:
                color, status_text = "#e8f5e8", "♾️ Không thời hạn"
            elif contract['days_to_expire'] <= 30:
                color, status_text = "#ffebee", "🔴 Sắp hết hạn"
            elif contract['days_to_expire'] <= 90:
                color, status_text = "#fff3e0", "🟡 Cần theo dõi"
            else:
                color, status_text = "#e3f2fd", "🔵 Bình thường"
            
            st.markdown(f"""
            <div style="border-left: 4px solid #1976d2; padding: 1rem; margin: 1rem 0; 
                       background: {color}; border-radius: 8px;">
                <h4>📄 {contract['employee']} ({status_text})</h4>
                <p><strong>Loại:</strong> {contract['type']}</p>
                <p><strong>Thời gian:</strong> {contract['start_date']} → {contract['end_date']}</p>
                <p><strong>Chức vụ:</strong> {contract['position']} | <strong>Lương:</strong> {contract['salary']}</p>
                {f'<p><strong>Còn lại:</strong> {contract["days_to_expire"]} ngày</p>' if contract['days_to_expire'] else ''}
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("➕ Tạo hợp đồng lao động mới")
        
        with st.form("new_contract"):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_name = st.text_input("👤 Họ tên nhân viên:")
                contract_type = st.selectbox("📋 Loại hợp đồng:", 
                    ["Hợp đồng có thời hạn", "Hợp đồng không thời hạn", "Hợp đồng Ban kiểm soát"])
                start_date = st.date_input("📅 Ngày bắt đầu:")
            
            with col2:
                position = st.text_input("💼 Chức vụ:")
                if contract_type != "Hợp đồng không thời hạn":
                    end_date = st.date_input("📅 Ngày kết thúc:")
                salary_coefficient = st.number_input("💰 Hệ số lương:", min_value=1.0, max_value=10.0, step=0.01)
            
            terms_conditions = st.text_area("📜 Điều khoản đặc biệt:", height=100)
            
            if st.form_submit_button("✅ Tạo hợp đồng"):
                st.success(f"✅ Đã tạo hợp đồng cho {employee_name}!")
    
    with tab3:
        st.subheader("⚠️ Cảnh báo hợp đồng sắp hết hạn")
        
        expiring_contracts = [c for c in contract_data if c['days_to_expire'] and c['days_to_expire'] <= 90]
        
        if expiring_contracts:
            st.error(f"🚨 Có {len(expiring_contracts)} hợp đồng sắp hết hạn!")
            
            for contract in expiring_contracts:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{contract['employee']}**")
                        st.write(f"Hết hạn: {contract['end_date']} (còn {contract['days_to_expire']} ngày)")
                    
                    with col2:
                        if st.button("🔄 Gia hạn", key=f"extend_{contract['employee']}"):
                            st.success("✅ Đã khởi tạo gia hạn hợp đồng!")
                    
                    with col3:
                        if st.button("📄 Tạo mới", key=f"new_{contract['employee']}"):
                            st.success("✅ Đã khởi tạo hợp đồng mới!")
        else:
            st.success("✅ Không có hợp đồng nào sắp hết hạn!")
        
        # Xuất báo cáo
        if st.button("📊 Xuất báo cáo hợp đồng", use_container_width=True):
            report_data = pd.DataFrame([
                {
                    "STT": i+1, "Họ tên": c["employee"], "Loại HĐ": c["type"],
                    "Bắt đầu": c["start_date"], "Kết thúc": c["end_date"],
                    "Chức vụ": c["position"], "Trạng thái": "Hiệu lực" if c["status"] == "active" else "Hết hạn"
                } for i, c in enumerate(contract_data)
            ])
            
            st.success("✅ Đã tạo báo cáo hợp đồng!")
            st.dataframe(report_data, use_container_width=True)

def appointment_page():
    st.markdown('<div class="main-header"><h1>✅ Kiểm tra điều kiện bổ nhiệm</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔍 Kiểm tra điều kiện", "⏰ Cảnh báo bổ nhiệm lại", "📊 Thống kê"])
    
    with tab1:
        st.subheader("🔍 Kiểm tra điều kiện bổ nhiệm")
        
        # Chọn nhân viên và vị trí
        col1, col2 = st.columns(2)
        
        with col1:
            selected_employee = st.selectbox("👤 Chọn nhân viên:", 
                ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"])
        
        with col2:
            target_position = st.selectbox("🎯 Vị trí bổ nhiệm:",
                ["Phó Trưởng phòng", "Trưởng phòng", "Chuyên viên cao cấp"])
        
        if st.button("🔍 Kiểm tra điều kiện", use_container_width=True):
            st.markdown("### 📋 Kết quả kiểm tra")
            
            # Mô phỏng kết quả kiểm tra
            conditions = [
                {"name": "Trong quy hoạch", "status": True, "details": "Có trong quy hoạch 2020-2025"},
                {"name": "Trình độ học vấn", "status": True, "details": "Thạc sĩ Luật (đạt yêu cầu)"},
                {"name": "Chứng chỉ bắt buộc", "status": False, "details": "Thiếu chứng chỉ Quản lý nhà nước"},
                {"name": "Kinh nghiệm công tác", "status": True, "details": "15 năm (≥ 5 năm yêu cầu)"},
                {"name": "Độ tuổi", "status": True, "details": "38 tuổi (trong giới hạn 45 tuổi)"},
                {"name": "Đánh giá năng lực", "status": True, "details": "Hoàn thành xuất sắc 3 năm liên tiếp"}
            ]
            
            all_passed = all(c['status'] for c in conditions)
            
            for condition in conditions:
                if condition['status']:
                    st.success(f"✅ **{condition['name']}**: {condition['details']}")
                else:
                    st.error(f"❌ **{condition['name']}**: {condition['details']}")
            
            st.markdown("---")
            
            if all_passed:
                st.success("🎉 **ĐỦ ĐIỀU KIỆN BỔ NHIỆM**")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("📄 Tạo hồ sơ đề xuất"):
                        st.success("✅ Đã tạo hồ sơ đề xuất bổ nhiệm!")
                
                with col_b:
                    if st.button("📋 Xuất báo cáo"):
                        st.success("✅ Đã xuất báo cáo đánh giá điều kiện!")
            else:
                st.error("❌ **CHƯA ĐỦ ĐIỀU KIỆN BỔ NHIỆM**")
                st.warning("📝 Cần hoàn thiện các điều kiện chưa đạt trước khi bổ nhiệm")
    
    with tab2:
        st.subheader("⏰ Cảnh báo bổ nhiệm lại (90 ngày)")
        
        # Dữ liệu cảnh báo bổ nhiệm lại
        reappointment_data = [
            {
                "name": "Trần Văn D", "position": "Trưởng phòng TCHC",
                "appointment_date": "15/01/2022", "term_end_date": "15/01/2025",
                "days_left": 45, "term_years": 3, "current_term": 1
            },
            {
                "name": "Nguyễn Thị E", "position": "Phó Trưởng phòng TCKT",
                "appointment_date": "01/03/2022", "term_end_date": "01/03/2025",
                "days_left": 90, "term_years": 3, "current_term": 1
            }
        ]
        
        if reappointment_data:
            st.error(f"⚠️ Có {len(reappointment_data)} cán bộ cần xét bổ nhiệm lại trong 90 ngày tới!")
            
            for person in reappointment_data:
                # Xác định mức độ ưu tiên
                if person['days_left'] <= 30:
                    priority_color, priority_text = "#ffebee", "🔴 Khẩn cấp"
                elif person['days_left'] <= 60:
                    priority_color, priority_text = "#fff3e0", "🟡 Quan trọng"
                else:
                    priority_color, priority_text = "#e3f2fd", "🔵 Theo dõi"
                
                st.markdown(f"""
                <div style="border-left: 4px solid #f44336; padding: 1rem; margin: 1rem 0; 
                           background: {priority_color}; border-radius: 8px;">
                    <h4>👤 {person['name']} ({priority_text})</h4>
                    <p><strong>Chức vụ:</strong> {person['position']}</p>
                    <p><strong>Nhiệm kỳ:</strong> {person['appointment_date']} → {person['term_end_date']} (Nhiệm kỳ {person['current_term']})</p>
                    <p><strong>Thời gian còn lại:</strong> {person['days_left']} ngày</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Nút hành động
                col_x, col_y, col_z = st.columns(3)
                
                with col_x:
                    if st.button("🔍 Kiểm tra điều kiện", key=f"check_{person['name']}"):
                        st.info(f"Đang kiểm tra điều kiện bổ nhiệm lại cho {person['name']}")
                
                with col_y:
                    if st.button("📄 Tạo hồ sơ", key=f"create_{person['name']}"):
                        st.success(f"✅ Đã tạo hồ sơ bổ nhiệm lại cho {person['name']}")
                
                with col_z:
                    if st.button("⏰ Thiết lập nhắc nhở", key=f"remind_{person['name']}"):
                        st.success("✅ Đã thiết lập nhắc nhở!")
        else:
            st.success("✅ Hiện tại không có cán bộ nào cần bổ nhiệm lại trong 90 ngày tới!")
    
    with tab3:
        st.subheader("📊 Thống kê bổ nhiệm")
        
        # Biểu đồ thống kê
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Bổ nhiệm theo năm")
            year_data = pd.DataFrame({
                'Năm': ['2022', '2023', '2024'],
                'Số lượng': [5, 8, 3]
            })
            st.bar_chart(year_data.set_index('Năm'))
        
        with col2:
            st.markdown("#### 🎯 Theo vị trí")
            position_data = pd.DataFrame({
                'Vị trí': ['Trưởng phòng', 'Phó Trưởng phòng', 'Chuyên viên cao cấp'],
                'Số lượng': [2, 4, 6]
            })
            st.bar_chart(position_data.set_index('Vị trí'))
        
        # Bảng thống kê chi tiết
        st.markdown("#### 📋 Chi tiết bổ nhiệm năm 2024")
        
        detail_data = pd.DataFrame([
            {"Tháng": "01/2024", "Họ tên": "Trần Văn F", "Vị trí": "Phó Trưởng phòng", "Trạng thái": "Đã bổ nhiệm"},
            {"Tháng": "03/2024", "Họ tên": "Nguyễn Thị G", "Vị trí": "Chuyên viên cao cấp", "Trạng thái": "Đã bổ nhiệm"},
            {"Tháng": "06/2024", "Họ tên": "Lê Văn H", "Vị trí": "Trưởng phòng", "Trạng thái": "Đang xử lý"}
        ])
        
        st.dataframe(detail_data, use_container_width=True)
        
        # Xuất báo cáo
        if st.button("📊 Xuất báo cáo thống kê", use_container_width=True):
            st.success("✅ Đã tạo báo cáo thống kê bổ nhiệm năm 2024!")

def award_page():
    st.markdown('<div class="main-header"><h1>🏆 Xem điều kiện khen thưởng</h1></div>', unsafe_allow_html=True)
    
    # Chọn nhân viên
    selected_employee = st.selectbox("👤 Chọn nhân viên:", 
        ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"])
    
    # Chọn loại khen thưởng
    award_type = st.selectbox("🎯 Loại khen thưởng:",
        ["Lao động tiên tiến", "Chiến sỹ thi đua cơ sở", "Bằng khen Thủ tướng", "Huân chương Lao động"])
    
    if st.button("🔍 Kiểm tra điều kiện khen thưởng"):
        st.subheader(f"📋 Điều kiện {award_type} cho {selected_employee}")
        
        # Mô phỏng điều kiện khen thưởng
        award_conditions = [
            {"criteria": "Hoàn thành xuất sắc nhiệm vụ", "status": True, "details": "3 năm liên tiếp đạt xuất sắc"},
            {"criteria": "Không vi phạm kỷ luật", "status": True, "details": "Không có kỷ luật trong 5 năm gần nhất"},
            {"criteria": "Có thành tích nổi bật", "status": True, "details": "Dẫn đầu đơn vị về hiệu quả công việc"},
            {"criteria": "Thời gian công tác", "status": True, "details": "15 năm (≥ 5 năm yêu cầu)"}
        ]
        
        all_eligible = all(c['status'] for c in award_conditions)
        
        for condition in award_conditions:
            if condition['status']:
                st.success(f"✅ **{condition['criteria']}**: {condition['details']}")
            else:
                st.error(f"❌ **{condition['criteria']}**: {condition['details']}")
        
        if all_eligible:
            st.success(f"🎉 **ĐỦ ĐIỀU KIỆN** nhận {award_type}!")
        else:
            st.error(f"❌ **CHƯA ĐỦ ĐIỀU KIỆN** nhận {award_type}")
    
    st.info("💡 **Lưu ý**: Chức năng sẽ được cập nhật thêm các tiêu chí cụ thể")

def early_salary_page():
    st.markdown('<div class="main-header"><h1>⚡ Nâng lương trước thời hạn do thành tích</h1></div>', unsafe_allow_html=True)
    
    st.subheader("🏆 Danh sách đề xuất nâng lương trước thời hạn")
    
    # Dữ liệu mẫu
    early_salary_candidates = [
        {
            "name": "Trần Văn X", "achievement": "Giải nhất cuộc thi sáng kiến cải tiến",
            "current_salary": "A2/3.2", "proposed_salary": "A2/3.45",
            "recommendation_date": "15/11/2024", "status": "pending"
        },
        {
            "name": "Nguyễn Thị Y", "achievement": "Hoàn thành xuất sắc dự án trọng điểm",
            "current_salary": "A1/2.5", "proposed_salary": "A1/2.67", 
            "recommendation_date": "20/10/2024", "status": "approved"
        }
    ]
    
    for candidate in early_salary_candidates:
        status_color = "#e8f5e8" if candidate['status'] == 'approved' else "#fff3e0"
        status_text = "✅ Đã duyệt" if candidate['status'] == 'approved' else "⏳ Chờ duyệt"
        
        st.markdown(f"""
        <div style="border-left: 4px solid #4caf50; padding: 1rem; margin: 1rem 0; 
                   background: {status_color}; border-radius: 8px;">
            <h4>🏆 {candidate['name']} ({status_text})</h4>
            <p><strong>Thành tích:</strong> {candidate['achievement']}</p>
            <p><strong>Lương hiện tại:</strong> {candidate['current_salary']} → <strong>Đề xuất:</strong> {candidate['proposed_salary']}</p>
            <p><strong>Ngày đề xuất:</strong> {candidate['recommendation_date']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if candidate['status'] == 'pending':
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Phê duyệt", key=f"approve_{candidate['name']}"):
                    st.success("✅ Đã phê duyệt nâng lương trước thời hạn!")
            with col2:
                if st.button(f"📄 Xuất quyết định", key=f"export_{candidate['name']}"):
                    st.success("✅ Đã xuất quyết định nâng lương!")

def reports_page():
    st.markdown('<div class="main-header"><h1>📊 Báo cáo nhanh</h1></div>', unsafe_allow_html=True)
    
    # Chọn năm báo cáo
    report_year = st.selectbox("📅 Chọn năm báo cáo:", ["2024", "2023", "2022"])
    
    tab1, tab2, tab3 = st.tabs(["📈 Tổng quan", "📊 Phân tích", "🔍 Chi tiết"])
    
    with tab1:
        st.subheader(f"📈 Báo cáo tổng quan năm {report_year}")
        
        # Thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Nâng lương", "25", "8")
            st.metric("⏰ Nghỉ hưu", "12", "-3")
        
        with col2:
            st.metric("📄 Hợp đồng mới", "15", "5")
            st.metric("👋 Thôi việc", "8", "2")
        
        with col3:
            st.metric("⬆️ Bổ nhiệm", "6", "1")
            st.metric("🤱 Nghỉ thai sản", "4", "-1")
        
        with col4:
            st.metric("📚 Đi học", "3", "1")
            st.metric("🌍 Phu nhân ngoại giao", "1", "0")
        
        # Biểu đồ theo tháng
        st.subheader("📊 Biến động nhân sự theo tháng")
        monthly_data = pd.DataFrame({
            'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
            'Vào': [2, 1, 3, 2, 1, 4, 2, 0, 1, 2, 1, 0],
            'Ra': [1, 0, 2, 1, 3, 1, 0, 2, 1, 0, 1, 2]
        })
        st.line_chart(monthly_data.set_index('Tháng'))
    
    with tab2:
        st.subheader("🔍 Phân tích thôi việc")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Theo độ tuổi")
            age_resign_data = pd.DataFrame({
                'Độ tuổi': ['25-30', '31-35', '36-40', '41-45', '46-50'],
                'Số lượng': [3, 2, 2, 1, 0]
            })
            st.bar_chart(age_resign_data.set_index('Độ tuổi'))
        
        with col2:
            st.markdown("#### 🎓 Theo trình độ")
            education_resign_data = pd.DataFrame({
                'Trình độ': ['Cử nhân', 'Thạc sĩ', 'Tiến sĩ'],
                'Số lượng': [5, 2, 1]
            })
            st.bar_chart(education_resign_data.set_index('Trình độ'))
        
        st.markdown("#### ⏰ Theo thâm niên")
        tenure_data = pd.DataFrame({
            'Thâm niên': ['< 2 năm', '2-5 năm', '5-10 năm', '> 10 năm'],
            'Số lượng': [4, 2, 1, 1]
        })
        st.bar_chart(tenure_data.set_index('Thâm niên'))
        
        st.info("💡 **Nhận xét**: Tỷ lệ thôi việc cao ở nhóm 25-35 tuổi, cần có biện pháp giữ chân nhân tài")
    
    with tab3:
        st.subheader("🔍 Cơ cấu nhân sự chi tiết")
        
        # Cơ cấu theo nhiều tiêu chí
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 Theo giới tính")
            gender_structure = pd.DataFrame({
                'Giới tính': ['Nam', 'Nữ'],
                'Số lượng': [85, 65],
                'Tỷ lệ (%)': [56.7, 43.3]
            })
            st.dataframe(gender_structure)
            
            st.markdown("#### 🏛️ Theo dân tộc")
            ethnic_structure = pd.DataFrame({
                'Dân tộc': ['Kinh', 'Tày', 'Thái', 'Khác'],
                'Số lượng': [140, 5, 3, 2]
            })
            st.dataframe(ethnic_structure)
        
        with col2:
            st.markdown("#### 🎓 Theo trình độ LLCT")
            political_structure = pd.DataFrame({
                'Trình độ': ['Cao cấp', 'Trung cấp', 'Sơ cấp', 'Chưa có'],
                'Số lượng': [25, 80, 35, 10]
            })
            st.dataframe(political_structure)
            
            st.markdown("#### 💼 Theo chuyên môn")
            professional_structure = pd.DataFrame({
                'Trình độ': ['Tiến sĩ', 'Thạc sĩ', 'Cử nhân', 'Khác'],
                'Số lượng': [5, 45, 85, 15]
            })
            st.dataframe(professional_structure)
        
        # Tra cứu thời gian còn lại
        st.markdown("---")
        st.markdown("#### ⏰ Tra cứu thời gian còn lại đến sự kiện")
        
        col_a, col_b = st.columns(2)
        with col_a:
            target_date = st.date_input("📅 Chọn mốc thời gian:")
        with col_b:
            event_type = st.selectbox("🎯 Loại sự kiện:", 
                ["Nghỉ hưu", "Hết hạn hợp đồng", "Kết thúc quy hoạch"])
        
        if st.button("🔍 Tính toán thời gian"):
            from datetime import date
            days_left = (target_date - date.today()).days
            st.info(f"⏰ Còn **{days_left} ngày** ({days_left/30:.1f} tháng) đến {event_type.lower()}")
    
    # Xuất báo cáo
    st.markdown("---")
    if st.button("📊 Xuất báo cáo năm tổng hợp", use_container_width=True):
        st.success(f"✅ Đã xuất báo cáo tổng hợp năm {report_year}!")

def insurance_page():
    st.markdown('<div class="main-header"><h1>🏥 Báo bảo hiểm xã hội</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["⏰ Nhắc nhở", "📊 Xuất Excel BHXH", "📋 Quản lý thay đổi"])
    
    with tab1:
        st.subheader("⏰ Nhắc nhở công việc bảo hiểm")
        
        # Danh sách nhắc nhở
        insurance_reminders = [
            {"type": "Điều chỉnh lương", "employee": "Nguyễn Văn A", "deadline": "31/12/2024", "days_left": 30},
            {"type": "Báo nghỉ thai sản", "employee": "Trần Thị B", "deadline": "15/01/2025", "days_left": 45},
            {"type": "Báo nghỉ hưu", "employee": "Lê Văn C", "deadline": "28/02/2025", "days_left": 89}
        ]
        
        if insurance_reminders:
            st.warning(f"⚠️ Có {len(insurance_reminders)} việc cần xử lý!")
            
            for reminder in insurance_reminders:
                if reminder['days_left'] <= 7:
                    urgency, color = "🔴 Khẩn cấp", "#ffebee"
                elif reminder['days_left'] <= 30:
                    urgency, color = "🟡 Quan trọng", "#fff3e0"
                else:
                    urgency, color = "🟢 Bình thường", "#e8f5e8"
                
                st.markdown(f"""
                <div style="border-left: 4px solid #1976d2; padding: 1rem; margin: 1rem 0; 
                           background: {color}; border-radius: 8px;">
                    <h4>📋 {reminder['type']} ({urgency})</h4>
                    <p><strong>Nhân viên:</strong> {reminder['employee']}</p>
                    <p><strong>Hạn xử lý:</strong> {reminder['deadline']} (còn {reminder['days_left']} ngày)</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"✅ Đã xử lý", key=f"done_{reminder['employee']}"):
                    st.success(f"✅ Đã đánh dấu hoàn thành {reminder['type']} cho {reminder['employee']}")
        else:
            st.success("✅ Không có công việc bảo hiểm nào cần xử lý!")
    
    with tab2:
        st.subheader("📊 Xuất file Excel cho Bảo hiểm Xã hội")
        
        # Chọn loại báo cáo
        report_type = st.selectbox("📋 Chọn loại báo cáo BHXH:",
            ["Điều chỉnh chức danh/lương/phụ cấp", "Nghỉ hưu/thôi việc", "Nghỉ thai sản", 
             "Nghỉ ốm đau", "Đi học", "Phu nhân ngoại giao"])
        
        # Chọn tháng báo cáo
        col1, col2 = st.columns(2)
        
        with col1:
            report_month = st.selectbox("📅 Tháng báo cáo:", 
                ["12/2024", "11/2024", "10/2024", "09/2024"])
        
        with col2:
            department = st.selectbox("🏢 Phòng ban:", 
                ["Tất cả", "Phòng TCHC", "Phòng TCKT", "Phòng KD"])
        
        if st.button("📊 Tạo file Excel BHXH", use_container_width=True):
            # Dữ liệu mẫu tùy theo loại báo cáo
            if "lương" in report_type:
                excel_data = pd.DataFrame([
                    {"STT": 1, "Mã NV": "NV001", "Họ tên": "Nguyễn Văn A", "Số sổ BHXH": "1234567890",
                     "Lương cũ": 6900000, "Lương mới": 7320000, "Từ tháng": "01/2025", "Ghi chú": "Nâng lương định kỳ"},
                    {"STT": 2, "Mã NV": "NV002", "Họ tên": "Trần Thị B", "Số sổ BHXH": "1234567891", 
                     "Lương cũ": 5340000, "Lương mới": 5781000, "Từ tháng": "01/2025", "Ghi chú": "Nâng lương định kỳ"}
                ])
            elif "thai sản" in report_type:
                excel_data = pd.DataFrame([
                    {"STT": 1, "Mã NV": "NV003", "Họ tên": "Nguyễn Thị C", "Số sổ BHXH": "1234567892",
                     "Từ ngày": "15/01/2025", "Đến ngày": "15/07/2025", "Chế độ": "Nghỉ thai sản 6 tháng", "Ghi chú": ""}
                ])
            else:
                excel_data = pd.DataFrame([
                    {"STT": 1, "Thông tin": "Dữ liệu mẫu", "Ghi chú": "Sẽ cập nhật theo loại báo cáo"}
                ])
            
            st.success(f"✅ Đã tạo file Excel: {report_type} - {report_month}")
            st.dataframe(excel_data, use_container_width=True)
            
            # Nút tải xuống
            csv_data = excel_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Tải file Excel",
                data=csv_data,
                file_name=f"BHXH_{report_type.replace('/', '_')}_{report_month.replace('/', '_')}.csv",
                mime="text/csv"
            )
    
    with tab3:
        st.subheader("📋 Quản lý thay đổi BHXH")
        
        # Thêm thay đổi mới
        with st.expander("➕ Thêm thay đổi BHXH mới"):
            with st.form("add_insurance_change"):
                col1, col2 = st.columns(2)
                
                with col1:
                    emp_name = st.text_input("👤 Họ tên nhân viên:")
                    change_type = st.selectbox("📋 Loại thay đổi:",
                        ["Điều chỉnh lương", "Nghỉ thai sản", "Nghỉ hưu", "Thôi việc", "Đi học"])
                    effective_date = st.date_input("📅 Ngày hiệu lực:")
                
                with col2:
                    old_value = st.text_input("📊 Giá trị cũ:")
                    new_value = st.text_input("🔄 Giá trị mới:")
                    notes = st.text_area("📝 Ghi chú:")
                
                if st.form_submit_button("➕ Thêm thay đổi"):
                    st.success(f"✅ Đã thêm thay đổi BHXH cho {emp_name}!")
        
        # Danh sách thay đổi gần đây
        st.markdown("#### 📋 Thay đổi BHXH gần đây")
        
        recent_changes = pd.DataFrame([
            {"Ngày": "15/12/2024", "Nhân viên": "Nguyễn Văn A", "Loại": "Điều chỉnh lương", 
             "Cũ": "6.900.000", "Mới": "7.320.000", "Trạng thái": "Đã xử lý"},
            {"Ngày": "10/12/2024", "Nhân viên": "Trần Thị B", "Loại": "Nghỉ thai sản", 
             "Cũ": "Đang làm", "Mới": "Nghỉ từ 15/01/2025", "Trạng thái": "Chờ xử lý"},
            {"Ngày": "05/12/2024", "Nhân viên": "Lê Văn C", "Loại": "Nghỉ hưu", 
             "Cũ": "Đang làm", "Mới": "Nghỉ hưu từ 01/03/2025", "Trạng thái": "Đã xử lý"}
        ])
        
        st.dataframe(recent_changes, use_container_width=True)
        
        # Xuất tổng hợp
        if st.button("📊 Xuất báo cáo tổng hợp BHXH tháng", use_container_width=True):
            st.success("✅ Đã xuất báo cáo tổng hợp BHXH!")

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
