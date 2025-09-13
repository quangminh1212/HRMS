@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title HRMS - Hệ thống Quản lý Nhân sự

echo 🏢 HRMS - Hệ thống Quản lý Nhân sự Modern
echo.

REM Kiểm tra Python và dependencies
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt. Chạy setup.bat trước.
    pause
    exit /b 1
)

python -c "import streamlit, plotly, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Dependencies chưa được cài đặt. Chạy setup.bat trước.
    pause
    exit /b 1
)

echo ✅ Đang khởi động HRMS Modern...
echo 🌐 URL: http://localhost:3000
echo.

REM Chạy trực tiếp Streamlit
python -m streamlit run app_minimal.py --server.port 3000 --server.address 0.0.0.0


