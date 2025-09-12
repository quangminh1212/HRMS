# HRMS - Hệ thống Quản lý Nhân sự

Hệ thống quản lý nhân sự toàn diện được phát triển bằng Python Flask.

## Tính năng chính

### 1. Quản lý nhân sự
- Tra cứu thông tin nhân sự (150+ người)
- Thêm, sửa, xóa thông tin nhân viên
- Quản lý hồ sơ chi tiết: thông tin cá nhân, công việc, lương, đào tạo, thành tích

### 2. Quản lý lương & phụ cấp
- Theo dõi và cảnh báo nâng lương định kỳ
- Tính toán tự động theo quy định (36 tháng cho Chuyên viên, 24 tháng cho Nhân viên)
- Xuất quyết định nâng lương

### 3. Quản lý nghỉ hưu
- Theo dõi nhân viên sắp nghỉ hưu
- Cảnh báo trước 6 tháng, quyết định trước 3 tháng
- Kiểm tra nâng lương trước thời hạn khi nghỉ hưu

### 4. Các chức năng khác
- Kiểm tra quy hoạch cán bộ
- Quản lý quá trình công tác
- Quản lý hợp đồng lao động
- Kiểm tra điều kiện bổ nhiệm
- Báo cáo thống kê đa dạng
- Xuất file Word, Excel

## Cài đặt và chạy

### Yêu cầu
- Python 3.8 trở lên
- pip

### Các bước thực hiện

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy ứng dụng:**
```bash
python run.py
```

3. **Truy cập hệ thống:**
- Mở trình duyệt: http://localhost:5000
- Đăng nhập:
  - **Tên đăng nhập:** admin
  - **Mật khẩu:** admin123

## Cấu trúc dự án

```
HRMS/
├── app.py              # Ứng dụng Flask chính
├── run.py              # File khởi chạy
├── config.py           # Cấu hình ứng dụng
├── models.py           # Database models
├── utils.py            # Hàm tiện ích
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
├── static/            # CSS, JS files
├── tests/             # Test files
├── exports/           # File xuất ra
└── instance/         # Database file
```

## Testing

Chạy tests:
```bash
python -m pytest tests/
```

## Hướng dẫn sử dụng

### Tra cứu nhân sự
1. Đăng nhập vào hệ thống
2. Chọn menu "Nhân sự" > "Danh sách nhân sự"
3. Sử dụng ô tìm kiếm hoặc bộ lọc để tìm nhân viên
4. Click vào tên nhân viên để xem chi tiết

### Quản lý nâng lương
1. Chọn menu "Lương & Phụ cấp" > "Quản lý nâng lương"
2. Hệ thống tự động liệt kê nhân viên đủ điều kiện
3. Chọn nhân viên cần xử lý
4. Xuất quyết định nâng lương

### Xuất báo cáo
1. Chọn menu "Báo cáo"
2. Chọn loại báo cáo cần xuất
3. Chọn định dạng file (Word/Excel)
4. File sẽ được lưu trong thư mục exports/

## Ghi chú
- Tài khoản mặc định: admin / admin123  
- Database được tạo tự động khi chạy lần đầu
- File export sẽ lưu trong thư mục exports/

---
© 2024 HRMS - Hệ thống Quản lý Nhân sự
