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

REM ===== AUTO KEEP-ALIVE =====
:keep_alive_loop
netstat -ano | findstr :3000 >nul
if !errorlevel!==0 (
    echo ✅ Server running
) else (
    echo 🔄 Starting server...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq HRMS*" >nul 2>&1
    start /MIN "HRMS Server" python -m streamlit run app_minimal.py --server.port 3000 --server.address 0.0.0.0
    timeout /t 15 >nul
)

timeout /t 30 >nul
goto keep_alive_loop


