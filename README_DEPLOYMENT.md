# 🚀 HƯỚNG DẪN TRIỂN KHAI HRMS

> Hệ thống Quản lý Nhân sự - Frontend & Backend 100% Python

## 📋 Yêu cầu hệ thống

- **Windows 10/11** (64-bit)  
- **Python 3.8+** ([Tải tại python.org](https://python.org))
- **4GB RAM** trở lên
- **Kết nối Internet** (cho lần cài đặt đầu tiên)

## ⚡ Cài đặt nhanh (2 bước)

### Bước 1: Thiết lập dự án
```batch
setup.bat
```
**Chức năng:**
- ✅ Kiểm tra Python
- ✅ Cập nhật pip
- ✅ Cài đặt thư viện Streamlit + dependencies
- ✅ Tạo thư mục cần thiết
- ✅ Khởi tạo môi trường

### Bước 2: Chạy ứng dụng
```batch
run.bat
```
**Chức năng:**
- ✅ Kiểm tra môi trường
- ✅ Khởi động server Streamlit
- ✅ Tự động mở browser tại http://localhost:8501

---

## 🔐 Thông tin đăng nhập

```
👤 Tên đăng nhập: admin
🔑 Mật khẩu: admin123
```

---

## 📱 11 Chức năng chính

| STT | Chức năng | Mô tả |
|-----|-----------|-------|
| 1️⃣ | **Tra cứu nhân sự** | Tìm kiếm, xem chi tiết 5 tabs thông tin |
| 2️⃣ | **Nâng lương định kỳ** | Logic 36/24 tháng + phụ cấp thâm niên |
| 3️⃣ | **Theo dõi nghỉ hưu** | Cảnh báo 6/3 tháng, xuất văn bản |
| 4️⃣ | **Kiểm tra quy hoạch** | Quản lý tuổi, quota theo vị trí |
| 5️⃣ | **Quá trình công tác** | Timeline, thêm/sửa/xóa giai đoạn |
| 6️⃣ | **Hợp đồng lao động** | Quản lý BKS + nhân viên, cảnh báo hết hạn |
| 7️⃣ | **Điều kiện bổ nhiệm** | Kiểm tra đầy đủ, cảnh báo 90 ngày |
| 8️⃣ | **Điều kiện khen thưởng** | Đánh giá tiêu chí khen thưởng |
| 9️⃣ | **Nâng lương trước hạn** | Quản lý thành tích xuất sắc |
| 🔟 | **Báo cáo thống kê** | Phân tích toàn diện, charts tương tác |
| 1️⃣1️⃣ | **Báo bảo hiểm** | Nhắc nhở, xuất Excel BHXH |

---

## 🛠️ Xử lý sự cố thường gặp

### ❌ Lỗi: "Python không tìm thấy"
**Nguyên nhân:** Python chưa được cài đặt hoặc chưa add vào PATH
**Giải pháp:**
1. Tải Python từ [python.org](https://python.org)
2. ✅ **QUAN TRỌNG:** Tick "Add Python to PATH" khi cài đặt
3. Khởi động lại Command Prompt
4. Chạy lại `setup.bat`

### ❌ Lỗi: "Cổng 8501 đang được sử dụng"
**Giải pháp:**
1. Đóng tất cả Streamlit apps khác
2. Hoặc kill process: `taskkill /F /IM python.exe`
3. Chạy lại `run.bat`

### ❌ Lỗi: "Module không tìm thấy"
**Giải pháp:**
```batch
# Cài đặt lại thư viện
pip install -r requirements.txt

# Hoặc chạy lại setup
setup.bat
```

### ❌ Lỗi: "Permission denied"
**Giải pháp:**
1. Chạy Command Prompt **với quyền Administrator**
2. Navigate đến thư mục dự án
3. Chạy lại `setup.bat`

---

## 🗂️ Cấu trúc dự án

```
HRMS/
├── 📄 setup.bat              # Script cài đặt
├── 🚀 run.bat                # Script khởi chạy  
├── 🐍 streamlit_app.py       # Ứng dụng chính
├── 🐍 models_streamlit.py    # Database models
├── 🐍 utils_streamlit.py     # Business logic  
├── 🐍 run_streamlit.py       # Launcher
├── 📋 requirements.txt       # Dependencies
├── 📖 README.md              # Tài liệu chính
├── 📁 exports/               # File xuất ra
└── 🗄️ hrms_streamlit.db     # SQLite database
```

---

## 🔧 Tùy chỉnh cấu hình

### Đổi port (nếu cần)
Sửa file `run_streamlit.py`:
```python
if __name__ == "__main__":
    st.set_page_config(...)
    
    # Đổi port từ 8501 sang port khác
    os.system("streamlit run streamlit_app.py --server.port 9000")
```

### Thêm dữ liệu mẫu
- Dữ liệu mẫu tự động tạo khi khởi động lần đầu
- File database: `hrms_streamlit.db`
- Có thể import/export qua Excel

---

## 📞 Hỗ trợ

### Kiểm tra phiên bản
```batch
python --version
streamlit --version
```

### Log files  
- Streamlit logs: Hiển thị trong terminal khi chạy
- Application logs: Xem trong tab "Báo cáo thống kê"

### Reset dữ liệu
```batch
# Xóa database để reset về mặc định
del hrms_streamlit.db
```

---

## 🎯 Tính năng nổi bật

✨ **100% Python** - Không HTML/CSS/JS  
🎨 **Giao diện đẹp** - Streamlit professional UI  
🧠 **Logic phức tạp** - Nâng lương 36/24 tháng, phụ cấp thâm niên  
🔔 **Cảnh báo thông minh** - Màu sắc ưu tiên, nhắc nhở tự động  
📊 **Charts tương tác** - Plotly visualizations  
📄 **Xuất văn bản** - Word, Excel templates  
⚡ **Hiệu suất cao** - SQLAlchemy ORM + SQLite  

---

## 🏁 Sẵn sàng sử dụng!

1. Chạy `setup.bat` (chỉ lần đầu)
2. Chạy `run.bat` 
3. Truy cập http://localhost:8501
4. Đăng nhập: admin/admin123
5. Khám phá 11 chức năng nghiệp vụ!

**🎊 Chúc bạn sử dụng HRMS hiệu quả!**
