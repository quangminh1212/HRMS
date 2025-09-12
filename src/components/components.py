"""
HRMS Modern Components
Chứa các UI components để tránh circular import
"""

import streamlit as st
import pandas as pd


class ModernComponents:
    """Class chứa các components UI hiện đại"""
    
    @staticmethod
    def hero_header(title: str, subtitle: str = None, icon: str = "🏢"):
        """Hero header với gradient background"""
        subtitle_html = f'<div class="headline-medium" style="opacity: 0.8; margin-top: 1rem;">{subtitle}</div>' if subtitle else ""
        
        return st.markdown(f"""
        <div class="hero-header animate-fade-in">
            <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1rem;">
                <div style="font-size: 3rem;">{icon}</div>
                <div>
                    <div class="display-small">{title}</div>
                    {subtitle_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod  
    def metric_card(title: str, value: str, change: str = None, icon: str = "📊"):
        """Metric card với hover effects"""
        change_html = f'<div class="label-large" style="color: #1565C0; margin-top: 0.5rem;">↗ {change}</div>' if change else ""
        
        return f"""
        <div class="metric-card animate-scale-up">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <div class="label-large" style="opacity: 0.7;">{title}</div>
                    <div class="display-medium" style="margin: 0.5rem 0;">{value}</div>
                    {change_html}
                </div>
                <div style="font-size: 2rem; opacity: 0.6;">{icon}</div>
            </div>
        </div>
        """
    
    @staticmethod
    def modern_alert(title: str, content: str, type: str = "info", details: str = None):
        """Modern alert component"""
        icons = {
            "warning": "⚠️",
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
