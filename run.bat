@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title HRMS - Hệ thống Quản lý Nhân sự

echo 🏢 HRMS - Hệ thống Quản lý Nhân sự
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

echo ✅ Hệ thống sẵn sàng
echo.

echo Chọn phiên bản:
echo [1] HRMS Modern     [2] Quick Start      [3] Launcher Menu
echo [4] Streamlit       [5] Flet (Desktop)   [6] NiceGUI
echo [7] Manual Mode (no auto-restart)
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
REM Kiểm tra port
netstat -ano | findstr :%port_number% >nul
if !errorlevel!==0 (
    echo ✅ Server OK
) else (
    echo ❌ Restarting server...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq HRMS*" >nul 2>&1
    start /MIN "HRMS Server" python %script_name%
    timeout /t 15 >nul
)

timeout /t 30 >nul
goto keep_alive_loop

:process_choice
if "%choice%"=="1" (
    echo Starting HRMS Modern... URL: http://localhost:3000
    call :keep_alive_function run.py 3000
) else if "%choice%"=="2" (
    echo Quick Start... Installing dependencies if needed...
    python -c "import streamlit" >nul 2>&1
    if !errorlevel! neq 0 (
        pip install streamlit plotly pandas sqlalchemy python-docx openpyxl pillow python-dateutil
    )
    echo Starting HRMS Modern... URL: http://localhost:3000
    call :keep_alive_function run.py 3000
) else if "%choice%"=="3" (
    echo Starting Launcher Menu...
    call :keep_alive_function apps\launcher.py 8080
) else if "%choice%"=="4" (
    echo Starting Streamlit Classic...
    call :keep_alive_function apps\run_classic.py 8501
) else if "%choice%"=="5" (
    echo Starting Flet...
    call :keep_alive_function apps\run_flet.py 8550
) else if "%choice%"=="6" (
    echo Starting NiceGUI...
    call :keep_alive_function apps\run_nicegui.py 8080
) else if "%choice%"=="7" (
    echo Manual Mode - URL: http://localhost:3000
    python run.py
) else (
    echo Invalid choice. Starting HRMS Modern...
    call :keep_alive_function run.py 3000
)

echo.
echo 👋 Cảm ơn bạn đã sử dụng HRMS!
pause
