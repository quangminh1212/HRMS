@echo off
chcp 65001 >nul
title HRMS Setup - Cài đặt Hệ thống Quản lý Nhân sự

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 HRMS SETUP - THIẾT LẬP HỆ THỐNG QUẢN LÝ NHÂN SỰ
echo ═══════════════════════════════════════════════════════════════════
echo 💎 Phiên bản Modern với giao diện Material Design 3
echo 🎨 Bộ sưu tập đa framework: Streamlit, Flet, NiceGUI
echo ═══════════════════════════════════════════════════════════════════
echo.

echo [1/4] Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt hoặc không có trong PATH
    echo 💡 Vui lòng tải Python từ: https://python.org/downloads/
    echo 🔧 Đảm bảo chọn "Add Python to PATH" khi cài đặt
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% đã sẵn sàng

echo.
echo [2/4] Nâng cấp pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️ Không thể nâng cấp pip, tiếp tục với phiên bản hiện tại
)

echo.
echo [3/4] Cài đặt dependencies...
echo 📦 Đang cài đặt các thư viện cần thiết...

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Lỗi khi cài đặt dependencies
    echo 💡 Hãy thử chạy lại script với quyền Administrator
    pause
    exit /b 1
)

echo ✅ Đã cài đặt tất cả dependencies thành công

echo.
echo [4/4] Tạo thư mục exports...
if not exist exports mkdir exports
echo ✅ Đã tạo thư mục exports

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🎉 CÀI ĐẶT HOÀN TẤT!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 🚀 Cách chạy HRMS:
echo    [Khuyến nghị] python launch_hrms.py    - Menu chọn framework
echo    [Trực tiếp]   python run_modern.py     - HRMS Modern (mới nhất)
echo    [Classic]     python run_streamlit.py  - Streamlit Classic
echo    [Flutter UI]  python run_flet.py       - Flet (Flutter)
echo    [Tailwind]    python run_nicegui.py    - NiceGUI (Tailwind CSS)
echo.
echo 🔑 Thông tin đăng nhập:
echo    👤 Username: admin
echo    🔒 Password: admin123
echo.
echo 📁 Thư mục dự án: %CD%
echo 🌐 Port mặc định: 8501 (Modern), 8080 (Flet), 8090 (NiceGUI)
echo.
echo ═══════════════════════════════════════════════════════════════════

pause
