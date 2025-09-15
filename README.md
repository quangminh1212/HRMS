# Hệ thống Quản lý Nhân sự (HRMS)

## 📋 Giới thiệu
Hệ thống quản lý nhân sự toàn diện cho các cơ quan, đơn vị hành chính nhà nước Việt Nam. Phần mềm được thiết kế để quản lý thông tin nhân sự, theo dõi quá trình công tác, nâng lương, nghỉ hưu, quy hoạch cán bộ và các chức năng khác theo quy định pháp luật Việt Nam.

## 🎯 Tính năng chính

### 1. Quản lý Thông tin Nhân sự
- Quản lý thông tin cá nhân đầy đủ (CCCD, ngày sinh, dân tộc, tôn giáo, quê quán)
- Phân loại: Cán bộ, công chức, viên chức, người lao động
- Quản lý trình độ học vấn, chứng chỉ, ngoại ngữ, tin học
- Theo dõi quá trình công tác
- Xuất báo cáo theo mẫu Word/Excel

### 2. Quản lý Lương và Nâng lương
- Tính toán tự động thời gian nâng lương định kỳ (24-36 tháng)
- Cảnh báo danh sách cán bộ đến kỳ nâng lương
- Xử lý các trường hợp đặc biệt (kỷ luật, nghỉ không lương)
- Nâng lương trước thời hạn cho thành tích xuất sắc
- Quản lý phụ cấp chức vụ, phụ cấp thâm niên

### 3. Quản lý Nghỉ hưu
- Tính toán tuổi nghỉ hưu theo lộ trình (nam 62 tuổi, nữ 60 tuổi)
- Cảnh báo tự động 6 tháng trước nghỉ hưu
- Kiểm tra điều kiện khen thưởng cống hiến
- Kiểm tra điều kiện nâng lương lần cuối trước nghỉ hưu

### 4. Quy hoạch Cán bộ
- Kiểm tra điều kiện tuổi quy hoạch
- Quản lý tối đa 3 vị trí quy hoạch/người
- Theo dõi quá trình vào/ra quy hoạch
- Kiểm tra điều kiện bổ nhiệm

### 5. Hợp đồng Lao động
- Quản lý các loại hợp đồng (thử việc, xác định/không xác định thời hạn)
- Cảnh báo hết hạn hợp đồng
- Tự động gia hạn hợp đồng

### 6. Khen thưởng và Kỷ luật
- Theo dõi danh hiệu thi đua hàng năm
- Quản lý Bằng khen, Huân chương các hạng
- Tính toán điều kiện theo Luật Thi đua Khen thưởng 2022
- Quản lý hình thức kỷ luật

### 7. Bảo hiểm Xã hội
- Quản lý số sổ BHXH
- Báo cáo điều chỉnh lương, phụ cấp
- Theo dõi chế độ thai sản, ốm đau

### 8. Báo cáo và Thống kê
- Dashboard tổng quan với biểu đồ real-time
- Báo cáo cơ cấu nhân sự
- Dự báo nâng lương, nghỉ hưu
- Export báo cáo theo mẫu cơ quan nhà nước

## 🛠️ Công nghệ sử dụng

### Backend
- **Python 3.11+** - Ngôn ngữ lập trình chính
- **FastAPI** - Web framework hiệu năng cao
- **PostgreSQL** - Cơ sở dữ liệu quan hệ
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Celery** - Task queue cho background jobs
- **Redis** - Caching và message broker

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Material-UI** - Component library
- **Redux Toolkit** - State management
- **React Query** - Server state management
- **React Hook Form** - Form handling
- **Chart.js** - Data visualization

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD
- **Let's Encrypt** - SSL certificates

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker & Docker Compose (optional)

### Cài đặt môi trường phát triển

1. Clone repository:
```bash
git clone https://github.com/your-org/hrms.git
cd hrms
```

2. Cài đặt backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Cài đặt frontend:
```bash
cd frontend
npm install
```

4. Cấu hình database:
```bash
# Tạo database PostgreSQL
createdb hrms_db

# Chạy migrations
cd backend
alembic upgrade head
```

5. Chạy ứng dụng:

Backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm start
```

### Sử dụng Docker

```bash
docker-compose up -d
```

## 📝 Cấu hình

Tạo file `.env` trong thư mục backend:

```env
DATABASE_URL=postgresql://user:password@localhost/hrms_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379

# Email configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_PATH=./uploads
```

## 🔒 Bảo mật

- JWT authentication với refresh tokens
- Role-based access control (RBAC)
- Mã hóa dữ liệu nhạy cảm
- Audit logs cho mọi thao tác
- Two-factor authentication (2FA)
- Regular security audits

## 📚 Tài liệu

- [API Documentation](docs/api.md)
- [User Manual](docs/user-manual.md)
- [Developer Guide](docs/developer-guide.md)
- [Database Schema](docs/database-schema.md)

## 🤝 Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết chi tiết về quy trình đóng góp.

## 📄 License

Dự án này được cấp phép theo [MIT License](LICENSE).

## 👥 Đội ngũ phát triển

- **Project Manager**: [Name]
- **Backend Developer**: [Name]
- **Frontend Developer**: [Name]
- **UI/UX Designer**: [Name]
- **QA Engineer**: [Name]

## 📞 Liên hệ

- Email: support@hrms.vn
- Phone: (+84) xxx xxx xxx
- Website: https://hrms.vn

## 🚀 Roadmap

### Phase 1 (Q1 2025)
- ✅ Core HR management features
- ✅ Salary calculation and tracking
- ✅ Basic reporting

### Phase 2 (Q2 2025)
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with government systems

### Phase 3 (Q3 2025)
- [ ] AI-powered insights
- [ ] Predictive analytics
- [ ] Voice assistant integration

## 📊 Project Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)