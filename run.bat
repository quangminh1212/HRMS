@echo off
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
echo [2] 🎮 Launcher Menu             - Chọn nhiều framework  
echo [3] 🌐 Streamlit Classic         - Phiên bản ổn định
echo [4] 📱 Flet (Flutter UI)         - Cross-platform
echo [5] ✨ NiceGUI (Tailwind)        - Web hiện đại
echo.

set /p choice="👉 Chọn (1-5): "

if "%choice%"=="1" (
    echo 💎 Đang khởi động HRMS Modern...
    echo 🌐 Mở trình duyệt tại: http://localhost:8501
    echo ⚠️  Nhấn Ctrl+C để dừng
    python run.py
) else if "%choice%"=="2" (
    echo 🎮 Đang mở Launcher Menu...
    python launcher.py
) else if "%choice%"=="3" (
    echo 🌐 Đang khởi động Streamlit Classic...
    python run_classic.py
) else if "%choice%"=="4" (
    echo 📱 Đang khởi động Flet...
    python run_flet.py
) else if "%choice%"=="5" (
    echo ✨ Đang khởi động NiceGUI...
    python run_nicegui.py
) else (
    echo ❌ Lựa chọn không hợp lệ!
    echo 💡 Mặc định chạy HRMS Modern...
    python run.py
)

echo.
echo 👋 Cảm ơn bạn đã sử dụng HRMS!
pause
