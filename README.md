# HRMS - Hệ thống Quản lý Nhân sự

## Giới thiệu
HRMS (Human Resource Management System) là hệ thống quản lý nhân sự toàn diện được phát triển bằng Python Flask.

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

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Windows 10/11

### Các bước cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```bash
python app.py
```

3. Truy cập hệ thống:
- Mở trình duyệt và truy cập: http://localhost:5000
- Đăng nhập với tài khoản mặc định:
  - Username: admin
  - Password: admin123

## Cấu trúc dự án

```
HRMS/
├── app.py              # File chính của ứng dụng
├── models.py           # Database models
├── utils.py            # Các hàm tiện ích
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── employees.html
│   └── ...
├── static/            # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── exports/           # Thư mục xuất file
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

## Bảo mật
- Mật khẩu được mã hóa
- Phân quyền người dùng (admin, manager, user)
- Session timeout sau 30 phút không hoạt động

## Hỗ trợ
Nếu gặp vấn đề khi sử dụng, vui lòng kiểm tra:
1. Python đã được cài đặt đúng phiên bản
2. Tất cả dependencies đã được cài đặt
3. Port 5000 không bị chiếm bởi ứng dụng khác

## License
© 2024 HRMS - Hệ thống Quản lý Nhân sự
