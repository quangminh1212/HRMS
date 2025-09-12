@echo off
chcp 65001 > nul
title HRMS - Hệ thống Quản lý Nhân sự
color 0A

echo ============================================================
echo 🚀 KHỞI CHẠY HRMS - Hệ thống Quản lý Nhân sự
echo ============================================================
echo ✨ Desktop Application 100%% Python với CustomTkinter
echo 🎯 Đáp ứng đầy đủ 11 yêu cầu nghiệp vụ  
echo ============================================================
echo.

echo [1/3] 📦 Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không tìm thấy!
    echo 💡 Vui lòng chạy setup.bat trước để cài đặt
    pause
    exit /b 1
) else (
    echo ✅ Python sẵn sàng
)
echo.

echo [2/3] 📚 Kiểm tra thư viện CustomTkinter...
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ CustomTkinter chưa được cài đặt!
    echo 💡 Đang tự động cài đặt...
    python -m pip install -r requirements_desktop.txt
    if %errorlevel% neq 0 (
        echo ❌ Cài đặt thất bại! Chạy setup.bat để thiết lập đầy đủ
        pause
        exit /b 1
    )
) else (
    echo ✅ CustomTkinter đã sẵn sàng
)
echo.

echo [3/3] 🖥️  Khởi động ứng dụng...
echo ============================================================
echo 🔥 HRMS Desktop đang khởi động...
echo ============================================================
echo 🖼️  Giao diện: Desktop GUI Application
echo 👤 Tài khoản: admin
echo 🔑 Mật khẩu: admin123
echo ============================================================
echo ⚠️  Đóng cửa sổ để thoát ứng dụng
echo 💡 Không cần trình duyệt web
echo ============================================================
echo.

rem Chờ 2 giây trước khi khởi chạy
timeout /t 2 /nobreak >nul

rem Khởi chạy ứng dụng desktop
python hrms_desktop.py

rem Xử lý khi ứng dụng kết thúc
echo.
echo ============================================================
echo 🛑 ỨNG DỤNG ĐÃ DỪNG
echo ============================================================
echo 💡 Các lý do có thể:
echo    • Bạn đã đóng cửa sổ ứng dụng
echo    • Có lỗi trong quá trình chạy
echo    • Thiếu thư viện CustomTkinter
echo.
echo 🔄 Muốn chạy lại? Chạy: run.bat
echo 🔧 Cần cài đặt lại? Chạy: setup.bat
echo ============================================================
echo.
pause
