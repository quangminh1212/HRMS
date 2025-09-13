#!/usr/bin/env python3
"""
Simple HRMS Test App - Để test localhost:3000
"""

import streamlit as st
import time

# Configure page
st.set_page_config(
    page_title="HRMS Test",
    page_icon="🏢",
    layout="wide"
)

# Simple app
st.title("🏢 HRMS - Test App")
st.write("Đây là app test đơn giản để kiểm tra localhost:3000")

# Login form
with st.form("login_form"):
    st.subheader("🔐 Đăng nhập")
    username = st.text_input("👤 Tên đăng nhập")
    password = st.text_input("🔒 Mật khẩu", type="password")
    submit = st.form_submit_button("🚀 Đăng nhập")
    
    if submit:
        if username == "admin" and password == "admin123":
            st.success("✅ Đăng nhập thành công!")
            st.balloons()
        else:
            st.error("❌ Sai thông tin đăng nhập")

# Test features
st.subheader("🧪 Test Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Nhân viên", "150", "5")

with col2:
    st.metric("💰 Lương TB", "15M", "2M")

with col3:
    st.metric("📊 Hiệu suất", "95%", "3%")

# Simple chart
import pandas as pd
import plotly.express as px

data = pd.DataFrame({
    'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5'],
    'Nhân viên': [100, 110, 120, 135, 150]
})

fig = px.line(data, x='Tháng', y='Nhân viên', title='📈 Tăng trưởng nhân sự')
st.plotly_chart(fig, use_container_width=True)

st.success("🎉 App test hoạt động tốt!")
st.info("💡 Localhost:3000 đang hoạt động bình thường")
