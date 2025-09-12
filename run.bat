@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title HRMS - Hệ thống Quản lý Nhân sự

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🏢 HRMS - HỆ THỐNG QUẢN LÝ NHÂN SỰ
echo ═══════════════════════════════════════════════════════════════════
echo 💎 HRMS Modern - Giao diện Material Design 3
echo 🎨 Component System chuyên nghiệp
echo ═══════════════════════════════════════════════════════════════════
echo.

echo 🔍 Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt
    echo 💡 Vui lòng chạy setup.bat trước
    pause
    exit /b 1
)

echo 🔍 Kiểm tra dependencies...
python -c "import streamlit, plotly, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Dependencies chưa được cài đặt
    echo 💡 Vui lòng chạy setup.bat trước
    pause
    exit /b 1
)

echo ✅ Hệ thống đã sẵn sàng!
echo.

echo 🚀 Bạn muốn chạy phiên bản nào?
echo.
echo [1] 💎 HRMS Modern (MỚI NHẤT)    - Giao diện đẹp nhất
echo [2] ⚡ Quick Start              - Khởi động nhanh, tự cài dependencies
echo [3] 🌐 Keep Alive               - Duy trì server tự động, không bao giờ tắt
echo [4] 🎮 Launcher Menu             - Chọn nhiều framework  
echo [5] 🌐 Streamlit Classic         - Phiên bản ổn định
echo [6] 📱 Flet (Flutter UI)         - Cross-platform
echo [7] ✨ NiceGUI (Tailwind)        - Web hiện đại
echo.

set /p choice="👉 Chọn (1-7): "

if "%choice%"=="1" (
    echo 💎 Đang khởi động HRMS Modern...
    echo 🌐 Mở trình duyệt tại: http://localhost:8501
    echo ⚠️  Nhấn Ctrl+C để dừng
    python run.py
) else if "%choice%"=="2" (
    echo ⚡ HRMS MODERN - QUICK START
    echo 🚀 Khởi động nhanh với tự động cài đặt dependencies...
    echo.
    
    REM Kiểm tra dependencies nhanh
    python -c "import streamlit" >nul 2>&1
    if !errorlevel! neq 0 (
        echo 🔧 Cài đặt dependencies...
        pip install streamlit plotly pandas sqlalchemy python-docx openpyxl pillow python-dateutil
    )
    
    echo ✅ Đang khởi động HRMS Modern...
    echo 🌐 URL: http://localhost:8501  
    echo 🔑 admin/admin123
    echo.
    python run.py
) else if "%choice%"=="3" (
    echo 🌐 HRMS LOCALHOST KEEPER - DUY TRI SERVER
    echo ======================================================================
    echo 💡 Script này sẽ tự động duy trì localhost:8501
    echo 🔄 Tự động restart nếu server bị dừng
    echo ⚠️  Nhấn Ctrl+C để dừng hoàn toàn
    echo ======================================================================
    echo.
    
    :keep_alive_start
    echo [%date% %time%] 🚀 Đang kiểm tra HRMS server...
    
    REM Kiểm tra port 8501 có đang hoạt động không
    netstat -ano | findstr :8501 >nul
    if !errorlevel!==0 (
        echo [%date% %time%] ✅ Server đang hoạt động tốt trên localhost:8501
    ) else (
        echo [%date% %time%] ❌ Server không phản hồi, đang khởi động lại...
        echo [%date% %time%] 🔄 Restarting HRMS Modern...
        
        REM Kill any remaining processes
        taskkill /F /IM python.exe /FI "WINDOWTITLE eq HRMS*" >nul 2>&1
        
        REM Restart server
        start /MIN "HRMS Server" python run.py
        
        echo [%date% %time%] ⏳ Chờ 10 giây để server khởi động...
        timeout /t 10 >nul
    )
    
    echo [%date% %time%] 💤 Chờ 30 giây trước khi kiểm tra lại...
    timeout /t 30 >nul
    goto keep_alive_start
) else if "%choice%"=="4" (
    echo 🎮 Đang mở Launcher Menu...
    python apps\launcher.py
) else if "%choice%"=="5" (
    echo 🌐 Đang khởi động Streamlit Classic...
    python apps\run_classic.py
) else if "%choice%"=="6" (
    echo 📱 Đang khởi động Flet...
    python apps\run_flet.py
) else if "%choice%"=="7" (
    echo ✨ Đang khởi động NiceGUI...
    python apps\run_nicegui.py
) else (
    echo ❌ Lựa chọn không hợp lệ!
    echo 💡 Mặc định chạy HRMS Modern...
    python run.py
)

echo.
echo 👋 Cảm ơn bạn đã sử dụng HRMS!
pause
