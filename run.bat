@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title HRMS - Hệ thống Quản lý Nhân sự

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🏢 HRMS - HỆ THỐNG QUẢN LÝ NHÂN SỰ (AUTO KEEP-ALIVE)
echo ═══════════════════════════════════════════════════════════════════
echo 💎 HRMS Modern - Giao diện Material Design 3
echo 🎨 Component System chuyên nghiệp
echo 🔄 Tự động duy trì server cho tất cả lựa chọn
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
echo [1] 💎 HRMS Modern (MỚI NHẤT)    - Giao diện đẹp nhất + Auto Keep-Alive
echo [2] ⚡ Quick Start              - Khởi động nhanh + Auto Keep-Alive
echo [3] 🎮 Launcher Menu             - Chọn nhiều framework + Auto Keep-Alive
echo [4] 🌐 Streamlit Classic         - Phiên bản ổn định + Auto Keep-Alive
echo [5] 📱 Flet (Flutter UI)         - Cross-platform + Auto Keep-Alive
echo [6] ✨ NiceGUI (Tailwind)        - Web hiện đại + Auto Keep-Alive
echo [7] 🛠️  Manual Mode               - Chạy 1 lần không auto restart
echo.
echo 💡 Tất cả lựa chọn đều có tính năng Auto Keep-Alive (tự động duy trì server)
echo ⚠️  Nhấn Ctrl+C để dừng hoàn toàn
echo.

set /p choice="👉 Chọn (1-7): "

REM ===== KEEP ALIVE FUNCTION =====
goto :process_choice

:keep_alive_function
set script_name=%1
set port_number=%2
if "%port_number%"=="" set port_number=3000

echo.
echo 🌐 AUTO KEEP-ALIVE MODE ACTIVATED
echo ======================================================================
echo 💡 Script sẽ tự động duy trì server trên localhost:%port_number%
echo 🔄 Tự động restart nếu server bị dừng
echo ⚠️  Nhấn Ctrl+C để dừng hoàn toàn
echo ======================================================================
echo.

:keep_alive_loop
echo [%date% %time%] 🚀 Đang kiểm tra server trên port %port_number%...

REM Kiểm tra port có đang hoạt động không
netstat -ano | findstr :%port_number% >nul
if !errorlevel!==0 (
    echo [%date% %time%] ✅ Server đang hoạt động tốt trên localhost:%port_number%
) else (
    echo [%date% %time%] ❌ Server không phản hồi, đang khởi động lại...
    echo [%date% %time%] 🔄 Restarting %script_name%...

    REM Kill any remaining processes
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq HRMS*" >nul 2>&1

    REM Restart server
    start /MIN "HRMS Server" python %script_name%

    echo [%date% %time%] ⏳ Chờ 15 giây để server khởi động...
    timeout /t 15 >nul
)

echo [%date% %time%] 💤 Chờ 30 giây trước khi kiểm tra lại...
timeout /t 30 >nul
goto keep_alive_loop

:process_choice
if "%choice%"=="1" (
    echo 💎 Đang khởi động HRMS Modern với Auto Keep-Alive...
    echo 🌐 URL: http://localhost:3000
    echo 🔑 admin/admin123
    call :keep_alive_function run.py 3000
) else if "%choice%"=="2" (
    echo ⚡ HRMS MODERN - QUICK START với Auto Keep-Alive
    echo 🚀 Khởi động nhanh với tự động cài đặt dependencies...
    echo.

    REM Kiểm tra dependencies nhanh
    python -c "import streamlit" >nul 2>&1
    if !errorlevel! neq 0 (
        echo 🔧 Cài đặt dependencies...
        pip install streamlit plotly pandas sqlalchemy python-docx openpyxl pillow python-dateutil
    )

    echo ✅ Đang khởi động HRMS Modern với Auto Keep-Alive...
    echo 🌐 URL: http://localhost:3000
    echo 🔑 admin/admin123
    call :keep_alive_function run.py 3000
) else if "%choice%"=="3" (
    echo 🎮 Đang mở Launcher Menu với Auto Keep-Alive...
    call :keep_alive_function apps\launcher.py 8080
) else if "%choice%"=="4" (
    echo 🌐 Đang khởi động Streamlit Classic với Auto Keep-Alive...
    call :keep_alive_function apps\run_classic.py 8501
) else if "%choice%"=="5" (
    echo 📱 Đang khởi động Flet với Auto Keep-Alive...
    call :keep_alive_function apps\run_flet.py 8550
) else if "%choice%"=="6" (
    echo ✨ Đang khởi động NiceGUI với Auto Keep-Alive...
    call :keep_alive_function apps\run_nicegui.py 8080
) else if "%choice%"=="7" (
    echo 🛠️  MANUAL MODE - Chạy 1 lần không auto restart
    echo 💎 Đang khởi động HRMS Modern...
    echo 🌐 URL: http://localhost:3000
    echo 🔑 admin/admin123
    echo ⚠️  Server sẽ dừng khi bạn đóng cửa sổ này
    python run.py
) else (
    echo ❌ Lựa chọn không hợp lệ!
    echo 💡 Mặc định chạy HRMS Modern với Auto Keep-Alive...
    call :keep_alive_function run.py 3000
)

echo.
echo 👋 Cảm ơn bạn đã sử dụng HRMS!
pause
