# 🖥️ HRMS Desktop Application

> Hệ thống Quản lý Nhân sự - Desktop GUI 100% Python

## ✨ Đặc điểm nổi bật

- 🖼️ **Desktop Application** - Không cần trình duyệt web
- 🎯 **100% Python** - CustomTkinter cho giao diện native Windows  
- 🚀 **Hiệu suất cao** - Không phụ thuộc localhost/server
- 💾 **Offline hoàn toàn** - SQLite database cục bộ
- 🎨 **Giao diện đẹp** - Modern UI với CustomTkinter
- 📦 **Portable** - Có thể build thành file .exe

## 📋 Yêu cầu hệ thống

- **Windows 10/11** (64-bit)  
- **Python 3.8+** ([Tải tại python.org](https://python.org))
- **4GB RAM** trở lên
- **Kết nối Internet** (chỉ cho lần cài đặt đầu tiên)

## ⚡ Cài đặt & Chạy (2 bước)

### Bước 1: Thiết lập
```batch
setup.bat
```
**➡️ Tự động cài đặt CustomTkinter + dependencies**

### Bước 2: Chạy ứng dụng
```batch
run.bat
```
**➡️ Desktop application sẽ mở ngay lập tức**

---

## 🔐 Đăng nhập

```
👤 Tên đăng nhập: admin
🔑 Mật khẩu: admin123
```

---

## 📱 Giao diện Desktop

### 🏠 Dashboard chính
- **Sidebar navigation** với 11 chức năng
- **Statistics cards** hiển thị thống kê real-time
- **Recent activities** danh sách hoạt động gần đây
- **Professional UI** với CustomTkinter modern design

### 🔍 Tra cứu nhân sự (Đã hoàn thành)
- **Search interface** tìm kiếm theo tên/mã nhân viên
- **Employee results** hiển thị danh sách kết quả
- **Detail popup window** xem chi tiết đầy đủ thông tin
- **Export to Word** xuất thông tin ra file

### ⚙️ Các chức năng khác (Đang phát triển)
- 💰 Nâng lương định kỳ
- ⏰ Theo dõi nghỉ hưu  
- 📋 Kiểm tra quy hoạch
- 💼 Quá trình công tác
- 📄 Hợp đồng lao động
- ✅ Điều kiện bổ nhiệm
- 🏆 Điều kiện khen thưởng
- ⚡ Nâng lương trước hạn
- 📊 Báo cáo thống kê
- 🏥 Báo bảo hiểm

---

## 🏗️ Build file thực thi

### Tạo file .exe (không cần Python)
```batch
build_exe.bat
```

**Kết quả:**
- ✅ File `HRMS_Desktop.exe` trong thư mục `dist/`
- ✅ Dung lượng: ~50-100MB
- ✅ Chạy trên Windows mà không cần cài Python
- ✅ Portable - copy sang máy khác chạy ngay

### Cách sử dụng file .exe
1. **Copy** `HRMS_Desktop.exe` sang máy đích
2. **Double-click** để chạy (Windows có thể cảnh báo - bình thường)
3. **Đăng nhập** admin/admin123
4. **Sử dụng** đầy đủ 11 chức năng

---

## 🛠️ Cấu trúc dự án

```
HRMS/
├── 🖥️ hrms_desktop.py        # Ứng dụng desktop chính
├── 📦 requirements_desktop.txt # Dependencies cho desktop
├── 📦 setup.bat              # Script cài đặt
├── 🚀 run.bat                # Script khởi chạy  
├── 🏗️ build_exe.bat          # Script build exe
├── 🐍 models_streamlit.py    # Database models (tái sử dụng)
├── 🐍 utils_streamlit.py     # Business logic (tái sử dụng)
├── 📖 README_DESKTOP.md      # Tài liệu desktop
├── 🗄️ hrms_desktop.db       # SQLite database
└── 📁 dist/                  # Thư mục chứa file .exe
```

---

## 🎯 So sánh với Web version

| Tính năng | Web (Streamlit) | Desktop (CustomTkinter) |
|-----------|----------------|----------------------|
| **Giao diện** | Trình duyệt web | Native Windows GUI |
| **Hiệu suất** | Cần server | Chạy trực tiếp |
| **Offline** | Cần localhost:8501 | 100% offline |
| **Phân phối** | Cần Python + Browser | File .exe độc lập |
| **UI/UX** | Web responsive | Desktop native |
| **Dữ liệu** | SQLite | SQLite |
| **Chức năng** | 11 chức năng đầy đủ | 11 chức năng (phát triển) |

---

## 🔧 Xử lý sự cố

### ❌ "Module customtkinter not found"
```batch
# Cài đặt lại dependencies
pip install -r requirements_desktop.txt

# Hoặc chạy setup
setup.bat
```

### ❌ "Permission denied khi build exe"
1. Chạy Command Prompt **với quyền Administrator**
2. Navigate đến thư mục HRMS
3. Chạy `build_exe.bat`

### ❌ "Windows Defender cảnh báo file .exe"
- **Bình thường** - file Python được compile
- Click **"More info" → "Run anyway"**
- Hoặc thêm exception trong Windows Defender

### ❌ Database lỗi
```batch
# Xóa database để reset
del hrms_desktop.db

# Chạy lại app sẽ tạo database mới với sample data
run.bat
```

---

## 🎊 Kế hoạch phát triển

### 🔄 Phase 1 (Hiện tại)
- ✅ Login system với SQLite
- ✅ Dashboard với statistics
- ✅ Employee search với detail popup
- ✅ Export to Word functionality  
- ✅ Professional CustomTkinter UI

### 🚀 Phase 2 (Tiếp theo)
- 💰 Salary management với logic 36/24 tháng
- ⏰ Retirement tracking với alerts
- 📋 Planning management
- 💼 Work history timeline
- 📄 Contract management

### 🏆 Phase 3 (Tương lai)
- 📊 Advanced reporting với charts
- 🏥 Insurance integration  
- 🔄 Data import/export
- 🎨 Theme customization
- 📱 Multi-language support

---

## 💡 Lời khuyên sử dụng

### Cho người dùng cuối
- Sử dụng file `.exe` để dễ dàng triển khai
- Không cần kiến thức kỹ thuật
- Backup database định kỳ

### Cho developer  
- Sử dụng Python source code để phát triển
- CustomTkinter có documentation tốt
- SQLite dễ dàng migrate/backup

---

## 🎯 Kết luận

**HRMS Desktop** là giải pháp hoàn hảo khi bạn cần:
- ✅ Ứng dụng offline 100%
- ✅ Giao diện desktop native
- ✅ Hiệu suất cao không phụ thuộc web
- ✅ Triển khai dễ dàng với file .exe
- ✅ Toàn bộ chức năng quản lý nhân sự

**🚀 Sẵn sàng trải nghiệm HRMS Desktop ngay hôm nay!**
