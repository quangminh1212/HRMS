"""
HRMS Desktop Application - Hệ thống Quản lý Nhân sự
Frontend & Backend 100% Python với CustomTkinter GUI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys
from PIL import Image, ImageTk
import threading
import webbrowser

# Microsoft Fluent Design Colors
COLORS = {
    'primary': '#0078d4',      # Microsoft Blue
    'secondary': '#106ebe',     # Darker Blue
    'success': '#107c10',       # Microsoft Green  
    'warning': '#ff8c00',       # Microsoft Orange
    'error': '#d13438',         # Microsoft Red
    'background': '#f3f2f1',    # Microsoft Light Gray
    'surface': '#ffffff',       # White
    'text': '#323130',          # Microsoft Dark Gray
    'text_secondary': '#605e5c' # Microsoft Medium Gray
}

# Import business logic
try:
    from models_streamlit import *
    from utils_streamlit import *
except ImportError:
    print("⚠️ Business logic modules not found. Creating mock data...")

# Microsoft Fluent Design Theme
ctk.set_appearance_mode("light")  # Microsoft uses light theme primarily
ctk.set_default_color_theme("blue")  # Microsoft Blue theme

# Microsoft-style Icons (Text-based for professional look)
ICONS = {
    'home': '🏠',
    'people': '👥', 
    'salary': '💰',
    'time': '⏰',
    'planning': '📋',
    'work': '💼',
    'contract': '📄',
    'check': '✅',
    'award': '🏆',
    'fast': '⚡',
    'chart': '📊',
    'health': '🏥',
    'settings': '⚙️',
    'help': '❓',
    'fullscreen': '⛶',
    'logout': '↪️',
    'search': '🔍',
    'export': '📤',
    'info': 'ℹ️'
}

# Help texts for each function (Microsoft-style helpful descriptions)
HELP_TEXTS = {
    'home': 'Xem tổng quan thống kê và hoạt động gần đây của hệ thống',
    'employee_search': 'Tìm kiếm và xem chi tiết thông tin của nhân viên theo tên hoặc mã',
    'salary_mgmt': 'Quản lý nâng lương định kỳ theo quy định 36/24 tháng và phụ cấp thâm niên',
    'retirement': 'Theo dõi nghỉ hưu, cảnh báo trước 6 tháng và xử lý nâng lương trước hạn',
    'planning': 'Kiểm tra quy hoạch cán bộ theo độ tuổi và quota từng vị trí',
    'work_history': 'Quản lý timeline quá trình công tác, thêm/sửa/xóa các giai đoạn',
    'contracts': 'Quản lý hợp đồng lao động cho Ban kiểm soát và nhân viên, cảnh báo hết hạn',
    'appointment': 'Kiểm tra đầy đủ điều kiện bổ nhiệm và cảnh báo bổ nhiệm lại sau 90 ngày',
    'awards': 'Xem điều kiện khen thưởng và đánh giá các tiêu chí cần thiết',
    'early_salary': 'Quản lý nâng lương trước thời hạn do lập thành tích xuất sắc',
    'reports': 'Xem báo cáo thống kê toàn diện và phân tích cơ cấu nhân sự',
    'insurance': 'Nhắc nhở và xuất Excel báo cáo bảo hiểm xã hội'
}

class HRMSDesktop:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Microsoft HRMS - Human Resource Management System")
        
        # Set larger default size and make fully resizable
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Start with 90% of screen size
        start_width = int(screen_width * 0.9)
        start_height = int(screen_height * 0.9)
        
        self.root.geometry(f"{start_width}x{start_height}")
        self.root.resizable(True, True)
        
        # Enable maximize button and fullscreen capability
        self.root.state('normal')  # Allow maximize
        self.is_fullscreen = False
        
        # Bind F11 for fullscreen toggle
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Center window
        self.center_window()
        
        # Initialize database
        self.init_database()
        
        # Session state
        self.current_user = None
        self.is_logged_in = False
        self.show_help = True  # Microsoft-style contextual help
        
        # Tooltip system for Microsoft-style guidance
        self.current_tooltip = None
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show login screen
        self.show_login_screen()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-fullscreen", False)
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)
    
    def init_database(self):
        """Initialize SQLite database"""
        try:
            self.conn = sqlite3.connect('hrms_desktop.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Create tables if not exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_code TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    birth_date DATE,
                    gender TEXT,
                    ethnicity TEXT DEFAULT 'Kinh',
                    religion TEXT DEFAULT 'Không',
                    hometown TEXT,
                    position TEXT,
                    department TEXT,
                    party_date DATE,
                    political_theory TEXT,
                    education_level TEXT,
                    major TEXT,
                    institution TEXT,
                    current_salary REAL,
                    salary_grade TEXT,
                    phone TEXT,
                    email TEXT,
                    start_date DATE,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert default admin user
            try:
                self.cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    ("admin", "admin123")
                )
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass  # User already exists
                
            # Insert sample employees if none exist
            self.cursor.execute("SELECT COUNT(*) FROM employees")
            if self.cursor.fetchone()[0] == 0:
                self.insert_sample_data()
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Lỗi kết nối database: {str(e)}")
    
    def insert_sample_data(self):
        """Insert sample employee data"""
        sample_employees = [
            ("NV001", "Nguyễn Văn A", "1985-06-15", "Nam", "Kinh", "Không", "Hà Nội", 
             "Chuyên viên chính", "Phòng TCHC", "2010-05-10", "Trung cấp", "Thạc sĩ Luật", 
             "Luật", "ĐH Luật Hà Nội", 7320000, "A2/3.45", "0901234567", "nguyenvana@company.vn", "2008-08-01"),
            ("NV002", "Trần Thị B", "1990-03-20", "Nữ", "Kinh", "Không", "Hà Nội",
             "Chuyên viên", "Phòng TCKT", "2015-08-15", "Sơ cấp", "Cử nhân Tài chính",
             "Tài chính", "ĐH Kinh tế Quốc dân", 5781000, "A1/2.67", "0907654321", "tranthib@company.vn", "2012-03-01"),
            ("NV003", "Lê Văn C", "1978-12-10", "Nam", "Kinh", "Phật giáo", "Hải Phòng",
             "Trưởng phòng", "Phòng Kinh doanh", "2005-01-20", "Cao cấp", "Cử nhân Kinh tế",
             "Kinh tế", "ĐH Thương mại", 9200000, "A3/4.2", "0912345678", "levanc@company.vn", "2000-06-01")
        ]
        
        for emp in sample_employees:
            try:
                self.cursor.execute('''
                    INSERT INTO employees (employee_code, full_name, birth_date, gender, ethnicity, 
                    religion, hometown, position, department, party_date, political_theory, 
                    education_level, major, institution, current_salary, salary_grade, phone, email, start_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', emp)
            except sqlite3.IntegrityError:
                pass  # Employee already exists
                
        self.conn.commit()
        
    def show_login_screen(self):
        """Show Microsoft-style login interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Main login container
        login_container = ctk.CTkFrame(self.main_container, fg_color=COLORS['surface'])
        login_container.pack(fill="both", expand=True)
        
        # Left panel - Welcome & Branding
        left_panel = ctk.CTkFrame(login_container, width=600, fg_color=COLORS['primary'])
        left_panel.pack(side="left", fill="y", padx=20, pady=20)
        left_panel.pack_propagate(False)
        
        # Microsoft-style welcome
        welcome_title = ctk.CTkLabel(left_panel, text="Chào mừng đến với", 
                                   font=ctk.CTkFont(size=18), text_color="white")
        welcome_title.pack(pady=(50, 10))
        
        app_title = ctk.CTkLabel(left_panel, text="Microsoft HRMS", 
                               font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        app_title.pack(pady=10)
        
        app_subtitle = ctk.CTkLabel(left_panel, text="Human Resource Management System", 
                                  font=ctk.CTkFont(size=16), text_color="white")
        app_subtitle.pack(pady=5)
        
        description = ctk.CTkLabel(left_panel, 
                                 text="Hệ thống quản lý nhân sự hiện đại\nvới giao diện Microsoft Fluent Design\n\n"
                                      "✓ Quản lý thông tin nhân viên\n"
                                      "✓ Theo dõi nâng lương định kỳ\n"
                                      "✓ Báo cáo và thống kê\n"
                                      "✓ Giao diện thân thiện, dễ sử dụng",
                                 font=ctk.CTkFont(size=13), text_color="white",
                                 justify="left")
        description.pack(pady=30, padx=40)
        
        # Right panel - Login form
        right_panel = ctk.CTkFrame(login_container, fg_color=COLORS['surface'])
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Login form container
        login_frame = ctk.CTkFrame(right_panel, width=400)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Login header
        login_header = ctk.CTkLabel(login_frame, text="Đăng nhập vào tài khoản", 
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=COLORS['text'])
        login_header.pack(pady=(30, 20))
        
        help_text = ctk.CTkLabel(login_frame, text="Nhập thông tin đăng nhập để tiếp tục", 
                               font=ctk.CTkFont(size=12),
                               text_color=COLORS['text_secondary'])
        help_text.pack(pady=(0, 30))
        
        # Username field with Microsoft-style labeling
        username_label = ctk.CTkLabel(login_frame, text="Tên đăng nhập", 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color=COLORS['text'])
        username_label.pack(anchor="w", padx=50, pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Nhập tên đăng nhập", 
                                         width=300, height=35,
                                         font=ctk.CTkFont(size=13))
        self.username_entry.pack(pady=(0, 20), padx=50)
        self.username_entry.insert(0, "admin")  # Default username
        
        # Password field
        password_label = ctk.CTkLabel(login_frame, text="Mật khẩu", 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color=COLORS['text'])
        password_label.pack(anchor="w", padx=50, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Nhập mật khẩu", 
                                         show="*", width=300, height=35,
                                         font=ctk.CTkFont(size=13))
        self.password_entry.pack(pady=(0, 30), padx=50)
        self.password_entry.insert(0, "admin123")  # Default password
        
        # Login button - Microsoft style
        login_btn = ctk.CTkButton(login_frame, text="Đăng nhập", 
                                command=self.handle_login, width=300, height=45,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color=COLORS['primary'], hover_color=COLORS['secondary'])
        login_btn.pack(pady=(0, 20), padx=50)
        
        # Demo credentials info with Microsoft styling
        demo_frame = ctk.CTkFrame(login_frame, fg_color=COLORS['background'], corner_radius=8)
        demo_frame.pack(fill="x", padx=50, pady=20)
        
        demo_title = ctk.CTkLabel(demo_frame, text="Tài khoản demo",
                                font=ctk.CTkFont(size=11, weight="bold"),
                                text_color=COLORS['text'])
        demo_title.pack(pady=(10, 5))
        
        credentials = ctk.CTkLabel(demo_frame, 
                                 text="Tên đăng nhập: admin\nMật khẩu: admin123",
                                 font=ctk.CTkFont(size=10),
                                 text_color=COLORS['text_secondary'])
        credentials.pack(pady=(0, 10))
        
        # Help section - Microsoft style
        help_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        help_frame.pack(fill="x", padx=50, pady=10)
        
        help_icon = ctk.CTkLabel(help_frame, text=ICONS['help'], font=ctk.CTkFont(size=12))
        help_icon.pack(side="left")
        
        help_text = ctk.CTkLabel(help_frame, 
                               text="F11: Toàn màn hình | ESC: Thoát | Enter: Đăng nhập",
                               font=ctk.CTkFont(size=9),
                               text_color=COLORS['text_secondary'])
        help_text.pack(side="left", padx=(5, 0))
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
    def handle_login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        # Check credentials
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                          (username, password))
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = username
            self.is_logged_in = True
            self.show_dashboard()
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    def show_dashboard(self):
        """Show main dashboard"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Create header
        self.create_header()
        
        # Create main content area
        content_frame = ctk.CTkFrame(self.main_container)
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Create sidebar navigation
        self.create_sidebar(content_frame)
        
        # Create main content
        self.main_content = ctk.CTkFrame(content_frame)
        self.main_content.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Show initial dashboard content
        self.show_home_dashboard()
    
    def create_header(self):
        """Create Microsoft-style header with user info and controls"""
        header = ctk.CTkFrame(self.main_container, height=70, fg_color=COLORS['surface'])
        header.pack(fill="x", pady=(0, 10))
        
        # Left side - App branding and user welcome
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=15)
        
        app_name = ctk.CTkLabel(left_frame, text="Microsoft HRMS", 
                              font=ctk.CTkFont(size=16, weight="bold"),
                              text_color=COLORS['primary'])
        app_name.pack(side="left")
        
        separator = ctk.CTkLabel(left_frame, text="•", 
                               font=ctk.CTkFont(size=14),
                               text_color=COLORS['text_secondary'])
        separator.pack(side="left", padx=10)
        
        welcome = ctk.CTkLabel(left_frame, text=f"Xin chào, {self.current_user}", 
                             font=ctk.CTkFont(size=14),
                             text_color=COLORS['text'])
        welcome.pack(side="left")
        
        # Right side - Controls with Microsoft styling
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=15)
        
        # Help toggle button
        help_btn = ctk.CTkButton(controls_frame, text=f"{ICONS['help']} Trợ giúp", 
                               command=self.toggle_help, width=100, height=30,
                               font=ctk.CTkFont(size=11),
                               fg_color="transparent", 
                               text_color=COLORS['primary'],
                               hover_color=COLORS['background'])
        help_btn.pack(side="left", padx=(0, 10))
        
        # Fullscreen button - Microsoft style
        fullscreen_btn = ctk.CTkButton(controls_frame, text=f"{ICONS['fullscreen']} Toàn màn hình", 
                                     command=self.toggle_fullscreen, width=130, height=30,
                                     font=ctk.CTkFont(size=11),
                                     fg_color=COLORS['background'], 
                                     text_color=COLORS['text'],
                                     hover_color=COLORS['primary'])
        fullscreen_btn.pack(side="left", padx=(0, 10))
        
        # Logout button - Microsoft style
        logout_btn = ctk.CTkButton(controls_frame, text=f"{ICONS['logout']} Đăng xuất", 
                                 command=self.handle_logout, width=110, height=30,
                                 font=ctk.CTkFont(size=11),
                                 fg_color=COLORS['error'], 
                                 hover_color="#b91c1c")
        logout_btn.pack(side="left")
        
    def create_sidebar(self, parent):
        """Create navigation sidebar with scrollable content"""
        sidebar = ctk.CTkFrame(parent, width=300)  # Slightly wider
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Navigation title
        nav_title = ctk.CTkLabel(sidebar, text="🧭 Chức năng chính", 
                               font=ctk.CTkFont(size=16, weight="bold"))
        nav_title.pack(pady=20)
        
        # Create scrollable frame for navigation buttons
        nav_scroll = ctk.CTkScrollableFrame(sidebar, width=260, height=600)
        nav_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Trang chủ", self.show_home_dashboard),
            ("👥 Tra cứu nhân sự", self.show_employee_search),
            ("💰 Nâng lương định kỳ", self.show_salary_management),
            ("⏰ Theo dõi nghỉ hưu", self.show_retirement_tracking),
            ("📋 Kiểm tra quy hoạch", self.show_planning_check),
            ("💼 Quá trình công tác", self.show_work_history),
            ("📄 Hợp đồng lao động", self.show_contracts),
            ("✅ Điều kiện bổ nhiệm", self.show_appointment_check),
            ("🏆 Điều kiện khen thưởng", self.show_award_check),
            ("⚡ Nâng lương trước hạn", self.show_early_salary),
            ("📊 Báo cáo thống kê", self.show_reports),
            ("🏥 Báo bảo hiểm", self.show_insurance)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(nav_scroll, text=text, command=command, 
                              width=240, height=40, anchor="w",
                              font=ctk.CTkFont(size=12, weight="bold"))
            btn.pack(pady=8, padx=10, fill="x")
    
    def show_home_dashboard(self):
        """Show home dashboard with statistics"""
        self.clear_main_content()
        
        # Title
        title = ctk.CTkLabel(self.main_content, text="🏠 Bảng điều khiển HRMS", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(self.main_content)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Get statistics from database
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'active'")
        total_employees = self.cursor.fetchone()[0]
        
        # Create statistics cards with better responsive layout
        stats = [
            ("👥 Tổng nhân sự", str(total_employees), "green"),
            ("⏰ Sắp nghỉ hưu", "12", "orange"),
            ("💰 Đến kỳ nâng lương", "25", "blue"),
            ("📄 Hợp đồng hết hạn", "6", "red"),
            ("🏆 Khen thưởng tháng", "8", "purple"),
            ("📋 Quy hoạch hết hạn", "15", "brown")
        ]
        
        # Create 2 rows of cards for better use of space
        for i, (label, value, color) in enumerate(stats):
            row = i // 3  # 3 cards per row
            col = i % 3
            
            card = ctk.CTkFrame(stats_frame, height=120)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
            
            value_label = ctk.CTkLabel(card, text=value, 
                                     font=ctk.CTkFont(size=36, weight="bold"))
            value_label.pack(pady=15)
            
            label_label = ctk.CTkLabel(card, text=label, 
                                     font=ctk.CTkFont(size=13, weight="bold"))
            label_label.pack(pady=5)
        
        # Configure grid weights for responsive layout
        for i in range(3):  # 3 columns
            stats_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):  # 2 rows
            stats_frame.grid_rowconfigure(i, weight=1)
        
        # Recent activities
        activities_frame = ctk.CTkFrame(self.main_content)
        activities_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        activities_title = ctk.CTkLabel(activities_frame, text="📋 Hoạt động gần đây", 
                                      font=ctk.CTkFont(size=18, weight="bold"))
        activities_title.pack(pady=15)
        
        # Activities list
        activities = [
            "💰 Nguyễn Văn A - Nâng lương từ A2/3.2 lên A2/3.45",
            "⏰ Trần Thị B - Cảnh báo nghỉ hưu trong 6 tháng",
            "📄 Lê Văn C - Gia hạn hợp đồng thành công",
            "✅ Phạm Thị D - Đủ điều kiện bổ nhiệm Phó Trưởng phòng",
            "🏆 Hoàng Văn E - Đạt danh hiệu Lao động tiên tiến"
        ]
        
        for activity in activities:
            activity_label = ctk.CTkLabel(activities_frame, text=activity, 
                                        font=ctk.CTkFont(size=11), anchor="w")
            activity_label.pack(fill="x", padx=20, pady=5)
    
    def clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_employee_search(self):
        """Show employee search interface"""
        self.clear_main_content()
        
        # Title
        title = ctk.CTkLabel(self.main_content, text="👥 Tra cứu thông tin nhân sự", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Search frame
        search_frame = ctk.CTkFrame(self.main_content)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍 Nhập tên nhân viên cần tìm:")
        search_label.pack(pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="VD: Nguyễn Văn A")
        self.search_entry.pack(pady=5)
        
        search_btn = ctk.CTkButton(search_frame, text="🔍 Tìm kiếm", 
                                 command=self.search_employee)
        search_btn.pack(pady=10)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_content)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self.search_employee())
    
    def search_employee(self):
        """Search for employee"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên cần tìm!")
            return
            
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Search in database
        self.cursor.execute('''
            SELECT * FROM employees 
            WHERE full_name LIKE ? OR employee_code LIKE ?
            ORDER BY full_name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        results = self.cursor.fetchall()
        
        if not results:
            no_result = ctk.CTkLabel(self.results_frame, text="❌ Không tìm thấy nhân viên phù hợp", 
                                   font=ctk.CTkFont(size=14))
            no_result.pack(pady=20)
            return
        
        # Show results
        for emp in results:
            self.display_employee_result(emp)
    
    def display_employee_result(self, employee):
        """Display employee search result"""
        emp_frame = ctk.CTkFrame(self.results_frame)
        emp_frame.pack(fill="x", padx=10, pady=10)
        
        # Employee info
        info_text = f"✅ {employee[2]} ({employee[1]})\n📍 {employee[8]} - {employee[9]}\n📞 {employee[17]} | 📧 {employee[18]}"
        
        info_label = ctk.CTkLabel(emp_frame, text=info_text, 
                                font=ctk.CTkFont(size=12), justify="left")
        info_label.pack(side="left", padx=15, pady=15)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(emp_frame)
        btn_frame.pack(side="right", padx=15, pady=10)
        
        detail_btn = ctk.CTkButton(btn_frame, text="📋 Chi tiết", width=100,
                                 command=lambda: self.show_employee_detail(employee))
        detail_btn.pack(pady=5)
        
        export_btn = ctk.CTkButton(btn_frame, text="📄 Xuất Word", width=100,
                                 command=lambda: self.export_employee_word(employee))
        export_btn.pack(pady=5)
    
    def show_employee_detail(self, employee):
        """Show detailed employee information"""
        # Create new window for employee details
        detail_window = ctk.CTkToplevel(self.root)
        detail_window.title(f"Chi tiết nhân viên - {employee[2]}")
        detail_window.geometry("800x600")
        
        # Employee details content
        content = ctk.CTkScrollableFrame(detail_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(content, text=f"👤 {employee[2]}", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)
        
        # Personal info
        personal_frame = ctk.CTkFrame(content)
        personal_frame.pack(fill="x", pady=10)
        
        personal_title = ctk.CTkLabel(personal_frame, text="📋 Thông tin cá nhân", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        personal_title.pack(pady=10)
        
        personal_info = f"""
        Mã nhân viên: {employee[1]}
        Họ tên: {employee[2]}
        Ngày sinh: {employee[3]}
        Giới tính: {employee[4]}
        Dân tộc: {employee[5]}
        Tôn giáo: {employee[6]}
        Quê quán: {employee[7]}
        Điện thoại: {employee[17]}
        Email: {employee[18]}
        """
        
        personal_label = ctk.CTkLabel(personal_frame, text=personal_info, 
                                    font=ctk.CTkFont(size=11), justify="left")
        personal_label.pack(padx=20, pady=10)
        
        # Work info
        work_frame = ctk.CTkFrame(content)
        work_frame.pack(fill="x", pady=10)
        
        work_title = ctk.CTkLabel(work_frame, text="💼 Thông tin công việc", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        work_title.pack(pady=10)
        
        work_info = f"""
        Chức vụ: {employee[8]}
        Đơn vị: {employee[9]}
        Ngày vào Đảng: {employee[10]}
        Trình độ LLCT: {employee[11]}
        Trình độ chuyên môn: {employee[12]} {employee[13]}
        Trường: {employee[14]}
        Lương hiện tại: {employee[15]:,.0f} VNĐ
        Ngạch/Hệ số: {employee[16]}
        Ngày bắt đầu: {employee[19]}
        Trạng thái: {employee[20]}
        """
        
        work_label = ctk.CTkLabel(work_frame, text=work_info, 
                                font=ctk.CTkFont(size=11), justify="left")
        work_label.pack(padx=20, pady=10)
    
    def export_employee_word(self, employee):
        """Export employee info to Word document"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx")],
                initialname=f"ThongTin_{employee[2].replace(' ', '_')}.docx"
            )
            
            if filename:
                # Create simple text document (mock export)
                content = f"""
                THÔNG TIN NHÂN VIÊN
                
                Mã nhân viên: {employee[1]}
                Họ tên: {employee[2]}
                Ngày sinh: {employee[3]}
                Giới tính: {employee[4]}
                Chức vụ: {employee[8]}
                Đơn vị: {employee[9]}
                Lương hiện tại: {employee[15]:,.0f} VNĐ
                
                Xuất ngày: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                """
                
                # Save as text file (in real app would use python-docx)
                with open(filename.replace('.docx', '.txt'), 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("Thành công", f"Đã xuất thông tin nhân viên ra file:\n{filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")
    
    def show_salary_management(self):
        """Show salary management interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="💰 Quản lý nâng lương định kỳ", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Placeholder content
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Lịch cảnh báo theo quý\n"
                                  "• Logic 36/24 tháng\n"
                                  "• Phụ cấp thâm niên 5% + 1%/năm\n"
                                  "• Xuất 3 file Word + Excel",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_retirement_tracking(self):
        """Show retirement tracking interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="⏰ Theo dõi nghỉ hưu", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Cảnh báo 6 tháng (thông báo)\n"
                                  "• Cảnh báo 3 tháng (quyết định)\n"
                                  "• Nâng lương trước thời hạn\n"
                                  "• Xuất Word thông báo & quyết định",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_planning_check(self):
        """Show planning check interface"""  
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="📋 Kiểm tra quy hoạch", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Kiểm tra tuổi trong quy hoạch\n"
                                  "• Quota checking theo vị trí\n"
                                  "• Biểu đồ phân tích\n"
                                  "• Cài đặt giới hạn tuổi",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_work_history(self):
        """Show work history interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="💼 Quá trình công tác", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Timeline view\n"
                                  "• Thêm/Sửa/Xóa giai đoạn\n"
                                  "• Xuất Word/Excel",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_contracts(self):
        """Show contracts interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="📄 Hợp đồng lao động", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Quản lý BKS + nhân viên\n"
                                  "• Cảnh báo hết hạn\n"
                                  "• Gia hạn/Tạo mới",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_appointment_check(self):
        """Show appointment check interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="✅ Điều kiện bổ nhiệm", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Kiểm tra đầy đủ điều kiện\n"
                                  "• Cảnh báo bổ nhiệm lại 90 ngày\n"
                                  "• Thống kê và báo cáo",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_award_check(self):
        """Show award check interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="🏆 Điều kiện khen thưởng", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Kiểm tra tiêu chí khen thưởng\n"
                                  "• Đánh giá đầy đủ điều kiện\n"
                                  "• Đề xuất khen thưởng",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_early_salary(self):
        """Show early salary interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="⚡ Nâng lương trước hạn", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Quản lý đề xuất\n"
                                  "• Phê duyệt thành tích\n"
                                  "• Xuất quyết định",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_reports(self):
        """Show reports interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="📊 Báo cáo thống kê", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Thống kê toàn diện\n"
                                  "• Phân tích thôi việc\n"
                                  "• Cơ cấu nhân sự\n"
                                  "• Charts tương tác",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def show_insurance(self):
        """Show insurance interface"""
        self.clear_main_content()
        
        title = ctk.CTkLabel(self.main_content, text="🏥 Báo bảo hiểm", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        content = ctk.CTkLabel(self.main_content, 
                             text="🔧 Chức năng đang được phát triển...\n\n"
                                  "Sẽ bao gồm:\n"
                                  "• Nhắc nhở BHXH\n"
                                  "• Xuất Excel\n"
                                  "• Quản lý thay đổi",
                             font=ctk.CTkFont(size=14))
        content.pack(expand=True)
    
    def handle_logout(self):
        """Handle user logout"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.current_user = None
            self.is_logged_in = False
            self.show_login_screen()
    
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if hasattr(self, 'conn'):
            self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    try:
        app = HRMSDesktop()
        app.run()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        input("Nhấn Enter để đóng...")
