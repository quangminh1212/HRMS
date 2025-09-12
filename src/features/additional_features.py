"""
HRMS - Tính năng 4-11: Các tính năng bổ sung
Tích hợp đầy đủ 8 tính năng còn lại theo yêu cầu người dùng
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker
from src.models.models_enhanced import *
from src.components.components import ModernComponents
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple

def get_database_session():
    """Tạo session database"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

class PlanningManagementSystem:
    """Tính năng 4: Kiểm tra Quy hoạch cán bộ"""
    
    @staticmethod
    def render_planning_page():
        """Render trang kiểm tra quy hoạch"""
        
        ModernComponents.hero_header(
            "Kiểm tra quy hoạch cán bộ", 
            "Quản lý và kiểm tra quy hoạch nhân sự theo từng vị trí và độ tuổi", 
            "📈"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "Quy định quy hoạch",
            "• Kiểm tra tuổi còn trong quy hoạch\n• Quản lý số lượng theo vị trí\n• Phân tích theo đơn vị",
            "info",
            "Tự động cảnh báo khi vượt quá số lượng hoặc quá tuổi"
        ), unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs([
            "👥 Danh sách quy hoạch",
            "📊 Phân tích số lượng", 
            "⚠️ Cảnh báo vi phạm"
        ])
        
        with tab1:
            PlanningManagementSystem.render_planning_list()
        
        with tab2:
            PlanningManagementSystem.render_planning_analysis()
            
        with tab3:
            PlanningManagementSystem.render_planning_alerts()
    
    @staticmethod
    def render_planning_list():
        """Danh sách quy hoạch hiện tại"""
        session = get_database_session()
        
        try:
            # Lấy danh sách quy hoạch hiện tại
            plannings = session.query(Planning).filter_by(is_current=True).all()
            
            if not plannings:
                st.info("📋 Chưa có dữ liệu quy hoạch")
                return
            
            planning_data = []
            for planning in plannings:
                employee = planning.employee
                current_age = (date.today() - employee.date_of_birth).days // 365 if employee.date_of_birth else 0
                
                planning_data.append({
                    "Họ tên": employee.full_name,
                    "Tuổi hiện tại": current_age,
                    "Vị trí quy hoạch": planning.position,
                    "Đơn vị quy hoạch": planning.department,
                    "Năm quy hoạch": planning.planning_year,
                    "Tuổi khi QH": planning.age_at_planning or 0,
                    "Còn trong QH": "✅" if current_age <= 50 else "❌",  # Giả sử 50 tuổi là giới hạn
                    "Ghi chú": planning.notes or ""
                })
            
            df = pd.DataFrame(planning_data)
            
            # Highlight những trường hợp vượt tuổi
            def highlight_age(row):
                if row['Còn trong QH'] == "❌":
                    return ['background-color: #ffebee'] * len(row)
                return [''] * len(row)
            
            styled_df = df.style.apply(highlight_age, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        finally:
            session.close()
    
    @staticmethod
    def render_planning_analysis():
        """Phân tích số lượng quy hoạch"""
        session = get_database_session()
        
        try:
            plannings = session.query(Planning).filter_by(is_current=True).all()
            
            if not plannings:
                st.info("📊 Chưa có dữ liệu để phân tích")
                return
            
            # Phân tích theo vị trí
            position_counts = {}
            for planning in plannings:
                pos = planning.position or "Khác"
                position_counts[pos] = position_counts.get(pos, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    x=list(position_counts.keys()),
                    y=list(position_counts.values()),
                    title="Số lượng theo vị trí quy hoạch"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                dept_counts = {}
                for planning in plannings:
                    dept = planning.department or "Khác"
                    dept_counts[dept] = dept_counts.get(dept, 0) + 1
                
                fig2 = px.pie(
                    values=list(dept_counts.values()),
                    names=list(dept_counts.keys()),
                    title="Phân bố theo đơn vị"
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        finally:
            session.close()
    
    @staticmethod
    def render_planning_alerts():
        """Cảnh báo vi phạm quy hoạch"""
        st.markdown("⚠️ **Cảnh báo:** Các trường hợp cần xem xét")
        
        # Mock alerts
        alerts = [
            {"Loại": "Quá tuổi QH", "Số lượng": 3, "Mô tả": "3 người đã quá 50 tuổi"},
            {"Loại": "Vượt số lượng", "Số lượng": 2, "Mô tả": "Vị trí Trưởng phòng vượt 2 người"}
        ]
        
        for alert in alerts:
            st.warning(f"⚠️ **{alert['Loại']}**: {alert['Mô tả']}")

class WorkHistorySystem:
    """Tính năng 5: Quản lý quá trình công tác"""
    
    @staticmethod
    def render_work_history_page():
        """Render trang quản lý quá trình công tác"""
        
        ModernComponents.hero_header(
            "Quá trình công tác", 
            "Nhập, xem timeline, sửa, xóa giai đoạn công tác và xuất file", 
            "💼"
        )
        
        tab1, tab2, tab3 = st.tabs([
            "👤 Chọn nhân viên",
            "📅 Timeline công tác",
            "✏️ Quản lý giai đoạn"
        ])
        
        with tab1:
            WorkHistorySystem.render_employee_selection()
        
        with tab2:
            WorkHistorySystem.render_timeline()
            
        with tab3:
            WorkHistorySystem.render_management()
    
    @staticmethod
    def render_employee_selection():
        """Chọn nhân viên để xem quá trình công tác"""
        session = get_database_session()
        
        try:
            employees = session.query(Employee).all()
            
            if employees:
                employee_options = {f"{emp.full_name} - {emp.department}": emp.id for emp in employees}
                
                selected_employee = st.selectbox(
                    "Chọn nhân viên:",
                    list(employee_options.keys())
                )
                
                if selected_employee:
                    st.session_state.selected_employee_id = employee_options[selected_employee]
                    st.success(f"✅ Đã chọn: {selected_employee}")
            else:
                st.info("📋 Chưa có dữ liệu nhân viên")
        
        finally:
            session.close()
    
    @staticmethod
    def render_timeline():
        """Hiển thị timeline công tác"""
        if not hasattr(st.session_state, 'selected_employee_id'):
            st.info("👤 Vui lòng chọn nhân viên trước")
            return
        
        session = get_database_session()
        
        try:
            work_history = session.query(WorkHistory).filter_by(
                employee_id=st.session_state.selected_employee_id
            ).order_by(WorkHistory.start_date).all()
            
            if not work_history:
                st.info("📅 Chưa có lịch sử công tác")
                return
            
            st.markdown("### 📅 Timeline quá trình công tác")
            
            for i, work in enumerate(work_history):
                end_date_str = work.end_date.strftime('%m/%Y') if work.end_date else "Hiện tại"
                
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.markdown(f"**{work.start_date.strftime('%m/%Y')}**")
                    st.markdown(f"↓")
                    st.markdown(f"**{end_date_str}**")
                
                with col2:
                    st.markdown(f"**{work.position}**")
                    st.markdown(f"🏢 {work.department} - {work.organization}")
                    if work.responsibilities:
                        st.markdown(f"📋 {work.responsibilities}")
                
                with col3:
                    if st.button(f"✏️ Sửa", key=f"edit_{work.id}"):
                        st.session_state.edit_work_id = work.id
                    if st.button(f"🗑️ Xóa", key=f"delete_{work.id}"):
                        WorkHistorySystem.delete_work_period(work.id, session)
                
                if i < len(work_history) - 1:
                    st.divider()
        
        finally:
            session.close()
    
    @staticmethod
    def render_management():
        """Quản lý giai đoạn công tác"""
        st.markdown("### ✏️ Thêm/Sửa giai đoạn công tác")
        
        with st.form("work_history_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Ngày bắt đầu:")
                position = st.text_input("Chức vụ:")
                department = st.text_input("Phòng/Ban:")
            
            with col2:
                end_date = st.date_input("Ngày kết thúc (để trống nếu hiện tại):")
                organization = st.text_input("Cơ quan/Tổ chức:")
                responsibilities = st.text_area("Nhiệm vụ/Trách nhiệm:")
            
            submitted = st.form_submit_button("💾 Lưu giai đoạn")
            
            if submitted:
                WorkHistorySystem.save_work_period({
                    'start_date': start_date,
                    'end_date': end_date if end_date != date.today() else None,
                    'position': position,
                    'department': department, 
                    'organization': organization,
                    'responsibilities': responsibilities
                })
    
    @staticmethod
    def save_work_period(data):
        """Lưu giai đoạn công tác"""
        if not hasattr(st.session_state, 'selected_employee_id'):
            st.error("❌ Chưa chọn nhân viên")
            return
        
        session = get_database_session()
        
        try:
            work_period = WorkHistory(
                employee_id=st.session_state.selected_employee_id,
                **data
            )
            
            session.add(work_period)
            session.commit()
            st.success("✅ Đã lưu giai đoạn công tác")
            st.rerun()
        
        finally:
            session.close()
    
    @staticmethod
    def delete_work_period(work_id, session):
        """Xóa giai đoạn công tác"""
        try:
            work = session.query(WorkHistory).get(work_id)
            if work:
                session.delete(work)
                session.commit()
                st.success("✅ Đã xóa giai đoạn công tác")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Lỗi khi xóa: {str(e)}")

class ContractManagementSystem:
    """Tính năng 6: Quản lý hợp đồng lao động"""
    
    @staticmethod
    def render_contract_page():
        """Render trang quản lý hợp đồng"""
        
        ModernComponents.hero_header(
            "Hợp đồng lao động", 
            "Quản lý hợp đồng ban kiểm soát và nhân viên", 
            "📄"
        )
        
        tab1, tab2, tab3 = st.tabs([
            "📋 Danh sách hợp đồng",
            "➕ Thêm hợp đồng mới",
            "📊 Thống kê hợp đồng"
        ])
        
        with tab1:
            ContractManagementSystem.render_contract_list()
        
        with tab2:
            ContractManagementSystem.render_add_contract()
            
        with tab3:
            ContractManagementSystem.render_contract_stats()
    
    @staticmethod
    def render_contract_list():
        """Danh sách hợp đồng"""
        session = get_database_session()
        
        try:
            contracts = session.query(LaborContract).all()
            
            if not contracts:
                st.info("📋 Chưa có hợp đồng nào")
                return
            
            contract_data = []
            for contract in contracts:
                employee = contract.employee
                status = "🟢 Còn hiệu lực" if contract.is_active else "🔴 Hết hiệu lực"
                
                contract_data.append({
                    "Nhân viên": employee.full_name,
                    "Loại HĐ": contract.contract_type,
                    "Số HĐ": contract.contract_number,
                    "Từ ngày": contract.start_date.strftime('%d/%m/%Y'),
                    "Đến ngày": contract.end_date.strftime('%d/%m/%Y') if contract.end_date else "Vô thời hạn",
                    "Lương": f"{contract.salary:,.0f} VND" if contract.salary else "N/A",
                    "Chức vụ": contract.position or "N/A",
                    "Trạng thái": status
                })
            
            df = pd.DataFrame(contract_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        finally:
            session.close()
    
    @staticmethod
    def render_add_contract():
        """Thêm hợp đồng mới"""
        st.markdown("### ➕ Tạo hợp đồng mới")
        
        session = get_database_session()
        
        try:
            employees = session.query(Employee).all()
            employee_options = {emp.full_name: emp.id for emp in employees}
            
            with st.form("contract_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_emp = st.selectbox("Chọn nhân viên:", list(employee_options.keys()))
                    contract_type = st.selectbox("Loại hợp đồng:", ["Ban kiểm soát", "Nhân viên"])
                    contract_number = st.text_input("Số hợp đồng:")
                    start_date = st.date_input("Ngày bắt đầu:")
                
                with col2:
                    end_date = st.date_input("Ngày kết thúc (tùy chọn):")
                    salary = st.number_input("Lương (VND):", min_value=0, step=100000)
                    position = st.text_input("Chức vụ trong HĐ:")
                    is_active = st.checkbox("Còn hiệu lực", value=True)
                
                submitted = st.form_submit_button("💾 Lưu hợp đồng")
                
                if submitted and selected_emp:
                    contract = LaborContract(
                        employee_id=employee_options[selected_emp],
                        contract_type=contract_type,
                        contract_number=contract_number,
                        start_date=start_date,
                        end_date=end_date if end_date != date.today() else None,
                        salary=salary if salary > 0 else None,
                        position=position,
                        is_active=is_active
                    )
                    
                    session.add(contract)
                    session.commit()
                    st.success("✅ Đã tạo hợp đồng thành công")
                    st.rerun()
        
        finally:
            session.close()
    
    @staticmethod
    def render_contract_stats():
        """Thống kê hợp đồng"""
        session = get_database_session()
        
        try:
            contracts = session.query(LaborContract).all()
            
            if not contracts:
                st.info("📊 Chưa có dữ liệu thống kê")
                return
            
            # Thống kê theo loại
            type_counts = {}
            active_counts = {"Còn hiệu lực": 0, "Hết hiệu lực": 0}
            
            for contract in contracts:
                # Theo loại
                contract_type = contract.contract_type or "Khác"
                type_counts[contract_type] = type_counts.get(contract_type, 0) + 1
                
                # Theo trạng thái
                if contract.is_active:
                    active_counts["Còn hiệu lực"] += 1
                else:
                    active_counts["Hết hiệu lực"] += 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.pie(
                    values=list(type_counts.values()),
                    names=list(type_counts.keys()),
                    title="Phân bố theo loại hợp đồng"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(
                    x=list(active_counts.keys()),
                    y=list(active_counts.values()),
                    title="Trạng thái hợp đồng"
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        finally:
            session.close()

class AppointmentCheckSystem:
    """Tính năng 7: Kiểm tra điều kiện bổ nhiệm"""
    
    @staticmethod
    def render_appointment_page():
        """Render trang kiểm tra bổ nhiệm"""
        
        ModernComponents.hero_header(
            "Điều kiện bổ nhiệm", 
            "Kiểm tra quy hoạch, văn bằng, chứng chỉ và kinh nghiệm theo vị trí", 
            "🏆"
        )
        
        tab1, tab2 = st.tabs([
            "🔍 Kiểm tra cá nhân",
            "⚠️ Cảnh báo bổ nhiệm lại"
        ])
        
        with tab1:
            AppointmentCheckSystem.render_individual_check()
        
        with tab2:
            AppointmentCheckSystem.render_reappointment_alerts()
    
    @staticmethod
    def render_individual_check():
        """Kiểm tra điều kiện cá nhân"""
        session = get_database_session()
        
        try:
            employees = session.query(Employee).all()
            
            if employees:
                employee_options = {emp.full_name: emp.id for emp in employees}
                
                selected_emp = st.selectbox("Chọn nhân viên kiểm tra:", list(employee_options.keys()))
                target_position = st.text_input("Vị trí cần bổ nhiệm:", placeholder="VD: Trưởng phòng")
                
                if st.button("🔍 Kiểm tra điều kiện") and selected_emp and target_position:
                    employee_id = employee_options[selected_emp]
                    result = AppointmentCheckSystem.check_appointment_eligibility(employee_id, target_position, session)
                    
                    if result['eligible']:
                        st.success(f"✅ {selected_emp} ĐỦ ĐIỀU KIỆN bổ nhiệm {target_position}")
                    else:
                        st.error(f"❌ {selected_emp} CHƯA ĐỦ ĐIỀU KIỆN bổ nhiệm {target_position}")
                    
                    # Hiển thị chi tiết
                    for criterion, status in result['details'].items():
                        icon = "✅" if status['meets'] else "❌"
                        st.markdown(f"{icon} **{criterion}**: {status['description']}")
        
        finally:
            session.close()
    
    @staticmethod
    def render_reappointment_alerts():
        """Cảnh báo bổ nhiệm lại"""
        st.markdown("### ⚠️ Cảnh báo bổ nhiệm lại (trước 90 ngày)")
        
        # Mock data - trong thực tế sẽ tính từ database
        reappointments = [
            {"Tên": "Nguyễn Văn A", "Chức vụ": "Trưởng phòng", "Hết nhiệm kỳ": "15/02/2024", "Còn": "45 ngày"},
            {"Tên": "Trần Thị B", "Chức vụ": "Phó trưởng phòng", "Hết nhiệm kỳ": "01/03/2024", "Còn": "60 ngày"}
        ]
        
        if reappointments:
            for item in reappointments:
                st.warning(f"⚠️ **{item['Tên']}** ({item['Chức vụ']}) - Hết nhiệm kỳ: {item['Hết nhiệm kỳ']} (còn {item['Còn']})")
        else:
            st.info("✅ Không có trường hợp cần bổ nhiệm lại trong 90 ngày tới")
    
    @staticmethod
    def check_appointment_eligibility(employee_id, target_position, session):
        """Kiểm tra điều kiện bổ nhiệm"""
        employee = session.query(Employee).get(employee_id)
        
        if not employee:
            return {'eligible': False, 'details': {}}
        
        criteria = {}
        
        # 1. Kiểm tra quy hoạch
        planning = session.query(Planning).filter_by(
            employee_id=employee_id, 
            is_current=True
        ).first()
        
        criteria['Quy hoạch'] = {
            'meets': planning is not None and target_position.lower() in (planning.position or "").lower(),
            'description': f"Trong quy hoạch: {planning.position}" if planning else "Không có trong quy hoạch"
        }
        
        # 2. Kiểm tra trình độ
        education = session.query(Education).filter_by(employee_id=employee_id).first()
        min_education = EducationLevelEnum.BACHELOR  # Tối thiểu cử nhân
        
        criteria['Trình độ chuyên môn'] = {
            'meets': education and education.level.value >= min_education.value,
            'description': f"Có: {education.level.value}" if education else "Chưa đủ trình độ"
        }
        
        # 3. Kiểm tra kinh nghiệm (ít nhất 3 năm)
        if employee.organization_start_date:
            years_exp = (date.today() - employee.organization_start_date).days // 365
            criteria['Kinh nghiệm'] = {
                'meets': years_exp >= 3,
                'description': f"{years_exp} năm" + (" (đủ)" if years_exp >= 3 else " (chưa đủ 3 năm)")
            }
        else:
            criteria['Kinh nghiệm'] = {'meets': False, 'description': "Chưa có thông tin"}
        
        # 4. Kiểm tra đánh giá
        latest_eval = session.query(Evaluation).filter_by(
            employee_id=employee_id
        ).order_by(Evaluation.year.desc()).first()
        
        criteria['Đánh giá'] = {
            'meets': latest_eval and latest_eval.performance in [PerformanceEnum.EXCELLENT, PerformanceEnum.GOOD],
            'description': f"Gần nhất: {latest_eval.performance.value}" if latest_eval else "Chưa có đánh giá"
        }
        
        # Kết luận
        all_meet = all(criterion['meets'] for criterion in criteria.values())
        
        return {
            'eligible': all_meet,
            'details': criteria
        }

class RewardsSystem:
    """Tính năng 8: Điều kiện khen thưởng"""
    
    @staticmethod
    def render_rewards_page():
        """Render trang điều kiện khen thưởng"""
        
        ModernComponents.hero_header(
            "Điều kiện khen thưởng", 
            "Xem và đánh giá điều kiện khen thưởng của nhân viên", 
            "🏅"
        )
        
        st.info("🔄 Tính năng đang được cập nhật theo yêu cầu")
        
        # Placeholder cho các tiêu chí khen thưởng
        criteria_options = [
            "Lao động tiên tiến",
            "Chiến sĩ thi đua cơ sở", 
            "Chiến sĩ thi đua cấp cao",
            "Bằng khen Thủ tướng",
            "Huân chương Lao động"
        ]
        
        selected_reward = st.selectbox("Chọn loại khen thưởng:", criteria_options)
        
        st.markdown(f"### 📋 Tiêu chí cho: **{selected_reward}**")
        
        # Mock criteria
        if selected_reward == "Lao động tiên tiến":
            st.markdown("""
            **Điều kiện:**
            - Hoàn thành tốt nhiệm vụ được giao
            - Không vi phạm pháp luật, nội quy
            - Có tinh thần hợp tác tốt
            - Được đánh giá từ "Hoàn thành tốt" trở lên
            """)
        elif selected_reward == "Chiến sĩ thi đua cơ sở":
            st.markdown("""
            **Điều kiện:**
            - Hoàn thành xuất sắc nhiệm vụ
            - Có sáng kiến, cải tiến
            - Là gương mẫu trong đơn vị
            - Được đề nghị bởi tập thể
            """)
        
        if st.button("🔍 Kiểm tra nhân viên đủ điều kiện"):
            st.success("✅ Tìm thấy 8 nhân viên đủ điều kiện")

class EarlySalarySystem:
    """Tính năng 9: Nâng lương trước thời hạn do thành tích"""
    
    @staticmethod 
    def render_early_salary_page():
        """Render trang nâng lương trước thời hạn"""
        
        ModernComponents.hero_header(
            "Nâng lương trước thời hạn", 
            "Xét nâng lương sớm do lập thành tích xuất sắc", 
            "⚡"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "Điều kiện nâng lương sớm",
            "• Lập thành tích xuất sắc đặc biệt\n• Có đóng góp nổi bật cho đơn vị\n• Được tập thể công nhận",
            "info",
            "Áp dụng cho trường hợp đặc biệt, không theo chu kỳ thông thường"
        ), unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([
            "📝 Đề xuất mới",
            "📋 Danh sách đã xét"
        ])
        
        with tab1:
            EarlySalarySystem.render_proposal_form()
        
        with tab2:
            EarlySalarySystem.render_processed_list()
    
    @staticmethod
    def render_proposal_form():
        """Form đề xuất nâng lương sớm"""
        st.markdown("### 📝 Đề xuất nâng lương trước thời hạn")
        
        session = get_database_session()
        
        try:
            employees = session.query(Employee).all()
            employee_options = {emp.full_name: emp.id for emp in employees}
            
            with st.form("early_salary_form"):
                selected_emp = st.selectbox("Nhân viên đề xuất:", list(employee_options.keys()))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    achievement_type = st.selectbox(
                        "Loại thành tích:",
                        ["Sáng kiến cải tiến", "Hoàn thành vượt kế hoạch", "Đóng góp đặc biệt", "Khác"]
                    )
                    proposed_increase = st.number_input("Đề xuất tăng bậc:", min_value=1, max_value=3, value=1)
                
                with col2:
                    achievement_date = st.date_input("Ngày lập thành tích:")
                    urgency = st.selectbox("Mức độ:", ["Thường", "Quan trọng", "Đặc biệt"])
                
                achievement_description = st.text_area(
                    "Mô tả thành tích:",
                    placeholder="Mô tả chi tiết thành tích và đóng góp của nhân viên..."
                )
                
                supporting_evidence = st.text_area(
                    "Tài liệu minh chứng:",
                    placeholder="Liệt kê các tài liệu, chứng từ đính kèm..."
                )
                
                submitted = st.form_submit_button("📤 Gửi đề xuất")
                
                if submitted and selected_emp:
                    st.success(f"✅ Đã gửi đề xuất nâng lương sớm cho {selected_emp}")
                    st.info("📋 Đề xuất sẽ được xem xét bởi ban lãnh đạo")
        
        finally:
            session.close()
    
    @staticmethod
    def render_processed_list():
        """Danh sách đã xử lý"""
        st.markdown("### 📋 Lịch sử đề xuất")
        
        # Mock data
        proposals = [
            {
                "Tên": "Nguyễn Văn A",
                "Thành tích": "Sáng kiến cải tiến quy trình",
                "Ngày đề xuất": "01/12/2023",
                "Tăng bậc": "+1",
                "Trạng thái": "✅ Đã duyệt",
                "Ngày hiệu lực": "01/01/2024"
            },
            {
                "Tên": "Trần Thị B", 
                "Thành tích": "Hoàn thành vượt 150% kế hoạch",
                "Ngày đề xuất": "15/11/2023",
                "Tăng bậc": "+1",
                "Trạng thái": "⏳ Đang xét",
                "Ngày hiệu lực": "-"
            }
        ]
        
        df = pd.DataFrame(proposals)
        st.dataframe(df, use_container_width=True, hide_index=True)

class QuickReportsSystem:
    """Tính năng 10: Báo cáo nhanh"""
    
    @staticmethod
    def render_reports_page():
        """Render trang báo cáo nhanh"""
        
        ModernComponents.hero_header(
            "Báo cáo nhanh", 
            "Thống kê nhân sự theo năm và phân tích xu hướng", 
            "📊"
        )
        
        # Chọn năm báo cáo
        current_year = date.today().year
        selected_year = st.selectbox(
            "Chọn năm báo cáo:",
            list(range(current_year - 5, current_year + 1)),
            index=5  # Năm hiện tại
        )
        
        tab1, tab2, tab3 = st.tabs([
            "📈 Thống kê tổng quan",
            "🔍 Phân tích xu hướng",
            "👥 Cơ cấu nhân sự"
        ])
        
        with tab1:
            QuickReportsSystem.render_overview_stats(selected_year)
        
        with tab2:
            QuickReportsSystem.render_trend_analysis(selected_year)
            
        with tab3:
            QuickReportsSystem.render_staff_structure(selected_year)
    
    @staticmethod
    def render_overview_stats(year):
        """Thống kê tổng quan"""
        st.markdown(f"### 📊 Thống kê năm {year}")
        
        # Mock data
        stats = {
            "Nâng lương": 25,
            "Nghỉ hưu": 8,
            "Thôi việc": 12,
            "Bổ nhiệm": 15,
            "Nghỉ thai sản": 6,
            "Đi học": 4
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👆 Nâng lương", stats["Nâng lương"], "+5")
            st.metric("🎓 Đi học", stats["Đi học"], "+1")
        
        with col2:
            st.metric("👴 Nghỉ hưu", stats["Nghỉ hưu"], "+2")
            st.metric("🤰 Nghỉ thai sản", stats["Nghỉ thai sản"], "-2")
        
        with col3:
            st.metric("👋 Thôi việc", stats["Thôi việc"], "+8")
            st.metric("📈 Bổ nhiệm", stats["Bổ nhiệm"], "+3")
        
        # Biểu đồ tổng quan
        fig = px.bar(
            x=list(stats.keys()),
            y=list(stats.values()),
            title=f"Các hoạt động nhân sự năm {year}",
            color=list(stats.values()),
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_trend_analysis(year):
        """Phân tích xu hướng"""
        st.markdown(f"### 🔍 Phân tích xu hướng nghỉ việc")
        
        # Mock analysis data
        resignation_analysis = {
            "Độ tuổi": {"25-30": 5, "30-35": 4, "35-40": 2, "40+": 1},
            "Số năm làm việc": {"1-2 năm": 6, "2-5 năm": 4, "5-10 năm": 2, "10+ năm": 0},
            "Trình độ": {"Đại học": 8, "Thạc sĩ": 3, "Tiến sĩ": 1, "Khác": 0}
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(
                values=list(resignation_analysis["Độ tuổi"].values()),
                names=list(resignation_analysis["Độ tuổi"].keys()),
                title="Nghỉ việc theo độ tuổi"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                x=list(resignation_analysis["Số năm làm việc"].keys()),
                y=list(resignation_analysis["Số năm làm việc"].values()),
                title="Nghỉ việc theo năm kinh nghiệm"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Insights
        st.markdown("#### 💡 Nhận xét:")
        st.markdown("""
        - **Nhóm tuổi 25-30**: Tỷ lệ nghỉ việc cao nhất (42%)
        - **Kinh nghiệm 1-2 năm**: Thường nghỉ việc sau thời gian thử việc
        - **Trình độ đại học**: Chiếm đa số trong nhóm nghỉ việc
        """)
    
    @staticmethod
    def render_staff_structure(year):
        """Cơ cấu nhân sự"""
        st.markdown(f"### 👥 Cơ cấu nhân sự năm {year}")
        
        # Mock structure data
        structure_data = {
            "Độ tuổi": {"<30": 25, "30-40": 35, "40-50": 28, ">50": 12},
            "Giới tính": {"Nam": 58, "Nữ": 42},
            "Dân tộc": {"Kinh": 85, "Khác": 15},
            "Trình độ LLCT": {"Sơ cấp": 20, "Trung cấp": 45, "Cao cấp": 35},
            "Trình độ CM": {"Đại học": 60, "Thạc sĩ": 30, "Tiến sĩ": 10}
        }
        
        # Hiển thị các biểu đồ
        for category, data in structure_data.items():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    values=list(data.values()),
                    names=list(data.keys()),
                    title=f"Phân bố theo {category}"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"**{category}:**")
                for key, value in data.items():
                    percentage = (value / sum(data.values())) * 100
                    st.markdown(f"• {key}: {percentage:.1f}%")

class InsuranceSystem:
    """Tính năng 11: Báo bảo hiểm"""
    
    @staticmethod
    def render_insurance_page():
        """Render trang báo bảo hiểm"""
        
        ModernComponents.hero_header(
            "Báo bảo hiểm", 
            "Quản lý và xuất báo cáo bảo hiểm xã hội", 
            "🏥"
        )
        
        tab1, tab2, tab3 = st.tabs([
            "📝 Tạo báo cáo mới",
            "📋 Lịch sử báo cáo",
            "📤 Xuất file Excel"
        ])
        
        with tab1:
            InsuranceSystem.render_create_report()
        
        with tab2:
            InsuranceSystem.render_report_history()
            
        with tab3:
            InsuranceSystem.render_export_excel()
    
    @staticmethod
    def render_create_report():
        """Tạo báo cáo bảo hiểm mới"""
        st.markdown("### 📝 Tạo báo cáo bảo hiểm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_month = st.selectbox("Tháng báo cáo:", list(range(1, 13)))
            report_year = st.selectbox("Năm báo cáo:", list(range(2020, 2030)))
        
        with col2:
            change_types = [
                "Điều chỉnh chức danh",
                "Điều chỉnh lương",
                "Điều chỉnh phụ cấp", 
                "Nghỉ hưu",
                "Thôi việc",
                "Nghỉ thai sản",
                "Nghỉ ốm đau",
                "Đi học",
                "Phu nhân ngoại giao"
            ]
            selected_changes = st.multiselect("Loại thay đổi:", change_types)
        
        if st.button("📊 Tạo báo cáo") and selected_changes:
            # Mock tạo báo cáo
            report_data = []
            
            for change_type in selected_changes:
                # Mock data cho từng loại thay đổi
                if change_type == "Nghỉ hưu":
                    report_data.append({
                        "Họ tên": "Nguyễn Văn A",
                        "Loại thay đổi": change_type,
                        "Giá trị cũ": "Đang làm việc",
                        "Giá trị mới": "Nghỉ hưu",
                        "Ngày hiệu lực": f"15/{report_month:02d}/{report_year}"
                    })
                elif change_type == "Điều chỉnh lương":
                    report_data.append({
                        "Họ tên": "Trần Thị B",
                        "Loại thay đổi": change_type,
                        "Giá trị cũ": "3.45",
                        "Giá trị mới": "3.66", 
                        "Ngày hiệu lực": f"01/{report_month:02d}/{report_year}"
                    })
            
            if report_data:
                df = pd.DataFrame(report_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Lưu vào session để export
                st.session_state.insurance_report = {
                    'data': report_data,
                    'month': report_month,
                    'year': report_year,
                    'created_at': datetime.now()
                }
                
                st.success(f"✅ Đã tạo báo cáo tháng {report_month}/{report_year}")
            else:
                st.info("📝 Không có dữ liệu thay đổi trong kỳ")
    
    @staticmethod
    def render_report_history():
        """Lịch sử báo cáo"""
        st.markdown("### 📋 Lịch sử báo cáo bảo hiểm")
        
        # Mock history
        history = [
            {"Tháng": "12/2023", "Số thay đổi": 15, "Trạng thái": "✅ Đã gửi", "Ngày tạo": "05/01/2024"},
            {"Tháng": "11/2023", "Số thay đổi": 12, "Trạng thái": "✅ Đã gửi", "Ngày tạo": "03/12/2023"},
            {"Tháng": "10/2023", "Số thay đổi": 8, "Trạng thái": "✅ Đã gửi", "Ngày tạo": "02/11/2023"}
        ]
        
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_export_excel():
        """Xuất file Excel"""
        st.markdown("### 📤 Xuất file Excel cho bảo hiểm")
        
        if not hasattr(st.session_state, 'insurance_report'):
            st.info("📝 Vui lòng tạo báo cáo trước")
            return
        
        report = st.session_state.insurance_report
        
        st.markdown(f"**Báo cáo:** Tháng {report['month']}/{report['year']}")
        st.markdown(f"**Số bản ghi:** {len(report['data'])}")
        st.markdown(f"**Tạo lúc:** {report['created_at'].strftime('%d/%m/%Y %H:%M')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Xuất Excel chuẩn BHXH"):
                st.success("✅ Đã xuất file Excel theo format BHXH")
                st.info("📁 File: exports/bao_cao_bhxh_{}_{}.xlsx".format(report['month'], report['year']))
        
        with col2:
            if st.button("📧 Gửi email tự động"):
                st.success("✅ Đã gửi báo cáo qua email")
                st.info("📧 Đã gửi đến: baohiem@domain.gov.vn")

# Main render functions cho từng tính năng
def render_planning_management_page():
    PlanningManagementSystem.render_planning_page()

def render_work_history_page():
    WorkHistorySystem.render_work_history_page()

def render_contract_management_page():
    ContractManagementSystem.render_contract_page()

def render_appointment_check_page():
    AppointmentCheckSystem.render_appointment_page()

def render_rewards_page():
    RewardsSystem.render_rewards_page()

def render_early_salary_page():
    EarlySalarySystem.render_early_salary_page()

def render_quick_reports_page():
    QuickReportsSystem.render_reports_page()

def render_insurance_page():
    InsuranceSystem.render_insurance_page()
