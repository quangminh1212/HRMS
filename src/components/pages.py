"""
HRMS Modern - Additional Pages
Các trang bổ sung với giao diện hiện đại
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from design import DesignTokens, UIComponents

class ModernPages:
    """Class chứa các trang bổ sung cho HRMS Modern"""
    
    @staticmethod
    def salary_management_page():
        """Trang quản lý nâng lương hiện đại"""
        from components import ModernComponents
        
        ModernComponents.hero_header(
            "Quản lý nâng lương",
            "Theo dõi và xử lý nâng lương định kỳ cho nhân viên",
            "💰"
        )
        
        # Tabs hiện đại
        tab1, tab2, tab3 = st.tabs([
            "📅 Lịch cảnh báo", 
            "👥 Danh sách nâng lương", 
            "📄 Xuất báo cáo"
        ])
        
        with tab1:
            # Current quarter info
            current_quarter = f"Q{((datetime.now().month - 1) // 3) + 1}"
            current_year = datetime.now().year
            
            st.markdown(ModernComponents.surface_container(f"""
                <div style="padding: 1.5rem;">
                    <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                        📅 Lịch cảnh báo nâng lương {current_year}
                    </div>
                    <div class="body-medium" style="color: #49454F; margin-bottom: 1.5rem;">
                        Hiện tại: <strong>{current_quarter}/{current_year}</strong>
                    </div>
                </div>
            """, "container-high"), unsafe_allow_html=True)
            
            # Quarterly schedule
            quarters = [
                {"q": "Q1", "alert": "15/02", "review": "31/03", "status": "completed" if datetime.now().month > 3 else "upcoming"},
                {"q": "Q2", "alert": "15/05", "review": "30/06", "status": "completed" if datetime.now().month > 6 else "upcoming"},
                {"q": "Q3", "alert": "15/08", "review": "30/09", "status": "completed" if datetime.now().month > 9 else "upcoming"},
                {"q": "Q4", "alert": "15/11", "review": "31/12", "status": "completed" if datetime.now().month > 12 else "upcoming"}
            ]
            
            col1, col2 = st.columns(2)
            
            for i, quarter in enumerate(quarters):
                col = col1 if i % 2 == 0 else col2
                
                with col:
                    alert_type = "success" if quarter["status"] == "completed" else "warning"
                    status_icon = "✅" if quarter["status"] == "completed" else "⏰"
                    
                    st.markdown(ModernComponents.modern_alert(
                        alert_type,
                        f"{status_icon} {quarter['q']}/{current_year}",
                        f"Cảnh báo: {quarter['alert']}/{current_year} • Xét nâng lương: {quarter['review']}/{current_year}",
                        "Thông tư 08/2013/TT-BNV"
                    ), unsafe_allow_html=True)
            
            # Rules info
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            
            st.markdown(ModernComponents.modern_alert(
                "info",
                "Quy tắc nâng lương định kỳ",
                "Chuyên viên và tương đương trở lên: 36 tháng • Nhân viên, Thủ quỹ: 24 tháng",
                "📖 Căn cứ pháp lý: Thông tư 08/2013/TT-BNV"
            ), unsafe_allow_html=True)
        
        with tab2:
            st.markdown(ModernComponents.surface_container("""
                <div style="padding: 1.5rem;">
                    <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                        👥 Danh sách nhân viên đủ điều kiện
                    </div>
                </div>
            """, "container"), unsafe_allow_html=True)
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                department = st.selectbox(
                    "🏢 Đơn vị",
                    ["Tất cả", "Phòng TCHC", "Phòng TCKT", "Phòng KD"]
                )
            
            with col2:
                position = st.selectbox(
                    "💼 Chức vụ", 
                    ["Tất cả", "Chuyên viên cao cấp", "Chuyên viên chính", "Chuyên viên", "Nhân viên"]
                )
            
            with col3:
                grade = st.selectbox(
                    "📊 Ngạch",
                    ["Tất cả", "A1", "A2", "A3", "B1", "B2", "B3"]
                )
            
            if st.button("🔍 Tính toán danh sách", use_container_width=True):
                # Sample data
                eligible_employees = pd.DataFrame([
                    {
                        "Họ tên": "Nguyễn Văn A",
                        "Chức vụ": "Chuyên viên chính", 
                        "Đơn vị": "Phòng TCHC",
                        "Ngạch hiện tại": "A2",
                        "Hệ số hiện tại": 3.45,
                        "Hệ số mới": 3.66,
                        "Ngày nâng lương": "01/04/2024",
                        "Trạng thái": "Đủ điều kiện"
                    },
                    {
                        "Họ tên": "Trần Thị B",
                        "Chức vụ": "Chuyên viên",
                        "Đơn vị": "Phòng TCKT", 
                        "Ngạch hiện tại": "A1",
                        "Hệ số hiện tại": 2.67,
                        "Hệ số mới": 2.89,
                        "Ngày nâng lương": "15/01/2025",
                        "Trạng thái": "Đủ điều kiện"
                    },
                    {
                        "Họ tên": "Lê Văn C",
                        "Chức vụ": "Nhân viên",
                        "Đơn vị": "Phòng KD",
                        "Ngạch hiện tại": "B1",
                        "Hệ số hiện tại": 2.10,
                        "Hệ số mới": 2.25,
                        "Ngày nâng lương": "10/06/2024", 
                        "Trạng thái": "Chờ xử lý"
                    }
                ])
                
                st.markdown(ModernComponents.modern_alert(
                    "success",
                    "Kết quả tính toán",
                    f"Tìm thấy {len(eligible_employees)} nhân viên đủ điều kiện nâng lương",
                    "Danh sách chi tiết hiển thị bên dưới"
                ), unsafe_allow_html=True)
                
                # Display data table with modern styling
                ModernComponents.data_table(eligible_employees, "📋 Danh sách chi tiết")
        
        with tab3:
            st.markdown(ModernComponents.surface_container("""
                <div style="padding: 1.5rem;">
                    <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                        📄 Xuất báo cáo và văn bản
                    </div>
                </div>
            """, "container"), unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            reports = [
                ("📄 Công văn rà soát", "CV_RaSoat_NangLuong", "Công văn rà soát điều kiện nâng lương"),
                ("📢 Thông báo kết quả", "ThongBao_KetQua", "Thông báo kết quả xét nâng lương"),
                ("⚖️ Quyết định nâng lương", "QuyetDinh_NangLuong", "Quyết định nâng lương chính thức")
            ]
            
            cols = [col1, col2, col3]
            for i, (title, filename, desc) in enumerate(reports):
                with cols[i]:
                    if st.button(title, use_container_width=True, help=desc):
                        st.success(f"✅ Đã xuất {filename}_{datetime.now().strftime('%m_%Y')}.docx")
            
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            
            # Excel export
            st.markdown(ModernComponents.modern_alert(
                "info", 
                "Xuất danh sách Excel",
                "Danh sách chi tiết nhân viên được nâng lương",
                "📊 Bao gồm thông tin đầy đủ cho báo cáo"
            ), unsafe_allow_html=True)
            
            if st.button("📊 Xuất danh sách Excel", use_container_width=True):
                sample_data = pd.DataFrame([
                    {
                        "STT": 1, "Họ tên": "Nguyễn Văn A", "Chức vụ": "Chuyên viên chính",
                        "Đơn vị": "Phòng TCHC", "Ngạch hiện tại": "A2", "Hệ số hiện tại": 3.45,
                        "Ngạch mới": "A2", "Hệ số mới": 3.66, "Thời điểm hưởng": "01/04/2025"
                    },
                    {
                        "STT": 2, "Họ tên": "Trần Thị B", "Chức vụ": "Chuyên viên", 
                        "Đơn vị": "Phòng TCKT", "Ngạch hiện tại": "A1", "Hệ số hiện tại": 2.67,
                        "Ngạch mới": "A1", "Hệ số mới": 2.89, "Thời điểm hưởng": "15/01/2025"
                    }
                ])
                
                st.success("✅ Đã tạo file Excel thành công!")
                ModernComponents.data_table(sample_data, "📊 Preview danh sách Excel")
    
    @staticmethod
    def retirement_tracking_page():
        """Trang theo dõi nghỉ hưu hiện đại"""
        from components import ModernComponents
        
        ModernComponents.hero_header(
            "Theo dõi nghỉ hưu", 
            "Quản lý và theo dõi nhân viên sắp nghỉ hưu",
            "⏰"
        )
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        retirement_metrics = [
            ("📊", "Tổng số", "12", "", "icon-primary"),
            ("⚠️", "Cần thông báo", "3", "+1", "icon-warning"),
            ("📋", "Cần quyết định", "2", "", "icon-error"), 
            ("💰", "Đủ điều kiện nâng lương", "4", "+2", "icon-success")
        ]
        
        cols = [col1, col2, col3, col4]
        for i, (icon, title, value, change, color_class) in enumerate(retirement_metrics):
            with cols[i]:
                st.markdown(
                    ModernComponents.metric_card(icon, title, value, change, color_class),
                    unsafe_allow_html=True
                )
        
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # Retirement timeline
        st.markdown(ModernComponents.surface_container("""
            <div style="padding: 1.5rem;">
                <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                    👥 Danh sách nhân viên sắp nghỉ hưu
                </div>
            </div>
        """, "container"), unsafe_allow_html=True)
        
        # Sample retirement data
        retirement_list = [
            {
                "name": "Nguyễn Văn D", "position": "Trưởng phòng TCHC",
                "birth": "15/03/1964", "retirement": "15/06/2025", 
                "days_left": 185, "priority": "warning"
            },
            {
                "name": "Trần Thị E", "position": "Phó Trưởng phòng TCKT",
                "birth": "10/01/1970", "retirement": "10/05/2025",
                "days_left": 149, "priority": "error" 
            },
            {
                "name": "Lê Văn F", "position": "Chuyên viên cao cấp",
                "birth": "20/02/1965", "retirement": "20/02/2025",
                "days_left": 70, "priority": "error"
            }
        ]
        
        for person in retirement_list:
            if person['days_left'] <= 90:
                alert_type = "error"
                urgency_text = f"🔴 Khẩn cấp - Còn {person['days_left']} ngày"
            elif person['days_left'] <= 180:
                alert_type = "warning" 
                urgency_text = f"🟡 Quan trọng - Còn {person['days_left']} ngày"
            else:
                alert_type = "info"
                urgency_text = f"🔵 Theo dõi - Còn {person['days_left']} ngày"
            
            st.markdown(ModernComponents.modern_alert(
                alert_type,
                f"👤 {person['name']} ({urgency_text})",
                f"Chức vụ: {person['position']} • Nghỉ hưu: {person['retirement']}",
                f"Sinh: {person['birth']} • Cần xử lý thủ tục"
            ), unsafe_allow_html=True)
            
            # Action buttons for each person
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button(f"📢 Thông báo", key=f"notify_{person['name']}"):
                    st.success(f"✅ Đã tạo thông báo nghỉ hưu cho {person['name']}")
            
            with col_b:
                if st.button(f"⚖️ Quyết định", key=f"decision_{person['name']}"):
                    st.success(f"✅ Đã tạo quyết định nghỉ hưu cho {person['name']}")
            
            with col_c:
                if st.button(f"💰 Kiểm tra lương", key=f"salary_{person['name']}"):
                    st.info(f"ℹ️ Đang kiểm tra điều kiện nâng lương trước hạn cho {person['name']}")
        
        # Summary section
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        st.markdown(ModernComponents.modern_alert(
            "info",
            "📋 Thống kê tổng quan",
            "3 nhân viên cần thông báo nghỉ hưu • 2 nhân viên cần quyết định • 4 nhân viên đủ điều kiện nâng lương trước hạn",
            "🔄 Cập nhật hàng ngày vào 8:00 AM"
        ), unsafe_allow_html=True)
    
    @staticmethod
    def reports_dashboard():
        """Dashboard báo cáo hiện đại"""
        from components import ModernComponents
        
        ModernComponents.hero_header(
            "Báo cáo & Thống kê",
            "Phân tích dữ liệu nhân sự và xu hướng phát triển",
            "📊"
        )
        
        # Time period selection
        col1, col2 = st.columns(2)
        
        with col1:
            report_year = st.selectbox(
                "📅 Chọn năm báo cáo",
                ["2024", "2023", "2022"],
                help="Chọn năm để xem báo cáo thống kê"
            )
        
        with col2:
            report_type = st.selectbox(
                "📋 Loại báo cáo",
                ["Tổng quan", "Nhân sự", "Lương thưởng", "Đào tạo"],
                help="Chọn loại báo cáo cụ thể"
            )
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        # Key metrics for the year
        col1, col2, col3, col4 = st.columns(4)
        
        year_metrics = [
            ("💰", "Nâng lương", "25", "+8"),
            ("⏰", "Nghỉ hưu", "12", "-3"), 
            ("📄", "Hợp đồng mới", "15", "+5"),
            ("⬆️", "Bổ nhiệm", "6", "+1")
        ]
        
        cols = [col1, col2, col3, col4]
        for i, (icon, title, value, change) in enumerate(year_metrics):
            with cols[i]:
                st.markdown(
                    ModernComponents.metric_card(icon, title, value, change, "icon-primary"),
                    unsafe_allow_html=True
                )
        
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(ModernComponents.surface_container("""
                <div style="padding: 1.5rem;">
                    <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                        📈 Biến động nhân sự theo tháng
                    </div>
                </div>
            """, "container"), unsafe_allow_html=True)
            
            monthly_data = pd.DataFrame({
                'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
                'Vào': [2, 1, 3, 2, 1, 4, 2, 0, 1, 2, 1, 0],
                'Ra': [1, 0, 2, 1, 3, 1, 0, 2, 1, 0, 1, 2]
            })
            
            fig = px.line(
                monthly_data.melt(id_vars=['Tháng'], var_name='Loại', value_name='Số lượng'), 
                x='Tháng', y='Số lượng', color='Loại',
                color_discrete_map={'Vào': '#6750A4', 'Ra': '#F44336'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Inter",
                font_color="#1C1B1F"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(ModernComponents.surface_container("""
                <div style="padding: 1.5rem;">
                    <div class="title-large" style="margin-bottom: 1rem; color: #1C1B1F;">
                        🎓 Phân tích thôi việc theo trình độ
                    </div>
                </div>
            """, "container"), unsafe_allow_html=True)
            
            education_data = pd.DataFrame({
                'Trình độ': ['Cử nhân', 'Thạc sĩ', 'Tiến sĩ', 'Khác'],
                'Số lượng': [5, 2, 1, 0]
            })
            
            fig2 = px.bar(
                education_data, x='Trình độ', y='Số lượng',
                color='Số lượng', color_continuous_scale='Reds'
            )
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family="Inter", 
                font_color="#1C1B1F",
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Insights section
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(ModernComponents.modern_alert(
                "warning",
                "⚠️ Cảnh báo xu hướng",
                "Tỷ lệ thôi việc cao ở nhóm 25-35 tuổi, cần có biện pháp giữ chân nhân tài",
                "💡 Đề xuất: Cải thiện chế độ đãi ngộ và môi trường làm việc"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(ModernComponents.modern_alert(
                "success",
                "✅ Điểm tích cực",
                f"Tăng trưởng nhân sự {report_year}: +8 người so với năm trước",
                "📈 Xu hướng tích cực trong tuyển dụng và giữ chân nhân viên"
            ), unsafe_allow_html=True)
        
        # Export section
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        if st.button("📊 Xuất báo cáo tổng hợp", use_container_width=True):
            st.success(f"✅ Đã xuất báo cáo tổng hợp năm {report_year}!")
            st.info("📁 File đã được lưu vào thư mục exports/")
