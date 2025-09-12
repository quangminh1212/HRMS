"""
Extended Modern Components - Thêm các component nâng cao
Tham khảo từ Chakra UI, Ant Design, Material-UI
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

class AdvancedComponents:
    """Component nâng cao cho HRMS Modern"""
    
    @staticmethod
    def progress_card(title: str, current: int, target: int, icon: str = "📊", color: str = "#6750A4"):
        """Progress card với animation"""
        percentage = (current / target * 100) if target > 0 else 0
        progress_color = color
        
        if percentage >= 90:
            progress_color = "#4CAF50"  # Green
        elif percentage >= 70:
            progress_color = "#FF9800"  # Orange
        elif percentage >= 50:
            progress_color = "#2196F3"  # Blue
        
        return f"""
        <div class="surface-container animate-fade-scale" style="padding: 1.5rem; margin: 0.5rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</div>
                <div class="title-medium" style="color: #1C1B1F; flex: 1;">{title}</div>
                <div class="label-large" style="color: {progress_color};">{percentage:.1f}%</div>
            </div>
            
            <div style="background: #E6E0E9; border-radius: 12px; height: 8px; margin-bottom: 0.75rem; overflow: hidden;">
                <div style="
                    background: linear-gradient(90deg, {progress_color}, {progress_color}AA);
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 12px;
                    transition: width 1s ease-in-out;
                "></div>
            </div>
            
            <div class="body-small" style="color: #49454F; text-align: center;">
                {current} / {target} hoàn thành
            </div>
        </div>
        """
    
    @staticmethod
    def status_timeline(events: list):
        """Timeline component cho trạng thái công việc"""
        timeline_html = """
        <div class="surface-container" style="padding: 1.5rem;">
            <div class="title-large" style="margin-bottom: 1.5rem; color: #1C1B1F;">
                📅 Timeline trạng thái
            </div>
        """
        
        for i, event in enumerate(events):
            is_completed = event.get('status') == 'completed'
            is_current = event.get('status') == 'current'
            is_future = event.get('status') == 'future'
            
            # Icon và màu sắc theo trạng thái
            if is_completed:
                icon = "✅"
                color = "#4CAF50"
                bg_color = "rgba(76, 175, 80, 0.1)"
            elif is_current:
                icon = "⚡"
                color = "#FF9800"
                bg_color = "rgba(255, 152, 0, 0.1)"
            else:
                icon = "⏳"
                color = "#9E9E9E"
                bg_color = "rgba(158, 158, 158, 0.1)"
            
            # Line connector (trừ item cuối)
            line_html = ""
            if i < len(events) - 1:
                line_html = f'<div style="width: 2px; height: 30px; background: {color}; margin: 5px auto;"></div>'
            
            timeline_html += f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
                <div style="
                    width: 40px; height: 40px; border-radius: 20px; 
                    background: {bg_color}; border: 2px solid {color};
                    display: flex; align-items: center; justify-content: center;
                    margin-right: 1rem; flex-shrink: 0;
                ">
                    {icon}
                </div>
                <div style="flex: 1; padding-top: 0.5rem;">
                    <div class="title-small" style="color: #1C1B1F; margin-bottom: 0.25rem;">
                        {event['title']}
                    </div>
                    <div class="body-small" style="color: #49454F; margin-bottom: 0.25rem;">
                        {event['description']}
                    </div>
                    <div class="label-small" style="color: {color};">
                        {event['date']}
                    </div>
                </div>
            </div>
            {line_html}
            """
        
        timeline_html += "</div>"
        return timeline_html
    
    @staticmethod
    def interactive_chart(df: pd.DataFrame, chart_type: str = "bar", title: str = "Biểu đồ"):
        """Biểu đồ tương tác với Plotly"""
        if chart_type == "bar":
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df.iloc[:, 0],
                y=df.iloc[:, 1], 
                marker=dict(
                    color=df.iloc[:, 1],
                    colorscale='Viridis',
                    line=dict(color='rgba(255,255,255,0.6)', width=1)
                ),
                hovertemplate='<b>%{x}</b><br>Số lượng: %{y}<extra></extra>'
            ))
        elif chart_type == "pie":
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=df.iloc[:, 0],
                values=df.iloc[:, 1],
                hole=0.4,
                marker=dict(
                    colors=['#6750A4', '#7F67BE', '#9A82DB', '#D0BCFF'],
                    line=dict(color='#FFFFFF', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(family="Inter", size=18, color="#1C1B1F"),
                x=0.5
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#1C1B1F"),
            margin=dict(t=60, l=20, r=20, b=20),
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def stats_grid(stats: list):
        """Grid thống kê với animation"""
        cols_html = ""
        
        for stat in stats:
            icon = stat.get('icon', '📊')
            title = stat.get('title', 'Tiêu đề')
            value = stat.get('value', '0')
            subtitle = stat.get('subtitle', '')
            trend = stat.get('trend', 'neutral')
            
            # Màu sắc theo trend
            if trend == 'up':
                trend_color = "#4CAF50"
                trend_icon = "📈"
            elif trend == 'down': 
                trend_color = "#F44336"
                trend_icon = "📉"
            else:
                trend_color = "#9E9E9E"
                trend_icon = "➡️"
            
            cols_html += f"""
            <div class="metric-card animate-slide-up" style="margin: 0.5rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="color: {trend_color}; font-size: 1rem;">{trend_icon}</div>
                </div>
                <div class="display-small" style="color: #1C1B1F; margin-bottom: 0.25rem; font-weight: 700;">
                    {value}
                </div>
                <div class="body-medium" style="color: #49454F; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div class="label-small" style="color: #79747E;">
                    {subtitle}
                </div>
            </div>
            """
        
        return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">{cols_html}</div>'
    
    @staticmethod
    def feature_announcement(title: str, description: str, version: str = "NEW", type: str = "feature"):
        """Thông báo tính năng mới"""
        colors = {
            'feature': {'bg': 'rgba(103, 80, 164, 0.1)', 'border': '#6750A4', 'text': '#6750A4'},
            'update': {'bg': 'rgba(76, 175, 80, 0.1)', 'border': '#4CAF50', 'text': '#4CAF50'},
            'info': {'bg': 'rgba(33, 150, 243, 0.1)', 'border': '#2196F3', 'text': '#2196F3'}
        }
        
        color_scheme = colors.get(type, colors['feature'])
        
        return f"""
        <div class="animate-slide-up" style="
            background: {color_scheme['bg']};
            border: 1px solid {color_scheme['border']};
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                right: 0;
                background: {color_scheme['border']};
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 0 16px 0 12px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            ">
                {version}
            </div>
            
            <div style="margin-right: 3rem;">
                <div class="title-medium" style="color: {color_scheme['text']}; margin-bottom: 0.5rem;">
                    ✨ {title}
                </div>
                <div class="body-medium" style="color: #1C1B1F;">
                    {description}
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def quick_actions_panel(actions: list):
        """Panel hành động nhanh"""
        actions_html = ""
        
        for action in actions:
            icon = action.get('icon', '⚡')
            title = action.get('title', 'Hành động')
            desc = action.get('description', '')
            color = action.get('color', '#6750A4')
            
            actions_html += f"""
            <div class="surface-container" style="
                padding: 1rem; margin: 0.5rem; cursor: pointer;
                transition: all 300ms ease;
                border: 1px solid rgba(255, 255, 255, 0.2);
            " onmouseover="this.style.transform='translateY(-4px) scale(1.02)'" 
               onmouseout="this.style.transform='translateY(0) scale(1)'">
                <div style="
                    width: 48px; height: 48px; border-radius: 12px;
                    background: linear-gradient(135deg, {color}, {color}AA);
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-size: 1.25rem;
                    margin-bottom: 0.75rem;
                ">
                    {icon}
                </div>
                <div class="title-small" style="color: #1C1B1F; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div class="body-small" style="color: #49454F;">
                    {desc}
                </div>
            </div>
            """
        
        return f"""
        <div class="surface-container-high" style="padding: 1.5rem;">
            <div class="title-large" style="margin-bottom: 1.5rem; color: #1C1B1F;">
                ⚡ Hành động nhanh
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.5rem;">
                {actions_html}
            </div>
        </div>
        """

def create_demo_dashboard():
    """Tạo demo dashboard với Advanced Components"""
    st.markdown("# 🚀 Demo Advanced Components")
    
    # Feature announcement
    st.markdown(AdvancedComponents.feature_announcement(
        "HRMS Modern UI ra mắt!", 
        "Giao diện được thiết kế lại hoàn toàn với Material Design 3, Component System chuyên nghiệp và Design Tokens.",
        "v2.0"
    ), unsafe_allow_html=True)
    
    # Stats grid
    stats_data = [
        {'icon': '👥', 'title': 'Tổng nhân sự', 'value': '150', 'subtitle': 'Tăng 5 người', 'trend': 'up'},
        {'icon': '⏰', 'title': 'Sắp nghỉ hưu', 'value': '12', 'subtitle': 'Giảm 2 người', 'trend': 'down'},
        {'icon': '💰', 'title': 'Nâng lương', 'value': '25', 'subtitle': 'Tăng 8 người', 'trend': 'up'},
        {'icon': '📄', 'title': 'Hợp đồng', 'value': '6', 'subtitle': 'Hết hạn', 'trend': 'neutral'}
    ]
    
    st.markdown(AdvancedComponents.stats_grid(stats_data), unsafe_allow_html=True)
    
    # Progress cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(AdvancedComponents.progress_card(
            "Hoàn thành mục tiêu Q4", 85, 100, "🎯", "#4CAF50"
        ), unsafe_allow_html=True)
        
        st.markdown(AdvancedComponents.progress_card(
            "Đào tạo nhân viên", 42, 60, "🎓", "#FF9800"
        ), unsafe_allow_html=True)
    
    with col2:
        # Timeline
        timeline_events = [
            {'title': 'Rà soát nhân sự', 'description': 'Hoàn tất đánh giá hiệu suất', 'date': '15/11/2024', 'status': 'completed'},
            {'title': 'Nâng lương Q4', 'description': 'Xử lý 25 hồ sơ nâng lương', 'date': '01/12/2024', 'status': 'current'},
            {'title': 'Kế hoạch 2025', 'description': 'Lập kế hoạch nhân sự năm mới', 'date': '15/12/2024', 'status': 'future'}
        ]
        
        st.markdown(AdvancedComponents.status_timeline(timeline_events), unsafe_allow_html=True)
    
    # Quick actions
    actions_data = [
        {'icon': '👥', 'title': 'Thêm nhân viên', 'description': 'Tạo hồ sơ mới', 'color': '#6750A4'},
        {'icon': '💰', 'title': 'Xử lý lương', 'description': 'Nâng lương & thưởng', 'color': '#4CAF50'},
        {'icon': '📊', 'title': 'Báo cáo', 'description': 'Xuất báo cáo tháng', 'color': '#2196F3'},
        {'icon': '⚙️', 'title': 'Cài đặt', 'description': 'Quản lý hệ thống', 'color': '#FF9800'}
    ]
    
    st.markdown(AdvancedComponents.quick_actions_panel(actions_data), unsafe_allow_html=True)

if __name__ == "__main__":
    # Demo page
    create_demo_dashboard()
