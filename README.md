# 🏢 HRMS - Hệ thống Quản lý Nhân sự Hiện đại

**🎯 100% Python với bộ sưu tập giao diện hiện đại**

Hệ thống quản lý nhân sự toàn diện với **4 framework UI khác nhau**, từ Material Design 3 đến Flutter components.

---

## 🚀 Quick Start

### **Cách 1: Setup & Run (Khuyến nghị)**
```bash
# Cài đặt
setup.bat

# Chạy với menu chọn framework  
run.bat

# Hoặc chạy nhanh HRMS Modern
quick-start.bat

# Duy trì localhost tự động (khuyến nghị)
keep-alive.bat
```

### **Cách 2: Python trực tiếp**
```bash
# Launcher (khuyến nghị)
python launcher.py

# HRMS Modern (đẹp nhất)  
python run.py

# Các phiên bản khác
python run_classic.py      # Classic
python run_flet.py         # Flutter UI  
python run_nicegui.py      # Tailwind CSS
```

### **🔑 Login Info**
- **Username**: `admin`
- **Password**: `admin123`

---

## 💎 Framework Collection

### **1. HRMS Modern** (🔥 MỚI NHẤT)
- **🎨 Design**: Material Design 3 system  
- **🌐 Port**: 3000
- **✨ Tính năng**: Component library, Design tokens, Glassmorphism
- **📱 UI**: Hero headers, Metric cards, Interactive charts

### **2. Streamlit Classic** 
- **🎨 Design**: Enhanced Streamlit với CSS hiện đại
- **🌐 Port**: 3000  
- **✨ Tính năng**: Glassmorphism effects, Gradient backgrounds
- **📱 UI**: Responsive layout, Smooth animations

### **3. Flet (Flutter for Python)**
- **🎨 Design**: Material Design components
- **🌐 Port**: 8080
- **✨ Tính năng**: Cross-platform, Native feel
- **📱 UI**: Flutter widgets, Smooth transitions

### **4. NiceGUI**  
- **🎨 Design**: Tailwind CSS tích hợp
- **🌐 Port**: 8090
- **✨ Tính năng**: Real-time updates, Vue.js-like
- **📱 UI**: Modern web components, Responsive

---

## 🎯 Tính năng chính

### ✅ **Hoàn thành (HRMS Modern)**
1. **🏠 Dashboard** - Metrics, charts, cảnh báo hiện đại  
2. **👥 Tra cứu nhân sự** - Search, tabs, action buttons
3. **💰 Quản lý nâng lương** - Timeline, filters, export
4. **⏰ Theo dõi nghỉ hưu** - Priority alerts, notifications
5. **📊 Báo cáo thống kê** - Interactive charts, insights

### 🚧 **Đang phát triển**
6. **📋 Quy hoạch cán bộ** (+ AI evaluation)
7. **💼 Quá trình công tác** (+ Interactive timeline)  
8. **📄 Hợp đồng lao động** (+ Digital management)
9. **✅ Điều kiện bổ nhiệm** (+ Auto checking)
10. **🏆 Khen thưởng** (+ Smart evaluation)
11. **⚡ Nâng lương trước hạn** (+ Workflow)
12. **🏥 Báo bảo hiểm** (+ API integration)

---

## 🛠️ Tech Stack

### **Backend**
- 🐍 **Python 3.8+**
- 📊 **SQLAlchemy** - Database ORM
- 📈 **Pandas** - Data processing
- 📉 **Plotly** - Interactive charts

### **Frontend Frameworks**  
- 🌐 **Streamlit** - Web app framework
- 📱 **Flet** - Flutter for Python
- ✨ **NiceGUI** - Modern web UI
- 🎨 **Custom CSS** - Material Design 3

### **Database**
- 🗄️ **SQLite** - Local database
- 📋 **Models** - Employee, Salary, Contract, etc.

---

## 📁 Cấu trúc Project

```
🏢 HRMS/
├── 💎 Modern UI
│   ├── app.py                  # Main HRMS Modern app
│   ├── design.py               # Design tokens & components  
│   ├── pages.py                # Additional modern pages
│   └── run.py                  # Modern launcher
│
├── 🌐 Multi-Framework
│   ├── app_classic.py          # Classic Streamlit
│   ├── app_flet.py             # Flet version
│   ├── app_nicegui.py          # NiceGUI version
│   └── run_*.py                # Individual launchers
│
├── 🎮 Launchers & Setup
│   ├── launcher.py             # Multi-framework launcher
│   ├── setup.bat               # Windows setup  
│   ├── run.bat                 # Windows run with menu
│   └── quick-start.bat         # Quick HRMS Modern start
│
├── 🗄️ Backend
│   ├── models.py               # Database models
│   ├── utils.py                # Utility functions
│   ├── database.db             # SQLite database
│   └── requirements.txt        # Python dependencies
│
└── 📚 Documentation
    └── README.md               # Complete project guide
```

---

## 📊 Framework Comparison

| Framework | Độ đẹp | Hiệu năng | Dễ dùng | Cross-platform | Ecosystem |
|-----------|--------|-----------|---------|----------------|-----------|
| **HRMS Modern** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Web only | ⭐⭐⭐⭐⭐ |
| **Streamlit Classic** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Web only | ⭐⭐⭐⭐⭐ |
| **Flet** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **NiceGUI** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Web only | ⭐⭐⭐ |

---

## 🎨 Screenshots

### HRMS Modern - Material Design 3
- 🏠 **Dashboard**: Glassmorphism hero + gradient metrics
- 👥 **Employee Search**: Modern tabs + surface containers  
- 💰 **Salary Management**: Interactive timeline + filters
- ⏰ **Retirement Tracking**: Priority alerts + action buttons
- 📊 **Reports**: Plotly charts + insights panel

*📸 Screenshots sẽ được cập nhật trong phiên bản tiếp theo*

---

## ⚙️ Requirements

### **System**
- 🖥️ **Windows 10/11** (Linux/Mac support coming)
- 🐍 **Python 3.8+** 
- 💾 **500MB** disk space
- 🌐 **Modern browser** (Chrome, Edge, Firefox)

### **Python Packages**  
```txt
streamlit>=1.28.1
plotly>=5.17.0
pandas>=2.1.4
sqlalchemy>=2.0.21
python-docx>=1.1.0
flet>=0.21.2
nicegui>=1.4.21
```

---

## 🤝 Contributing

### **Báo lỗi**
1. 🐛 Tạo **GitHub Issue** với label `bug`
2. 📝 Mô tả chi tiết: browser, Python version, steps
3. 📷 Attach screenshots nếu có UI issues

### **Feature Request**  
1. 💡 Tạo **GitHub Issue** với label `enhancement` 
2. 🎯 Mô tả tính năng và use case
3. 🎨 Mockups/wireframes nếu có

### **Development**
1. 🍴 Fork repository
2. 🌿 Create branch: `feature/your-feature-name`
3. 💻 Code với comment tiếng Việt
4. ✅ Test trên multiple frameworks
5. 📤 Create Pull Request

---

## 📈 Roadmap

### **v1.2 (Q1 2025)**
- [ ] 🤖 AI-powered features 
- [ ] 🌙 Dark mode support
- [ ] 📱 Mobile optimization
- [ ] 🔄 Real-time sync

### **v1.3 (Q2 2025)**  
- [ ] 🔐 Advanced authentication
- [ ] 📊 Advanced analytics
- [ ] 🌍 API integrations  
- [ ] 📦 PWA support

### **v2.0 (Q3 2025)**
- [ ] 🚀 FastAPI + React frontend
- [ ] 🏗️ Microservices architecture
- [ ] ☁️ Cloud deployment
- [ ] 📊 Business Intelligence

---

## 📜 License

**MIT License** - Free to use, modify, and distribute

---

## 💬 Support

- 📧 **Email**: support@hrms.vn
- 💬 **Chat**: GitHub Discussions  
- 📚 **Docs**: [README_HRMS_MODERN.md](README_HRMS_MODERN.md)
- 🎥 **Video**: YouTube tutorials coming soon

---

**🎉 Cảm ơn bạn đã sử dụng HRMS! Hãy chạy `quick-start.bat` để trải nghiệm ngay!**

*💎 "Hệ thống quản lý nhân sự Python đẹp nhất Việt Nam" - Built with ❤️*