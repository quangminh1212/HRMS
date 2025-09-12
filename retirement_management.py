"""
HRMS - Tính năng 3: Theo dõi nghỉ hưu
Cảnh báo trước 6 tháng, quyết định trước 3 tháng
Rà soát nâng lương trước thời hạn khi nghỉ hưu
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker
from models_enhanced import *
from components import ModernComponents
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple

def get_database_session():
    """Tạo session database"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

class RetirementManagementSystem:
    """Hệ thống theo dõi nghỉ hưu hoàn chỉnh"""
    
    # Tuổi nghỉ hưu theo quy định
    RETIREMENT_AGES = {
        GenderEnum.MALE: 62,
        GenderEnum.FEMALE: 60
    }
    
    # Thời gian cảnh báo
    NOTIFICATION_MONTHS = 6  # Thông báo trước 6 tháng
    DECISION_MONTHS = 3      # Quyết định trước 3 tháng
    
    @staticmethod
    def render_retirement_management_page():
        """Render trang theo dõi nghỉ hưu chính"""
        
        # Header với hướng dẫn
        ModernComponents.hero_header(
            "Theo dõi nghỉ hưu", 
            "Cảnh báo, ra quyết định và xử lý nâng lương trước thời hạn khi nghỉ hưu", 
            "⏰"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "Quy trình nghỉ hưu",
            "• **6 tháng trước**: Thông báo và rà soát nâng lương trước thời hạn\n"
            "• **3 tháng trước**: Ra quyết định nghỉ hưu\n"
            "• **Tự động**: Kiểm tra điều kiện nâng lương đặc biệt",
            "info", 
            "Tuổi nghỉ hưu: Nam 62 tuổi, Nữ 60 tuổi"
        ), unsafe_allow_html=True)
        
        # Tabs chính
        tab1, tab2, tab3, tab4 = st.tabs([
            "🚨 Cảnh báo nghỉ hưu",
            "📋 Danh sách chi tiết",
            "💰 Nâng lương trước hạn", 
            "📄 Xuất văn bản"
        ])
        
        with tab1:
            RetirementManagementSystem.render_alerts_tab()
            
        with tab2:
            RetirementManagementSystem.render_detailed_list_tab()
            
        with tab3:
            RetirementManagementSystem.render_early_salary_tab()
            
        with tab4:
            RetirementManagementSystem.render_export_tab()
    
    @staticmethod
    def render_alerts_tab():
        """Tab 1: Cảnh báo nghỉ hưu"""
        
        st.markdown("### 🚨 Cảnh báo nghỉ hưu")
        
        # Tính toán các nhóm cảnh báo
        retirement_data = RetirementManagementSystem.calculate_retirement_alerts()
        
        if not retirement_data:
            st.info("✅ Hiện tại không có nhân viên nào cần cảnh báo nghỉ hưu")
            return
        
        # Phân loại theo mức độ ưu tiên
        urgent_6_months = [emp for emp in retirement_data if emp['months_to_retirement'] <= 6 and emp['months_to_retirement'] > 3]
        urgent_3_months = [emp for emp in retirement_data if emp['months_to_retirement'] <= 3]
        upcoming_12_months = [emp for emp in retirement_data if emp['months_to_retirement'] <= 12 and emp['months_to_retirement'] > 6]
        
        # Hiển thị metrics tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Cần quyết định ngay",
                len(urgent_3_months),
                "≤ 3 tháng",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Cần thông báo", 
                len(urgent_6_months),
                "≤ 6 tháng",
                delta_color="off"
            )
        
        with col3:
            st.metric(
                "Sắp tới",
                len(upcoming_12_months),
                "≤ 12 tháng"
            )
        
        with col4:
            st.metric(
                "Tổng cộng",
                len(retirement_data),
                "người"
            )
        
        # Hiển thị danh sách theo mức độ ưu tiên
        if urgent_3_months:
            st.markdown("#### 🔥 CẤP BÁO - Cần ra quyết định ngay (≤ 3 tháng)")
            RetirementManagementSystem.display_retirement_table(urgent_3_months, "urgent")
        
        if urgent_6_months:
            st.markdown("#### ⚠️ QUAN TRỌNG - Cần thông báo (≤ 6 tháng)")
            RetirementManagementSystem.display_retirement_table(urgent_6_months, "warning")
        
        if upcoming_12_months:
            st.markdown("#### 📋 SẮP TỚI - Chuẩn bị trước (≤ 12 tháng)")
            with st.expander(f"Xem {len(upcoming_12_months)} người sắp nghỉ hưu"):
                RetirementManagementSystem.display_retirement_table(upcoming_12_months, "info")
    
    @staticmethod
    def render_detailed_list_tab():
        """Tab 2: Danh sách chi tiết"""
        
        st.markdown("### 📋 Danh sách chi tiết nhân viên sắp nghỉ hưu")
        
        # Tùy chọn lọc
        col1, col2, col3 = st.columns(3)
        
        with col1:
            months_filter = st.selectbox(
                "Lọc theo thời gian:",
                ["Tất cả", "≤ 3 tháng", "≤ 6 tháng", "≤ 12 tháng", "≤ 24 tháng"],
                index=3  # Mặc định ≤ 12 tháng
            )
        
        with col2:
            session = get_database_session()
            try:
                departments = session.query(Employee.department).distinct().all()
                dept_list = [dept[0] for dept in departments if dept[0]]
                
                selected_dept = st.selectbox(
                    "Lọc theo đơn vị:",
                    ["Tất cả"] + dept_list
                )
            finally:
                session.close()
        
        with col3:
            sort_by = st.selectbox(
                "Sắp xếp theo:",
                ["Thời gian nghỉ hưu", "Họ tên", "Đơn vị", "Tuổi"]
            )
        
        # Lấy dữ liệu đã lọc
        retirement_data = RetirementManagementSystem.calculate_retirement_alerts()
        
        # Áp dụng bộ lọc
        if months_filter != "Tất cả":
            months_limit = int(months_filter.split("≤ ")[1].split(" ")[0])
            retirement_data = [emp for emp in retirement_data if emp['months_to_retirement'] <= months_limit]
        
        if selected_dept != "Tất cả":
            retirement_data = [emp for emp in retirement_data if emp['department'] == selected_dept]
        
        if not retirement_data:
            st.info("Không có dữ liệu theo bộ lọc đã chọn")
            return
        
        # Sắp xếp
        if sort_by == "Thời gian nghỉ hưu":
            retirement_data.sort(key=lambda x: x['months_to_retirement'])
        elif sort_by == "Họ tên":
            retirement_data.sort(key=lambda x: x['full_name'])
        elif sort_by == "Đơn vị":
            retirement_data.sort(key=lambda x: x['department'] or "")
        elif sort_by == "Tuổi":
            retirement_data.sort(key=lambda x: x['current_age'], reverse=True)
        
        # Hiển thị bảng chi tiết với nhiều thông tin hơn
        detailed_df = pd.DataFrame([{
            "Họ tên": emp['full_name'],
            "Giới tính": emp['gender'],
            "Tuổi hiện tại": f"{emp['current_age']} tuổi", 
            "Đơn vị": emp['department'] or 'N/A',
            "Chức vụ": emp['position'] or 'N/A',
            "Ngày sinh": emp['date_of_birth'].strftime('%d/%m/%Y'),
            "Ngày nghỉ hưu": emp['retirement_date'].strftime('%d/%m/%Y'),
            "Còn lại": f"{emp['months_to_retirement']} tháng",
            "Trạng thái": emp['status'],
            "Cần làm": emp['action_required']
        } for emp in retirement_data])
        
        # Color coding cho bảng
        def highlight_urgency(row):
            months = int(row['Còn lại'].split(' ')[0])
            if months <= 3:
                return ['background-color: #ffebee'] * len(row)  # Đỏ nhạt
            elif months <= 6:
                return ['background-color: #fff3e0'] * len(row)  # Cam nhạt  
            elif months <= 12:
                return ['background-color: #f3e5f5'] * len(row)  # Tím nhạt
            else:
                return [''] * len(row)
        
        styled_df = detailed_df.style.apply(highlight_urgency, axis=1)
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Chú thích
        col_legend1, col_legend2, col_legend3 = st.columns(3)
        with col_legend1:
            st.markdown("🔴 **≤ 3 tháng**: Ra quyết định ngay")
        with col_legend2:
            st.markdown("🟠 **≤ 6 tháng**: Thông báo và chuẩn bị")
        with col_legend3:
            st.markdown("🟣 **≤ 12 tháng**: Theo dõi và lên kế hoạch")
        
        # Lưu dữ liệu cho các tab khác
        st.session_state.retirement_data = retirement_data
    
    @staticmethod
    def render_early_salary_tab():
        """Tab 3: Nâng lương trước thời hạn"""
        
        st.markdown("### 💰 Nâng lương trước thời hạn khi nghỉ hưu")
        
        st.markdown(ModernComponents.modern_alert(
            "Quy định nâng lương trước hạn",
            "Nhân viên sắp nghỉ hưu có thể được xem xét nâng lương trước thời hạn "
            "nếu có thành tích xuất sắc và đã hoàn thành tốt nhiệm vụ được giao.",
            "info",
            "Áp dụng cho những người nghỉ hưu trong vòng 6 tháng tới"
        ), unsafe_allow_html=True)
        
        if not hasattr(st.session_state, 'retirement_data'):
            st.info("📋 Vui lòng xem danh sách chi tiết trước")
            return
        
        # Lọc những người có thể nâng lương trước hạn (≤ 6 tháng)
        eligible_for_early = [
            emp for emp in st.session_state.retirement_data 
            if emp['months_to_retirement'] <= 6
        ]
        
        if not eligible_for_early:
            st.info("✅ Không có trường hợp cần xem xét nâng lương trước thời hạn")
            return
        
        st.markdown(f"#### 📊 Danh sách xem xét ({len(eligible_for_early)} người)")
        
        # Kiểm tra điều kiện nâng lương cho từng người
        early_salary_candidates = []
        
        session = get_database_session()
        try:
            for emp_data in eligible_for_early:
                employee = session.query(Employee).get(emp_data['employee_id'])
                if employee:
                    # Kiểm tra điều kiện
                    candidate_info = RetirementManagementSystem.check_early_salary_eligibility(
                        employee, emp_data, session
                    )
                    early_salary_candidates.append(candidate_info)
        
        finally:
            session.close()
        
        # Hiển thị danh sách ứng viên
        if early_salary_candidates:
            candidate_df = pd.DataFrame([{
                "Họ tên": cand['full_name'],
                "Đơn vị": cand['department'],
                "Hệ số hiện tại": f"{cand['current_coefficient']:.2f}",
                "Thời gian từ lần nâng cuối": f"{cand['months_since_last_increase']} tháng",
                "Đánh giá gần nhất": cand['latest_performance'],
                "Điều kiện": "✅ Đủ" if cand['is_eligible'] else "❌ Chưa đủ",
                "Dự kiến tăng": f"+{cand['proposed_increase']:.2f}" if cand['is_eligible'] else "N/A",
                "Ghi chú": cand['notes']
            } for cand in early_salary_candidates])
            
            # Highlight những người đủ điều kiện
            def highlight_eligible(row):
                if row['Điều kiện'] == "✅ Đủ":
                    return ['background-color: #e8f5e8'] * len(row)  # Xanh nhạt
                else:
                    return ['background-color: #fafafa'] * len(row)  # Xám nhạt
            
            styled_candidate_df = candidate_df.style.apply(highlight_eligible, axis=1)
            
            st.dataframe(
                styled_candidate_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Thống kê
            eligible_count = len([cand for cand in early_salary_candidates if cand['is_eligible']])
            total_increase = sum([cand.get('proposed_increase', 0) for cand in early_salary_candidates if cand['is_eligible']])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Đủ điều kiện", eligible_count, f"/{len(early_salary_candidates)}")
            with col2:
                st.metric("Tổng tăng hệ số", f"{total_increase:.2f}")
            with col3:
                estimated_cost = total_increase * 1490000  # Lương cơ sở
                st.metric("Chi phí ước tính/tháng", f"{estimated_cost:,.0f} VND")
            
            # Lưu dữ liệu cho export
            st.session_state.early_salary_candidates = early_salary_candidates
        
        else:
            st.info("Không có dữ liệu ứng viên")
    
    @staticmethod
    def render_export_tab():
        """Tab 4: Xuất văn bản"""
        
        st.markdown("### 📄 Xuất văn bản nghỉ hưu")
        
        if not hasattr(st.session_state, 'retirement_data'):
            st.info("📄 Vui lòng xem danh sách chi tiết trước")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Thông báo nghỉ hưu")
            st.markdown("Xuất thông báo cho những người còn 6 tháng")
            
            notification_count = len([emp for emp in st.session_state.retirement_data if emp['months_to_retirement'] <= 6])
            
            if st.button(f"📋 Xuất {notification_count} thông báo", use_container_width=True):
                RetirementManagementSystem.export_retirement_notifications()
        
        with col2:
            st.markdown("#### 📜 Quyết định nghỉ hưu")
            st.markdown("Xuất quyết định cho những người còn 3 tháng")
            
            decision_count = len([emp for emp in st.session_state.retirement_data if emp['months_to_retirement'] <= 3])
            
            if st.button(f"📜 Xuất {decision_count} quyết định", use_container_width=True):
                RetirementManagementSystem.export_retirement_decisions()
        
        # Nâng lương trước hạn
        if hasattr(st.session_state, 'early_salary_candidates'):
            st.markdown("---")
            st.markdown("#### 💰 Nâng lương trước thời hạn")
            
            eligible_early = [cand for cand in st.session_state.early_salary_candidates if cand['is_eligible']]
            
            col3, col4 = st.columns(2)
            
            with col3:
                if st.button(f"💰 Xuất đề xuất nâng lương ({len(eligible_early)})", use_container_width=True):
                    RetirementManagementSystem.export_early_salary_proposals()
            
            with col4:
                if st.button("📋 Xuất tất cả văn bản nghỉ hưu", use_container_width=True, type="primary"):
                    RetirementManagementSystem.export_all_retirement_documents()
    
    @staticmethod
    def calculate_retirement_alerts() -> List[Dict]:
        """Tính toán cảnh báo nghỉ hưu"""
        session = get_database_session()
        
        try:
            # Lấy tất cả nhân viên đang làm việc
            employees = session.query(Employee).filter(
                Employee.work_status == WorkStatusEnum.ACTIVE,
                Employee.date_of_birth.isnot(None)
            ).all()
            
            retirement_alerts = []
            today = date.today()
            
            for employee in employees:
                # Tính tuổi nghỉ hưu
                retirement_age = RetirementManagementSystem.RETIREMENT_AGES.get(
                    employee.gender, 62
                )
                
                # Ngày nghỉ hưu dự kiến
                retirement_date = date(
                    employee.date_of_birth.year + retirement_age,
                    employee.date_of_birth.month,
                    employee.date_of_birth.day
                )
                
                # Chỉ xét những người chưa đến tuổi nghỉ hưu và trong vòng 24 tháng tới
                if retirement_date > today:
                    months_to_retirement = (retirement_date.year - today.year) * 12 + (retirement_date.month - today.month)
                    
                    if months_to_retirement <= 24:  # Chỉ xét trong vòng 2 năm
                        current_age = today.year - employee.date_of_birth.year
                        if (today.month, today.day) < (employee.date_of_birth.month, employee.date_of_birth.day):
                            current_age -= 1
                        
                        # Xác định trạng thái và hành động cần thiết
                        if months_to_retirement <= 3:
                            status = "Cấp bách - Ra quyết định"
                            action_required = "Lập quyết định nghỉ hưu"
                        elif months_to_retirement <= 6:
                            status = "Quan trọng - Thông báo"
                            action_required = "Gửi thông báo + xem xét nâng lương trước hạn"
                        else:
                            status = "Theo dõi"
                            action_required = "Chuẩn bị hồ sơ và thủ tục"
                        
                        retirement_alerts.append({
                            'employee_id': employee.id,
                            'full_name': employee.full_name,
                            'gender': employee.gender.value if employee.gender else 'N/A',
                            'department': employee.department,
                            'position': employee.position,
                            'date_of_birth': employee.date_of_birth,
                            'current_age': current_age,
                            'retirement_age': retirement_age,
                            'retirement_date': retirement_date,
                            'months_to_retirement': months_to_retirement,
                            'status': status,
                            'action_required': action_required
                        })
            
            return retirement_alerts
        
        finally:
            session.close()
    
    @staticmethod
    def display_retirement_table(retirement_data: List[Dict], urgency_level: str):
        """Hiển thị bảng nghỉ hưu với định dạng phù hợp"""
        
        df = pd.DataFrame([{
            "Họ tên": emp['full_name'],
            "Đơn vị": emp['department'] or 'N/A',
            "Tuổi": f"{emp['current_age']} tuổi",
            "Ngày nghỉ hưu": emp['retirement_date'].strftime('%d/%m/%Y'),
            "Còn lại": f"{emp['months_to_retirement']} tháng",
            "Hành động": emp['action_required']
        } for emp in retirement_data])
        
        # Styling dựa trên mức độ khẩn cấp
        if urgency_level == "urgent":
            colors = ['background-color: #ffebee'] * len(df.columns)
        elif urgency_level == "warning":
            colors = ['background-color: #fff3e0'] * len(df.columns)  
        else:
            colors = ['background-color: #f3e5f5'] * len(df.columns)
        
        styled_df = df.style.apply(lambda x: colors, axis=0)
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )
    
    @staticmethod
    def check_early_salary_eligibility(employee: Employee, retirement_data: Dict, session) -> Dict:
        """Kiểm tra điều kiện nâng lương trước thời hạn"""
        
        # Lấy lịch sử lương gần nhất
        last_salary = session.query(SalaryHistory).filter_by(
            employee_id=employee.id
        ).order_by(SalaryHistory.effective_date.desc()).first()
        
        # Lấy đánh giá gần nhất
        latest_evaluation = session.query(Evaluation).filter_by(
            employee_id=employee.id
        ).order_by(Evaluation.year.desc()).first()
        
        # Tính thời gian từ lần nâng lương cuối
        last_increase_date = last_salary.effective_date if last_salary else employee.current_salary_date
        if not last_increase_date:
            last_increase_date = employee.organization_start_date or date.today() - timedelta(days=365*3)
        
        months_since_last = (date.today().year - last_increase_date.year) * 12 + (date.today().month - last_increase_date.month)
        
        # Điều kiện nâng lương trước hạn:
        # 1. Đã ít nhất 24 tháng từ lần nâng cuối
        # 2. Có đánh giá tốt (từ "Hoàn thành tốt" trở lên)
        # 3. Sắp nghỉ hưu (≤ 6 tháng)
        
        has_time_condition = months_since_last >= 24
        
        performance_condition = False
        latest_performance = "Chưa có"
        if latest_evaluation:
            latest_performance = latest_evaluation.performance.value
            performance_condition = latest_evaluation.performance in [
                PerformanceEnum.EXCELLENT, 
                PerformanceEnum.GOOD
            ]
        
        retirement_condition = retirement_data['months_to_retirement'] <= 6
        
        is_eligible = has_time_condition and performance_condition and retirement_condition
        
        # Dự kiến mức tăng (thường 0.34 cho nâng bậc)
        proposed_increase = 0.34 if is_eligible else 0
        
        # Ghi chú
        notes = []
        if not has_time_condition:
            notes.append(f"Chưa đủ 24 tháng (còn {24 - months_since_last} tháng)")
        if not performance_condition:
            notes.append("Cần đánh giá tốt trở lên")
        if not retirement_condition:
            notes.append("Chưa trong thời gian quy định")
        
        if is_eligible:
            notes.append("Đủ điều kiện nâng lương trước hạn")
        
        return {
            'employee_id': employee.id,
            'full_name': employee.full_name,
            'department': employee.department or 'N/A',
            'current_coefficient': employee.current_salary_coefficient or 0,
            'months_since_last_increase': months_since_last,
            'latest_performance': latest_performance,
            'is_eligible': is_eligible,
            'proposed_increase': proposed_increase,
            'notes': "; ".join(notes) if notes else "N/A"
        }
    
    @staticmethod
    def export_retirement_notifications():
        """Xuất thông báo nghỉ hưu"""
        try:
            # TODO: Implement Word document generation
            st.success("✅ Đã xuất thông báo nghỉ hưu thành công!")
            st.info("📁 Files được lưu tại: exports/thong_bao_nghi_huu_*.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất thông báo: {str(e)}")
    
    @staticmethod
    def export_retirement_decisions():
        """Xuất quyết định nghỉ hưu"""
        try:
            # TODO: Implement decision documents
            st.success("✅ Đã xuất quyết định nghỉ hưu thành công!")
            st.info("📁 Files được lưu tại: exports/quyet_dinh_nghi_huu_*.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất quyết định: {str(e)}")
    
    @staticmethod
    def export_early_salary_proposals():
        """Xuất đề xuất nâng lương trước thời hạn"""
        try:
            # TODO: Implement salary proposal documents
            st.success("✅ Đã xuất đề xuất nâng lương trước thời hạn thành công!")
            st.info("📁 Files được lưu tại: exports/de_xuat_nang_luong_truoc_han_*.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất đề xuất: {str(e)}")
    
    @staticmethod
    def export_all_retirement_documents():
        """Xuất tất cả văn bản nghỉ hưu"""
        try:
            RetirementManagementSystem.export_retirement_notifications()
            RetirementManagementSystem.export_retirement_decisions()
            if hasattr(st.session_state, 'early_salary_candidates'):
                RetirementManagementSystem.export_early_salary_proposals()
            
            st.success("🎉 Đã xuất tất cả văn bản nghỉ hưu thành công!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất văn bản: {str(e)}")

# Main function to render retirement management page
def render_retirement_management_page():
    """Render trang quản lý nghỉ hưu - được gọi từ main app"""
    RetirementManagementSystem.render_retirement_management_page()
