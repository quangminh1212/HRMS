@echo off
chcp 65001 > nul
echo ============================================================
echo 🔧 XÂY DỰNG FILE THỰC THI HRMS DESKTOP
echo ============================================================
echo ✨ Tạo file .exe cho Windows từ Python
echo 🎯 Không cần cài Python để chạy ứng dụng
echo ============================================================
echo.

echo [1/4] 📦 Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không tìm thấy!
    echo 💡 Vui lòng chạy setup.bat trước
    pause
    exit /b 1
) else (
    echo ✅ Python sẵn sàng
)
echo.

echo [2/4] 🔧 Cài đặt PyInstaller...
python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo ❌ Lỗi cài đặt PyInstaller!
    pause
    exit /b 1
) else (
    echo ✅ PyInstaller đã sẵn sàng
)
echo.

echo [3/4] 📦 Cài đặt dependencies...
python -m pip install -r requirements_desktop.txt
if %errorlevel% neq 0 (
    echo ❌ Lỗi cài đặt dependencies!
    pause
    exit /b 1
) else (
    echo ✅ Dependencies đã sẵn sàng  
)
echo.

echo [4/4] 🏗️  Xây dựng file exe...
echo 🔥 Đang biên dịch... Vui lòng chờ...

pyinstaller --onefile ^
    --windowed ^
    --name="HRMS_Desktop" ^
    --icon=hrms.ico ^
    --add-data "hrms_desktop.db;." ^
    --hidden-import=customtkinter ^
    --hidden-import=tkinter ^
    --hidden-import=sqlite3 ^
    --hidden-import=pandas ^
    --hidden-import=PIL ^
    --distpath=dist ^
    --workpath=build ^
    --specpath=build ^
    hrms_desktop.py

if %errorlevel% neq 0 (
    echo ❌ Lỗi khi xây dựng file exe!
    echo 💡 Kiểm tra lỗi ở trên và thử lại
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 🎉 XÂY DỰNG HOÀN TẤT!
echo ============================================================
echo 📂 File exe được tạo tại: dist\HRMS_Desktop.exe
echo 💾 Dung lượng: khoảng 50-100MB
echo.
echo 🚀 Cách sử dụng:
echo    • Copy file HRMS_Desktop.exe sang máy khác
echo    • Double-click để chạy (không cần cài Python)
echo    • Đăng nhập: admin / admin123
echo.
echo 📋 Lưu ý:
echo    • File exe chỉ chạy trên Windows
echo    • Lần đầu chạy có thể hơi chậm
echo    • Windows Defender có thể cảnh báo (an toàn)
echo ============================================================
echo.
pause
