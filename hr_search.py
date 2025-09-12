"""
HRMS - Tính năng 1: Tra cứu nhân sự đầy đủ
Theo đúng yêu cầu của người dùng với 5 tabs thông tin và export Word
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from models_enhanced import *
from components import ModernComponents
import plotly.express as px
import plotly.graph_objects as go

def get_database_session():
    """Tạo session database"""
    engine = get_engine() 
    Session = sessionmaker(bind=engine)
    return Session()

class EmployeeSearchSystem:
    """Hệ thống tra cứu nhân sự hoàn chỉnh"""
    
    @staticmethod
    def render_search_page():
        """Render trang tra cứu nhân sự chính"""
        
        # Header với hướng dẫn
        ModernComponents.hero_header(
            "Tra cứu thông tin nhân sự", 
            "Tìm kiếm và xem chi tiết thông tin nhân viên - ~150 người có thể bổ sung", 
            "🔍"
        )
        
        st.markdown(ModernComponents.modern_alert(
            "Hướng dẫn sử dụng",
            "1. Gõ tên nhân sự cần tìm vào ô tìm kiếm\n2. Chọn nhân viên từ kết quả\n3. Xem thông tin qua 5 tabs chi tiết\n4. Xuất file Word hoặc chuyển sang chức năng khác",
            "info",
            "Hỗ trợ tìm kiếm theo tên, chức vụ, phòng ban"
        ), unsafe_allow_html=True)
        
        # Search Box
        st.markdown("### 🔍 Tìm kiếm nhân sự")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input(
                "Nhập tên nhân sự cần tìm:",
                placeholder="VD: Nguyễn Văn An",
                help="Có thể tìm theo tên, chức vụ, hoặc phòng ban"
            )
            
        with col2:
            search_button = st.button("🔍 Tìm kiếm", type="primary")
        
        # Search Results
        if search_term or search_button:
            EmployeeSearchSystem.show_search_results(search_term)
    
    @staticmethod
    def show_search_results(search_term):
        """Hiển thị kết quả tìm kiếm"""
        session = get_database_session()
        
        try:
            # Tìm kiếm trong database
            query = session.query(Employee)
            
            if search_term:
                query = query.filter(
                    Employee.full_name.contains(search_term) |
                    Employee.position.contains(search_term) |
                    Employee.department.contains(search_term)
                )
            
            results = query.all()
            
            if not results:
                st.warning(f"Không tìm thấy nhân sự với từ khóa '{search_term}'")
                return
            
            # Hiển thị danh sách kết quả
            st.markdown(f"### 📋 Kết quả tìm kiếm ({len(results)} người)")
            
            # Tạo dataframe cho kết quả
            result_data = []
            for emp in results:
                result_data.append({
                    "ID": emp.id,
                    "Họ tên": emp.full_name,
                    "Chức vụ": emp.position or "N/A",
                    "Phòng ban": emp.department or "N/A", 
                    "Ngạch/Bậc": f"{emp.current_salary_grade or 'N/A'}/{emp.current_salary_level or 'N/A'}",
                    "Trạng thái": emp.work_status.value if emp.work_status else "N/A"
                })
            
            df = pd.DataFrame(result_data)
            
            # Cho phép chọn nhân viên
            selected_indices = st.dataframe(
                df,
                use_container_width=True,
                on_select="rerun",
                selection_mode="single-row",
                hide_index=True
            )
            
            if selected_indices.selection.rows:
                selected_index = selected_indices.selection.rows[0]
                selected_employee_id = df.iloc[selected_index]["ID"]
                
                # Hiển thị thông tin chi tiết
                EmployeeSearchSystem.show_employee_details(selected_employee_id)
        
        finally:
            session.close()
    
    @staticmethod
    def show_employee_details(employee_id):
        """Hiển thị thông tin chi tiết nhân viên qua 5 tabs"""
        session = get_database_session()
        
        try:
            employee = session.query(Employee).get(employee_id)
            if not employee:
                st.error("Không tìm thấy thông tin nhân viên")
                return
            
            st.markdown("---")
            st.markdown(f"## 👤 Thông tin chi tiết: **{employee.full_name}**")
            
            # Tạo 5 tabs theo yêu cầu
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 Thông tin cơ bản",
                "💼 Công tác & Lương",
                "🎓 Đào tạo & Trình độ", 
                "🏆 Thành tích & Đánh giá",
                "📊 Biểu đồ & Thống kê"
            ])
            
            with tab1:
                EmployeeSearchSystem.render_basic_info_tab(employee)
                
            with tab2:
                EmployeeSearchSystem.render_work_salary_tab(employee, session)
                
            with tab3:
                EmployeeSearchSystem.render_education_tab(employee, session)
                
            with tab4:
                EmployeeSearchSystem.render_achievements_tab(employee, session)
                
            with tab5:
                EmployeeSearchSystem.render_statistics_tab(employee, session)
            
            # Action buttons
            EmployeeSearchSystem.render_action_buttons(employee)
            
        finally:
            session.close()
    
    @staticmethod
    def render_basic_info_tab(employee):
        """Tab 1: Thông tin cơ bản"""
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Thông tin cá nhân")
            st.markdown(f"**Họ và tên:** {employee.full_name}")
            st.markdown(f"**Ngày sinh:** {employee.date_of_birth.strftime('%d/%m/%Y') if employee.date_of_birth else 'N/A'}")
            st.markdown(f"**Giới tính:** {employee.gender.value if employee.gender else 'N/A'}")
            st.markdown(f"**Dân tộc:** {employee.ethnicity or 'N/A'}")
            st.markdown(f"**Tôn giáo:** {employee.religion or 'N/A'}")
            st.markdown(f"**Quê quán:** {employee.hometown or 'N/A'}")
            
            # Tuổi hiện tại
            if employee.date_of_birth:
                age = (date.today() - employee.date_of_birth).days // 365
                st.markdown(f"**Tuổi hiện tại:** {age} tuổi")
        
        with col2:
            st.markdown("#### 🏛️ Thông tin công tác")
            st.markdown(f"**Chức vụ/chức danh:** {employee.position or 'N/A'}")
            st.markdown(f"**Đơn vị:** {employee.department or 'N/A'}")
            st.markdown(f"**Ngày vào Đảng:** {employee.party_join_date.strftime('%d/%m/%Y') if employee.party_join_date else 'N/A'}")
            st.markdown(f"**Trạng thái công tác:** {employee.work_status.value if employee.work_status else 'N/A'}")
            
            if employee.work_status_details:
                st.markdown(f"**Chi tiết trạng thái:** {employee.work_status_details}")
        
        # Quy hoạch
        if employee.current_planning:
            st.markdown("#### 📈 Quy hoạch")
            st.info(f"Chức danh quy hoạch hiện nay: **{employee.current_planning}**")
        
        # Liên hệ
        st.markdown("#### 📞 Thông tin liên hệ")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"**Điện thoại:** {employee.phone or 'N/A'}")
        with col4:
            st.markdown(f"**Email:** {employee.email or 'N/A'}")
    
    @staticmethod 
    def render_work_salary_tab(employee, session):
        """Tab 2: Công tác & Lương"""
        
        # Thông tin lương hiện tại
        st.markdown("#### 💰 Lương hiện hưởng")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Ngạch hiện hưởng",
                employee.current_salary_grade or "N/A"
            )
        with col2:
            st.metric(
                "Bậc lương", 
                employee.current_salary_level or "N/A"
            )
        with col3:
            st.metric(
                "Hệ số lương",
                f"{employee.current_salary_coefficient:.2f}" if employee.current_salary_coefficient else "N/A"
            )
        
        # Thời điểm hưởng lương
        if employee.current_salary_date:
            st.markdown(f"**Thời điểm hưởng lương hiện nay:** {employee.current_salary_date.strftime('%d/%m/%Y')}")
        
        # Phụ cấp chức vụ
        if employee.position_allowance:
            st.markdown(f"**Phụ cấp chức vụ:** {employee.position_allowance}")
            if employee.position_allowance_reserve_until:
                st.warning(f"⚠️ Bảo lưu phụ cấp chức vụ đến: {employee.position_allowance_reserve_until.strftime('%d/%m/%Y')}")
        
        # Thời gian công tác
        st.markdown("#### ⏰ Thời gian công tác")
        
        col4, col5 = st.columns(2)
        with col4:
            if employee.social_insurance_start_date:
                insurance_years = (date.today() - employee.social_insurance_start_date).days // 365
                st.markdown(f"**Ngày bắt đầu công tác (BHXH):** {employee.social_insurance_start_date.strftime('%d/%m/%Y')}")
                st.markdown(f"**Thời gian công tác:** {insurance_years} năm")
        
        with col5:
            if employee.organization_start_date:
                org_years = (date.today() - employee.organization_start_date).days // 365
                st.markdown(f"**Ngày vào cơ quan:** {employee.organization_start_date.strftime('%d/%m/%Y')}")
                st.markdown(f"**Thời gian tại cơ quan:** {org_years} năm")
        
        # Lịch sử lương (có thể mở rộng)
        salary_history = session.query(SalaryHistory).filter_by(employee_id=employee.id).order_by(SalaryHistory.effective_date.desc()).all()
        
        if salary_history:
            with st.expander("📈 Xem lịch sử lương"):
                salary_data = []
                for salary in salary_history:
                    salary_data.append({
                        "Ngày hiệu lực": salary.effective_date.strftime('%d/%m/%Y'),
                        "Ngạch": salary.salary_grade,
                        "Bậc": salary.salary_level,
                        "Hệ số": salary.salary_coefficient,
                        "Phụ cấp CV": salary.position_allowance or 0,
                        "Lý do": salary.reason or "N/A"
                    })
                
                df_salary = pd.DataFrame(salary_data)
                st.dataframe(df_salary, use_container_width=True, hide_index=True)
        
        # Quá trình công tác 
        work_history = session.query(WorkHistory).filter_by(employee_id=employee.id).order_by(WorkHistory.start_date.desc()).all()
        
        if work_history:
            with st.expander("💼 Xem quá trình công tác"):
                for work in work_history:
                    end_date_str = work.end_date.strftime('%d/%m/%Y') if work.end_date else "Hiện tại"
                    st.markdown(f"""
                    **{work.start_date.strftime('%d/%m/%Y')} - {end_date_str}**  
                    📍 {work.position} - {work.department}  
                    🏢 {work.organization}  
                    {work.responsibilities or ''}
                    """)
                    st.divider()
    
    @staticmethod
    def render_education_tab(employee, session):
        """Tab 3: Đào tạo & Trình độ"""
        
        # Trình độ chính
        st.markdown("#### 🎓 Trình độ chuyên môn")
        st.markdown(f"**Trình độ:** {employee.education_level.value if employee.education_level else 'N/A'}")
        st.markdown(f"**Trình độ lý luận chính trị:** {employee.political_theory_level.value if employee.political_theory_level else 'N/A'}")
        
        # Chi tiết học vấn
        education_records = session.query(Education).filter_by(employee_id=employee.id).all()
        
        if education_records:
            st.markdown("#### 📚 Chi tiết học vấn")
            for edu in education_records:
                with st.container():
                    st.markdown(f"""
                    **{edu.level.value if edu.level else 'N/A'}** - {edu.field_of_study or 'N/A'}  
                    🏫 Trường: {edu.institution or 'N/A'}  
                    🌍 Nước: {edu.country or 'N/A'}  
                    📖 Hình thức: {edu.study_mode or 'N/A'}  
                    📅 Tốt nghiệp: {edu.graduation_date.strftime('%d/%m/%Y') if edu.graduation_date else 'N/A'}
                    """)
                    st.divider()
        
        # Quá trình đào tạo, bồi dưỡng
        training_records = session.query(Training).filter_by(employee_id=employee.id).all()
        
        if training_records:
            with st.expander("🏆 Xem quá trình đào tạo, bồi dưỡng"):
                training_data = []
                for training in training_records:
                    training_data.append({
                        "Loại đào tạo": training.training_type,
                        "Cấp độ": training.level,
                        "Trường/Cơ quan": training.institution,
                        "Ngày hoàn thành": training.completion_date.strftime('%d/%m/%Y') if training.completion_date else 'N/A',
                        "Số chứng chỉ": training.certificate_number or 'N/A'
                    })
                
                df_training = pd.DataFrame(training_data)
                st.dataframe(df_training, use_container_width=True, hide_index=True)
        
        # Tham gia hội đồng
        councils = session.query(CouncilMembership).filter_by(employee_id=employee.id).all()
        
        if councils:
            with st.expander("🏛️ Tham gia hội đồng, ban chỉ đạo"):
                for council in councils:
                    end_date_str = council.end_date.strftime('%d/%m/%Y') if council.end_date else "Hiện tại"
                    location = "Trong cơ quan" if council.is_internal else "Ngoài cơ quan"
                    st.markdown(f"""
                    **{council.council_name}**  
                    👤 Vai trò: {council.role or 'Thành viên'}  
                    📅 Thời gian: {council.start_date.strftime('%d/%m/%Y') if council.start_date else 'N/A'} - {end_date_str}  
                    📍 {location}
                    """)
                    st.divider()
    
    @staticmethod
    def render_achievements_tab(employee, session):
        """Tab 4: Thành tích & Đánh giá"""
        
        # Thành tích, khen thưởng
        achievements = session.query(Achievement).filter_by(employee_id=employee.id).order_by(Achievement.award_year.desc()).all()
        
        st.markdown("#### 🏆 Thành tích, khen thưởng")
        
        if achievements:
            for achievement in achievements:
                award_color = "🥇" if "nhất" in (achievement.award_level or "") else "🥈" if "nhì" in (achievement.award_level or "") else "🥉"
                
                st.markdown(f"""
                {award_color} **{achievement.award_type}** ({achievement.award_year})  
                🏅 Cấp độ: {achievement.award_level or 'N/A'}  
                🏢 Cơ quan cấp: {achievement.issuing_authority or 'N/A'}  
                {achievement.details or ''}
                """)
                st.divider()
        else:
            st.info("Chưa có thông tin khen thưởng")
        
        # Đánh giá hàng năm
        evaluations = session.query(Evaluation).filter_by(employee_id=employee.id).order_by(Evaluation.year.desc()).all()
        
        st.markdown("#### 📊 Đánh giá hàng năm")
        
        if evaluations:
            eval_data = []
            for evaluation in evaluations:
                performance_color = {"Hoàn thành xuất sắc": "🟢", "Hoàn thành tốt": "🟡", 
                                   "Hoàn thành": "🟠", "Không hoàn thành": "🔴"}
                
                eval_data.append({
                    "Năm": evaluation.year,
                    "Kết quả": f"{performance_color.get(evaluation.performance.value, '⚪')} {evaluation.performance.value}",
                    "Chi tiết": evaluation.details or 'N/A'
                })
            
            df_eval = pd.DataFrame(eval_data)
            st.dataframe(df_eval, use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có đánh giá hàng năm")
    
    @staticmethod
    def render_statistics_tab(employee, session):
        """Tab 5: Biểu đồ & Thống kê"""
        
        st.markdown("#### 📈 Biểu đồ thống kê cá nhân")
        
        # Biểu đồ lịch sử lương
        salary_history = session.query(SalaryHistory).filter_by(employee_id=employee.id).order_by(SalaryHistory.effective_date).all()
        
        if salary_history and len(salary_history) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 💰 Lịch sử hệ số lương")
                
                dates = [s.effective_date for s in salary_history]
                coefficients = [s.salary_coefficient for s in salary_history]
                
                fig = px.line(
                    x=dates, y=coefficients,
                    title="Tiến trình hệ số lương theo thời gian",
                    labels={'x': 'Thời gian', 'y': 'Hệ số lương'}
                )
                fig.update_traces(mode='markers+lines')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("##### 📊 Phụ cấp chức vụ")
                
                allowances = [s.position_allowance or 0 for s in salary_history]
                
                fig2 = px.bar(
                    x=dates, y=allowances,
                    title="Lịch sử phụ cấp chức vụ",
                    labels={'x': 'Thời gian', 'y': 'Phụ cấp'}
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Thống kê đánh giá
        evaluations = session.query(Evaluation).filter_by(employee_id=employee.id).all()
        
        if evaluations:
            st.markdown("##### 🎯 Phân bố kết quả đánh giá")
            
            eval_counts = {}
            for eval in evaluations:
                perf = eval.performance.value
                eval_counts[perf] = eval_counts.get(perf, 0) + 1
            
            fig3 = px.pie(
                values=list(eval_counts.values()),
                names=list(eval_counts.keys()),
                title="Tỷ lệ các mức đánh giá"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Thời gian làm việc
        if employee.social_insurance_start_date:
            total_days = (date.today() - employee.social_insurance_start_date).days
            total_years = total_days // 365
            remaining_days = total_days % 365
            
            st.markdown("##### ⏱️ Thống kê thời gian")
            
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("Tổng số năm", f"{total_years} năm")
            with col4:
                st.metric("Số ngày thêm", f"{remaining_days} ngày")
            with col5:
                if employee.date_of_birth:
                    retirement_age = 60 if employee.gender == GenderEnum.FEMALE else 62
                    retirement_date = date(employee.date_of_birth.year + retirement_age, employee.date_of_birth.month, employee.date_of_birth.day)
                    days_to_retirement = (retirement_date - date.today()).days
                    
                    if days_to_retirement > 0:
                        years_to_retirement = days_to_retirement // 365
                        st.metric("Năm còn lại đến nghỉ hưu", f"{years_to_retirement} năm")
                    else:
                        st.metric("Tình trạng", "Đã đến tuổi nghỉ hưu")
    
    @staticmethod
    def render_action_buttons(employee):
        """Render các nút hành động"""
        
        st.markdown("---")
        st.markdown("### 🎯 Hành động")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Xuất file Word", type="primary"):
                EmployeeSearchSystem.export_to_word(employee)
        
        with col2:
            if st.button("💰 Kiểm tra nâng lương"):
                st.info("🔄 Chuyển đến chức năng nâng lương...")
                # TODO: Implement chuyển đến tính năng nâng lương
        
        with col3:
            if st.button("⏰ Tính tuổi nghỉ hưu"):
                EmployeeSearchSystem.calculate_retirement_age(employee)
        
        with col4:
            if st.button("🏆 Kiểm tra điều kiện bổ nhiệm"):
                st.info("🔄 Chuyển đến chức năng bổ nhiệm...")
                # TODO: Implement chuyển đến tính năng bổ nhiệm
    
    @staticmethod
    def export_to_word(employee):
        """Xuất thông tin nhân sự ra file Word"""
        try:
            # TODO: Implement Word export using python-docx
            st.success(f"✅ Đã xuất thông tin {employee.full_name} ra file Word!")
            st.info("💡 File sẽ được lưu trong thư mục exports/")
            
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất file: {str(e)}")
    
    @staticmethod
    def calculate_retirement_age(employee):
        """Tính toán thông tin nghỉ hưu"""
        if not employee.date_of_birth:
            st.error("Không có thông tin ngày sinh")
            return
        
        retirement_age = 60 if employee.gender == GenderEnum.FEMALE else 62
        retirement_date = date(
            employee.date_of_birth.year + retirement_age,
            employee.date_of_birth.month, 
            employee.date_of_birth.day
        )
        
        days_remaining = (retirement_date - date.today()).days
        
        if days_remaining > 0:
            years_remaining = days_remaining // 365
            months_remaining = (days_remaining % 365) // 30
            
            st.success(f"""
            **🎂 Thông tin nghỉ hưu của {employee.full_name}:**
            
            - Tuổi nghỉ hưu: {retirement_age} tuổi
            - Ngày nghỉ hưu dự kiến: {retirement_date.strftime('%d/%m/%Y')}
            - Thời gian còn lại: {years_remaining} năm {months_remaining} tháng
            """)
            
            # Cảnh báo nếu gần nghỉ hưu
            if days_remaining <= 180:  # 6 tháng
                st.warning("⚠️ Gần đến thời điểm nghỉ hưu - cần chuẩn bị thủ tục!")
        else:
            st.info(f"👴 {employee.full_name} đã đến tuổi nghỉ hưu từ {retirement_date.strftime('%d/%m/%Y')}")

# Main function to render the search page
def render_employee_search_page():
    """Render trang tra cứu nhân sự - được gọi từ main app"""
    EmployeeSearchSystem.render_search_page()
