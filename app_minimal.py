#!/usr/bin/env python3
"""
HRMS Minimal - App tối giản để test
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="HRMS Minimal",
    page_icon="🏢",
    layout="wide"
)

# Main content
st.title("🏢 HRMS - Hệ thống Quản lý Nhân sự")
st.markdown("### ✅ App đã load thành công!")

# Login form
with st.form("login_form"):
    st.subheader("🔐 Đăng nhập")
    username = st.text_input("👤 Tên đăng nhập", value="admin")
    password = st.text_input("🔒 Mật khẩu", type="password", value="admin123")
    submit = st.form_submit_button("🚀 Đăng nhập")
    
    if submit:
        if username == "admin" and password == "admin123":
            st.success("✅ Đăng nhập thành công!")
            st.balloons()
        else:
            st.error("❌ Sai thông tin đăng nhập")

# Simple metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Nhân viên", "150")

with col2:
    st.metric("💰 Lương TB", "15M VNĐ")

with col3:
    st.metric("📊 Hiệu suất", "95%")

st.success("🎉 HRMS Minimal đang hoạt động tốt!")
st.info("💡 Localhost:3000 đã sẵn sàng")
