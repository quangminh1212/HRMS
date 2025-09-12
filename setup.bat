@echo off
chcp 65001 > nul
echo ============================================================
echo 🔧 THIẾT LẬP DỰ ÁN HRMS - Hệ thống Quản lý Nhân sự
echo ============================================================
echo ✨ Frontend ^& Backend 100%% Python với Streamlit
echo 🎯 Đáp ứng đầy đủ 11 yêu cầu nghiệp vụ
echo ============================================================
echo.

echo [1/4] 📦 Kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt!
    echo 💡 Vui lòng tải Python từ: https://python.org
    echo 🔗 Chọn phiên bản 3.8 trở lên
    pause
    exit /b 1
) else (
    echo ✅ Python đã sẵn sàng
    python --version
)
echo.

echo [2/4] 🔄 Cập nhật pip...
python -m pip install --upgrade pip
echo ✅ Pip đã được cập nhật
echo.

echo [3/4] 📚 Cài đặt thư viện cần thiết...
echo 🔽 Đang cài đặt dependencies từ requirements.txt...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Lỗi khi cài đặt thư viện!
    echo 💡 Kiểm tra kết nối mạng và thử lại
    pause
    exit /b 1
) else (
    echo ✅ Tất cả thư viện đã được cài đặt thành công
)
echo.

echo [4/4] 🗃️ Khởi tạo cơ sở dữ liệu...
if not exist "exports" mkdir exports
echo ✅ Thư mục exports đã được tạo
echo ✅ Cơ sở dữ liệu sẽ được khởi tạo khi chạy lần đầu
echo.

echo ============================================================
echo 🎉 THIẾT LẬP HOÀN TẤT!
echo ============================================================
echo 🚀 Cách chạy dự án:
echo    • Chạy tự động: run.bat
echo    • Chạy thủ công: python run_streamlit.py
echo.
echo 🌐 Truy cập: http://localhost:8501
echo 👤 Tài khoản: admin / admin123
echo ============================================================
echo 📋 Các chức năng chính:
echo    1️⃣  Tra cứu thông tin nhân sự
echo    2️⃣  Nâng lương định kỳ
echo    3️⃣  Theo dõi nghỉ hưu  
echo    4️⃣  Kiểm tra quy hoạch
echo    5️⃣  Quá trình công tác
echo    6️⃣  Hợp đồng lao động
echo    7️⃣  Điều kiện bổ nhiệm
echo    8️⃣  Điều kiện khen thưởng
echo    9️⃣  Nâng lương trước hạn
echo    🔟 Báo cáo thống kê
echo    1️⃣1️⃣ Báo bảo hiểm
echo ============================================================
echo.
echo ✅ Sẵn sàng sử dụng! Nhấn Enter để đóng...
pause >nul
