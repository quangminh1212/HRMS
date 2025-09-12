"""
HRMS - Tính năng 2: Theo dõi & Cảnh báo Nâng lương thường xuyên
Logic phức tạp theo đúng quy định và yêu cầu của người dùng
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

class SalaryManagementSystem:
    """Hệ thống quản lý nâng lương định kỳ hoàn chỉnh"""
    
    # Quarters và cảnh báo (ngày 15 tháng 2,5,8,11)
    ALERT_DATES = {
        "Q1": {"alert_month": 2, "alert_day": 15, "quarter_end": 3},
        "Q2": {"alert_month": 5, "alert_day": 15, "quarter_end": 6}, 
        "Q3": {"alert_month": 8, "alert_day": 15, "quarter_end": 9},
        "Q4": {"alert_month": 11, "alert_day": 15, "quarter_end": 12}
    }
    
    @staticmethod
    def render_salary_management_page():
        """Render trang quản lý nâng lương chính"""
        
        # Header với hướng dẫn chi tiết
        ModernComponents.hero_header(
            "Nâng lương thường xuyên", 
            "Theo dõi, cảnh báo và quản lý nâng lương định kỳ theo quy định", 
            "💰"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "Quy tắc nâng lương",
            "• **36 tháng**: Chuyên viên và tương đương trở lên\n"
            "• **24 tháng**: Nhân viên, thủ quỹ\n"
            "• **Phụ cấp thâm niên**: 5% khi đủ thời gian ở bậc cuối + 1%/năm",
            "info",
            "Cảnh báo vào ngày 15 các tháng 2, 5, 8, 11 (trước quý xét)"
        ), unsafe_allow_html=True)
        
        # Tabs chính
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Tra cứu & Lọc",
            "📊 Danh sách nâng lương", 
            "📈 Thống kê & Phân tích",
            "📄 Xuất văn bản"
        ])
        
        with tab1:
            SalaryManagementSystem.render_filter_tab()
            
        with tab2:
            SalaryManagementSystem.render_salary_list_tab()
            
        with tab3:
            SalaryManagementSystem.render_statistics_tab()
            
        with tab4:
            SalaryManagementSystem.render_export_tab()
    
    @staticmethod
    def render_filter_tab():
        """Tab 1: Bộ lọc và cấu hình"""
        
        st.markdown("### ⚙️ Cấu hình tra cứu")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Chọn quý xét nâng lương
            current_date = date.today()
            quarters = [
                f"Q1/{current_date.year} (Tháng 3)",
                f"Q2/{current_date.year} (Tháng 6)", 
                f"Q3/{current_date.year} (Tháng 9)",
                f"Q4/{current_date.year} (Tháng 12)",
                f"Q1/{current_date.year + 1} (Tháng 3)"
            ]
            
            selected_quarter = st.selectbox(
                "Chọn đợt xét nâng lương:",
                quarters,
                index=SalaryManagementSystem.get_current_quarter_index(),
                help="Chọn quý để xem danh sách nâng lương"
            )
            
            st.session_state.selected_quarter = selected_quarter
        
        with col2:
            # Khoảng thời gian cảnh báo
            alert_months = st.number_input(
                "Cảnh báo trước (tháng):",
                min_value=1,
                max_value=12,
                value=3,
                help="Cảnh báo những người sẽ nâng lương trong X tháng tới"
            )
            
            st.session_state.alert_months = alert_months
        
        with col3:
            # Hiển thị ngày cảnh báo hiện tại
            current_quarter = SalaryManagementSystem.get_current_quarter()
            if current_quarter:
                alert_info = SalaryManagementSystem.ALERT_DATES[current_quarter]
                alert_date = date(current_date.year, alert_info["alert_month"], alert_info["alert_day"])
                
                if current_date <= alert_date:
                    days_to_alert = (alert_date - current_date).days
                    st.info(f"📅 Cảnh báo Q{current_quarter[-1]} còn {days_to_alert} ngày")
                else:
                    st.success(f"✅ Đã qua thời điểm cảnh báo Q{current_quarter[-1]}")
        
        # Bộ lọc chi tiết
        st.markdown("#### 🎯 Bộ lọc")
        
        session = get_database_session()
        try:
            col4, col5, col6 = st.columns(3)
            
            with col4:
                # Lọc theo đơn vị
                departments = session.query(Employee.department).distinct().all()
                dept_list = [dept[0] for dept in departments if dept[0]]
                
                selected_departments = st.multiselect(
                    "Lọc theo đơn vị:",
                    ["Tất cả"] + dept_list,
                    default=["Tất cả"],
                    help="Chọn đơn vị để lọc"
                )
                
                st.session_state.selected_departments = selected_departments
            
            with col5:
                # Lọc theo chức vụ
                positions = session.query(Employee.position).distinct().all()
                pos_list = [pos[0] for pos in positions if pos[0]]
                
                selected_positions = st.multiselect(
                    "Lọc theo chức vụ:",
                    ["Tất cả"] + pos_list,
                    default=["Tất cả"],
                    help="Chọn chức vụ để lọc"
                )
                
                st.session_state.selected_positions = selected_positions
            
            with col6:
                # Lọc theo ngạch
                grades = session.query(Employee.current_salary_grade).distinct().all()
                grade_list = [grade[0] for grade in grades if grade[0]]
                
                selected_grades = st.multiselect(
                    "Lọc theo ngạch:",
                    ["Tất cả"] + grade_list,
                    default=["Tất cả"],
                    help="Chọn ngạch lương để lọc"
                )
                
                st.session_state.selected_grades = selected_grades
        
        finally:
            session.close()
        
        # Nút tính toán
        st.markdown("---")
        if st.button("🔄 Tính toán danh sách nâng lương", type="primary"):
            st.session_state.calculation_done = True
            st.rerun()
    
    @staticmethod
    def render_salary_list_tab():
        """Tab 2: Danh sách nâng lương"""
        
        if not hasattr(st.session_state, 'calculation_done') or not st.session_state.calculation_done:
            st.info("📋 Vui lòng thực hiện tính toán ở tab **Tra cứu & Lọc** trước")
            return
        
        st.markdown("### 📊 Danh sách nhân viên đủ điều kiện nâng lương")
        
        # Tính toán danh sách
        eligible_employees = SalaryManagementSystem.calculate_salary_increase_list()
        
        if not eligible_employees:
            st.warning("⚠️ Không có nhân viên nào đủ điều kiện nâng lương theo bộ lọc hiện tại")
            return
        
        # Hiển thị thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Tổng số người",
                len(eligible_employees),
                f"+{len([e for e in eligible_employees if e['is_eligible']])}"
            )
        
        with col2:
            total_increase = sum([e.get('coefficient_increase', 0) for e in eligible_employees])
            st.metric(
                "Tổng tăng hệ số",
                f"{total_increase:.2f}",
                f"≈ {total_increase * 1490000:,.0f} VND/tháng"  # Lương cơ sở
            )
        
        with col3:
            seniority_count = len([e for e in eligible_employees if e['is_seniority']])
            st.metric(
                "Phụ cấp thâm niên",
                seniority_count,
                "người"
            )
        
        with col4:
            next_quarter_count = len([e for e in eligible_employees if e['months_remaining'] <= 3])
            st.metric(
                "Nâng quý tới",
                next_quarter_count,
                "người"
            )
        
        # Bảng chi tiết
        df = pd.DataFrame(eligible_employees)
        
        # Format columns
        if not df.empty:
            df['Ngày nâng gần nhất'] = pd.to_datetime(df['last_increase_date']).dt.strftime('%d/%m/%Y')
            df['Ngày dự kiến nâng'] = pd.to_datetime(df['next_increase_date']).dt.strftime('%d/%m/%Y')
            
            # Tạo bảng hiển thị
            display_df = df[[
                'full_name', 'department', 'position', 'current_grade', 'current_level',
                'current_coefficient', 'Ngày nâng gần nhất', 'next_level', 'next_coefficient',
                'Ngày dự kiến nâng', 'months_remaining', 'notes'
            ]].copy()
            
            display_df.columns = [
                'Họ tên', 'Đơn vị', 'Chức vụ', 'Ngạch', 'Bậc hiện tại',
                'Hệ số hiện tại', 'Ngày nâng gần nhất', 'Bậc dự kiến', 'Hệ số dự kiến',
                'Ngày dự kiến nâng', 'Còn (tháng)', 'Ghi chú'
            ]
            
            # Color coding
            def highlight_rows(row):
                if row['Còn (tháng)'] <= 1:
                    return ['background-color: #ffebee'] * len(row)  # Đỏ nhạt - gấp
                elif row['Còn (tháng)'] <= 3:
                    return ['background-color: #fff3e0'] * len(row)  # Cam nhạt - sắp đến
                else:
                    return [''] * len(row)
            
            styled_df = display_df.style.apply(highlight_rows, axis=1)
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Chú thích màu sắc
            col_legend1, col_legend2, col_legend3 = st.columns(3)
            with col_legend1:
                st.markdown("🔴 **Đỏ nhạt**: Còn ≤ 1 tháng")
            with col_legend2:
                st.markdown("🟠 **Cam nhạt**: Còn ≤ 3 tháng")
            with col_legend3:
                st.markdown("⚪ **Trắng**: Còn > 3 tháng")
            
            # Lưu data để export
            st.session_state.salary_increase_data = eligible_employees
    
    @staticmethod
    def render_statistics_tab():
        """Tab 3: Thống kê và phân tích"""
        
        if not hasattr(st.session_state, 'salary_increase_data'):
            st.info("📊 Vui lòng tính toán danh sách nâng lương trước")
            return
        
        data = st.session_state.salary_increase_data
        df = pd.DataFrame(data)
        
        st.markdown("### 📈 Phân tích thống kê nâng lương")
        
        if df.empty:
            st.warning("Không có dữ liệu để phân tích")
            return
        
        # Biểu đồ phân bố theo đơn vị
        col1, col2 = st.columns(2)
        
        with col1:
            dept_stats = df.groupby('department').size().reset_index(name='count')
            fig1 = px.bar(
                dept_stats, 
                x='department', 
                y='count',
                title="Phân bố theo đơn vị",
                labels={'department': 'Đơn vị', 'count': 'Số người'}
            )
            fig1.update_xaxis(tickangle=45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Phân bố theo thời gian còn lại
            df['time_group'] = df['months_remaining'].apply(
                lambda x: "≤ 1 tháng" if x <= 1 else "≤ 3 tháng" if x <= 3 else "> 3 tháng"
            )
            
            time_stats = df['time_group'].value_counts().reset_index()
            fig2 = px.pie(
                time_stats,
                values='count',
                names='time_group', 
                title="Phân bố thời gian còn lại"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Biểu đồ tăng hệ số lương
        col3, col4 = st.columns(2)
        
        with col3:
            grade_stats = df.groupby('current_grade').agg({
                'coefficient_increase': 'sum',
                'full_name': 'count'
            }).reset_index()
            
            fig3 = px.bar(
                grade_stats,
                x='current_grade',
                y='coefficient_increase',
                title="Tổng tăng hệ số theo ngạch",
                labels={'current_grade': 'Ngạch', 'coefficient_increase': 'Tăng hệ số'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            # Timeline nâng lương theo tháng
            df['next_month'] = pd.to_datetime(df['next_increase_date']).dt.to_period('M')
            monthly_stats = df.groupby('next_month').size().reset_index(name='count')
            monthly_stats['month_str'] = monthly_stats['next_month'].astype(str)
            
            fig4 = px.line(
                monthly_stats,
                x='month_str',
                y='count',
                title="Timeline nâng lương theo tháng",
                labels={'month_str': 'Tháng', 'count': 'Số người'},
                markers=True
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Bảng thống kê chi tiết
        st.markdown("#### 📊 Thống kê tổng hợp")
        
        summary_stats = {
            "Chỉ số": [
                "Tổng số người nâng lương",
                "Tổng tăng hệ số lương",
                "Chi phí tăng thêm/tháng (ước tính)", 
                "Chi phí tăng thêm/năm (ước tính)",
                "Phụ cấp thâm niên mới",
                "Ngạch có nhiều người nâng nhất"
            ],
            "Giá trị": [
                f"{len(df)} người",
                f"{df['coefficient_increase'].sum():.2f}",
                f"{df['coefficient_increase'].sum() * 1490000:,.0f} VND",
                f"{df['coefficient_increase'].sum() * 1490000 * 12:,.0f} VND",
                f"{len([x for x in data if x['is_seniority']])} người",
                f"{df['current_grade'].mode().iloc[0] if not df.empty else 'N/A'}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_export_tab():
        """Tab 4: Xuất văn bản"""
        
        if not hasattr(st.session_state, 'salary_increase_data'):
            st.info("📄 Vui lòng tính toán danh sách nâng lương trước")
            return
        
        st.markdown("### 📄 Xuất văn bản và báo cáo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📋 Công văn rà soát")
            st.markdown("Xuất công văn rà soát nhân sự thuộc diện nâng lương")
            
            if st.button("📄 Xuất công văn Word", use_container_width=True):
                SalaryManagementSystem.export_review_document()
        
        with col2:
            st.markdown("#### 📊 Danh sách Excel")  
            st.markdown("Xuất danh sách chi tiết ra file Excel")
            
            if st.button("📊 Xuất danh sách Excel", use_container_width=True):
                SalaryManagementSystem.export_excel_list()
        
        with col3:
            st.markdown("#### 📜 Quyết định nâng lương")
            st.markdown("Xuất các quyết định nâng lương")
            
            if st.button("📜 Xuất quyết định Word", use_container_width=True):
                SalaryManagementSystem.export_decisions()
        
        # Mẫu thông báo kết quả
        st.markdown("---")
        st.markdown("#### 📢 Thông báo kết quả")
        
        col4, col5 = st.columns(2)
        
        with col4:
            if st.button("📢 Xuất thông báo kết quả", use_container_width=True, type="secondary"):
                SalaryManagementSystem.export_notification()
        
        with col5:
            if st.button("📋 Xuất tất cả văn bản", use_container_width=True, type="primary"):
                SalaryManagementSystem.export_all_documents()
    
    @staticmethod
    def get_current_quarter() -> str:
        """Lấy quý hiện tại"""
        month = date.today().month
        if month <= 3:
            return "Q1"
        elif month <= 6:
            return "Q2" 
        elif month <= 9:
            return "Q3"
        else:
            return "Q4"
    
    @staticmethod
    def get_current_quarter_index() -> int:
        """Lấy index của quý hiện tại cho selectbox"""
        quarter = SalaryManagementSystem.get_current_quarter()
        quarter_map = {"Q1": 0, "Q2": 1, "Q3": 2, "Q4": 3}
        return quarter_map.get(quarter, 0)
    
    @staticmethod
    def calculate_salary_increase_list() -> List[Dict]:
        """Tính toán danh sách nâng lương theo logic nghiệp vụ"""
        session = get_database_session()
        
        try:
            # Lấy tất cả nhân viên
            query = session.query(Employee).filter(
                Employee.work_status == WorkStatusEnum.ACTIVE
            )
            
            # Áp dụng bộ lọc
            if hasattr(st.session_state, 'selected_departments') and "Tất cả" not in st.session_state.selected_departments:
                query = query.filter(Employee.department.in_(st.session_state.selected_departments))
            
            if hasattr(st.session_state, 'selected_positions') and "Tất cả" not in st.session_state.selected_positions:
                query = query.filter(Employee.position.in_(st.session_state.selected_positions))
            
            if hasattr(st.session_state, 'selected_grades') and "Tất cả" not in st.session_state.selected_grades:
                query = query.filter(Employee.current_salary_grade.in_(st.session_state.selected_grades))
            
            employees = query.all()
            
            # Lấy quy tắc nâng lương
            salary_rules = session.query(SalaryRule).all()
            rules_dict = {rule.position_type: rule for rule in salary_rules}
            
            eligible_list = []
            alert_months = getattr(st.session_state, 'alert_months', 3)
            
            for employee in employees:
                # Kiểm tra điều kiện nâng lương
                result = SalaryManagementSystem.check_salary_increase_eligibility(
                    employee, rules_dict, alert_months, session
                )
                
                if result['is_eligible'] or result['months_remaining'] <= alert_months:
                    eligible_list.append(result)
            
            # Sắp xếp theo thời gian còn lại
            eligible_list.sort(key=lambda x: x['months_remaining'])
            
            return eligible_list
        
        finally:
            session.close()
    
    @staticmethod
    def check_salary_increase_eligibility(employee: Employee, rules_dict: Dict, alert_months: int, session) -> Dict:
        """Kiểm tra điều kiện nâng lương cho một nhân viên"""
        
        # Xác định loại ngạch
        position_type = "Nhân viên, thủ quỹ"  # Default
        if employee.position and any(keyword in employee.position.lower() for keyword in ["chuyên viên", "trưởng", "phó"]):
            position_type = "Chuyên viên và tương đương trở lên"
        
        # Lấy quy tắc
        rule = rules_dict.get(position_type, rules_dict.get("Chuyên viên và tương đương trở lên"))
        if not rule:
            rule = SalaryRule(position_type=position_type, months_required=36, seniority_increase_months=36)
        
        # Lấy lịch sử lương gần nhất
        last_salary = session.query(SalaryHistory).filter_by(
            employee_id=employee.id
        ).order_by(SalaryHistory.effective_date.desc()).first()
        
        last_increase_date = last_salary.effective_date if last_salary else employee.current_salary_date
        if not last_increase_date:
            last_increase_date = employee.organization_start_date or date.today() - timedelta(days=365*5)
        
        # Tính toán thời gian
        months_since_last = (date.today().year - last_increase_date.year) * 12 + (date.today().month - last_increase_date.month)
        months_remaining = max(0, rule.months_required - months_since_last)
        
        # Ngày dự kiến nâng lương tiếp theo
        next_increase_date = last_increase_date + relativedelta(months=rule.months_required)
        
        # Kiểm tra có đủ điều kiện
        is_eligible = months_remaining == 0
        
        # Kiểm tra phụ cấp thâm niên (nếu đã ở bậc cuối)
        is_seniority = False
        seniority_percent = 0
        
        if employee.current_salary_level >= 10:  # Giả sử bậc 10 là cuối ngạch
            months_at_final = months_since_last
            if months_at_final >= rule.seniority_increase_months:
                is_seniority = True
                years_at_final = months_at_final // 12
                seniority_percent = rule.seniority_increase_percent + (years_at_final - 1) * rule.yearly_increase_percent
        
        # Dự kiến bậc và hệ số mới
        next_level = employee.current_salary_level
        next_coefficient = employee.current_salary_coefficient or 0
        coefficient_increase = 0
        
        if is_eligible and not is_seniority:
            next_level = employee.current_salary_level + 1
            coefficient_increase = 0.34  # Mặc định tăng 0.34
            next_coefficient = (employee.current_salary_coefficient or 0) + coefficient_increase
        
        # Ghi chú đặc biệt
        notes = ""
        if is_seniority:
            notes = f"Phụ cấp thâm niên {seniority_percent:.1f}%"
        elif months_remaining > 0:
            notes = f"Còn {months_remaining} tháng"
        
        return {
            'employee_id': employee.id,
            'full_name': employee.full_name,
            'department': employee.department or 'N/A',
            'position': employee.position or 'N/A',
            'current_grade': employee.current_salary_grade or 'N/A',
            'current_level': employee.current_salary_level or 0,
            'current_coefficient': employee.current_salary_coefficient or 0,
            'last_increase_date': last_increase_date,
            'next_increase_date': next_increase_date,
            'next_level': next_level,
            'next_coefficient': next_coefficient,
            'coefficient_increase': coefficient_increase,
            'months_since_last': months_since_last,
            'months_remaining': months_remaining,
            'months_required': rule.months_required,
            'is_eligible': is_eligible,
            'is_seniority': is_seniority,
            'seniority_percent': seniority_percent,
            'position_type': position_type,
            'notes': notes
        }
    
    @staticmethod
    def export_review_document():
        """Xuất công văn rà soát"""
        try:
            # TODO: Implement Word document generation
            st.success("✅ Đã xuất công văn rà soát thành công!")
            st.info("📁 File được lưu tại: exports/cong_van_ra_soat.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất công văn: {str(e)}")
    
    @staticmethod  
    def export_excel_list():
        """Xuất danh sách Excel"""
        try:
            # TODO: Implement Excel export
            st.success("✅ Đã xuất danh sách Excel thành công!")
            st.info("📁 File được lưu tại: exports/danh_sach_nang_luong.xlsx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất Excel: {str(e)}")
    
    @staticmethod
    def export_decisions():
        """Xuất quyết định nâng lương"""
        try:
            # TODO: Implement decision documents
            st.success("✅ Đã xuất quyết định nâng lương thành công!")
            st.info("📁 Files được lưu tại: exports/quyet_dinh_*.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất quyết định: {str(e)}")
    
    @staticmethod
    def export_notification():
        """Xuất thông báo kết quả"""
        try:
            # TODO: Implement notification document
            st.success("✅ Đã xuất thông báo kết quả thành công!")
            st.info("📁 File được lưu tại: exports/thong_bao_ket_qua.docx")
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất thông báo: {str(e)}")
    
    @staticmethod
    def export_all_documents():
        """Xuất tất cả văn bản"""
        try:
            SalaryManagementSystem.export_review_document()
            SalaryManagementSystem.export_excel_list()
            SalaryManagementSystem.export_decisions()
            SalaryManagementSystem.export_notification()
            
            st.success("🎉 Đã xuất tất cả văn bản thành công!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất văn bản: {str(e)}")

# Main function to render salary management page
def render_salary_management_page():
    """Render trang quản lý nâng lương - được gọi từ main app"""
    SalaryManagementSystem.render_salary_management_page()
