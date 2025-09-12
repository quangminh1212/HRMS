@echo off
chcp 65001 >nul
title HRMS Modern - Quick Start

echo 💎 HRMS MODERN - QUICK START
echo 🚀 Khởi động nhanh giao diện Material Design 3...
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không tìm thấy. Chạy setup.bat trước.
    timeout /t 3 >nul
    exit /b 1
)

REM Kiểm tra dependencies nhanh
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔧 Cài đặt dependencies...
    pip install streamlit plotly pandas sqlalchemy python-docx openpyxl pillow python-dateutil
)

echo ✅ Đang khởi động HRMS Modern...
echo 🌐 URL: http://localhost:8501  
echo 🔑 admin/admin123
echo.

python run.py
