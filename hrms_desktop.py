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
    
    def toggle_help(self):
        """Toggle help display in Microsoft style"""
        self.show_help = not self.show_help
        # Refresh current view to show/hide help
        if hasattr(self, 'current_function'):
            self.show_function_help(self.current_function)
        else:
            self.show_general_help()
    
    def show_function_help(self, function_key):
        """Show contextual help for current function"""
        if not self.show_help:
            return
            
        help_text = HELP_TEXTS.get(function_key, "Chức năng này đang được phát triển.")
        
        # Create or update help panel
        if hasattr(self, 'help_panel'):
            self.help_panel.destroy()
        
        self.help_panel = ctk.CTkFrame(self.main_content, height=60, fg_color=COLORS['background'])
        self.help_panel.pack(fill="x", pady=(0, 10))
        
        help_icon = ctk.CTkLabel(self.help_panel, text=ICONS['info'], 
                               font=ctk.CTkFont(size=14))
        help_icon.pack(side="left", padx=15, pady=15)
        
        help_label = ctk.CTkLabel(self.help_panel, text=help_text,
                                font=ctk.CTkFont(size=12),
                                text_color=COLORS['text'])
        help_label.pack(side="left", padx=10, pady=15)
    
    def show_general_help(self):
        """Show general help information"""
        if not self.show_help:
            return
            
        general_help = "Chọn một chức năng từ menu bên trái để bắt đầu. Hover vào các nút để xem thông tin chi tiết."
        
        if hasattr(self, 'help_panel'):
            self.help_panel.destroy()
        
        self.help_panel = ctk.CTkFrame(self.main_content, height=60, fg_color=COLORS['background'])
        self.help_panel.pack(fill="x", pady=(0, 10))
        
        help_icon = ctk.CTkLabel(self.help_panel, text=ICONS['info'], 
                               font=ctk.CTkFont(size=14))
        help_icon.pack(side="left", padx=15, pady=15)
        
        help_label = ctk.CTkLabel(self.help_panel, text=general_help,
                                font=ctk.CTkFont(size=12),
                                text_color=COLORS['text'])
        help_label.pack(side="left", padx=10, pady=15)
    
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
        """Create Microsoft-style navigation sidebar"""
        sidebar = ctk.CTkFrame(parent, width=320, fg_color=COLORS['surface'])
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Sidebar header with Microsoft styling
        header_frame = ctk.CTkFrame(sidebar, height=80, fg_color=COLORS['primary'])
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        nav_title = ctk.CTkLabel(header_frame, text="Chức năng chính", 
                               font=ctk.CTkFont(size=18, weight="bold"),
                               text_color="white")
        nav_title.pack(pady=20)
        
        # Create scrollable frame for navigation buttons
        nav_scroll = ctk.CTkScrollableFrame(sidebar, width=280, height=600,
                                          fg_color="transparent")
        nav_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Navigation buttons with Microsoft-style icons and help text
        nav_items = [
            ("home", "Trang chủ", self.show_home_dashboard, 'home'),
            ("people", "Tra cứu nhân sự", self.show_employee_search, 'employee_search'),
            ("salary", "Nâng lương định kỳ", self.show_salary_management, 'salary_mgmt'),
            ("time", "Theo dõi nghỉ hưu", self.show_retirement_tracking, 'retirement'),
            ("planning", "Kiểm tra quy hoạch", self.show_planning_check, 'planning'),
            ("work", "Quá trình công tác", self.show_work_history, 'work_history'),
            ("contract", "Hợp đồng lao động", self.show_contracts, 'contracts'),
            ("check", "Điều kiện bổ nhiệm", self.show_appointment_check, 'appointment'),
            ("award", "Điều kiện khen thưởng", self.show_award_check, 'awards'),
            ("fast", "Nâng lương trước hạn", self.show_early_salary, 'early_salary'),
            ("chart", "Báo cáo thống kê", self.show_reports, 'reports'),
            ("health", "Báo bảo hiểm", self.show_insurance, 'insurance')
        ]
        
        for icon_key, text, command, help_key in nav_items:
            # Create button frame for better control
            btn_frame = ctk.CTkFrame(nav_scroll, fg_color="transparent")
            btn_frame.pack(fill="x", pady=4, padx=5)
            
            # Main navigation button with Microsoft styling
            btn = ctk.CTkButton(btn_frame, 
                              text=f"{ICONS[icon_key]}  {text}", 
                              command=lambda c=command, h=help_key: self.nav_click(c, h),
                              width=260, height=45, anchor="w",
                              font=ctk.CTkFont(size=13),
                              fg_color="transparent",
                              text_color=COLORS['text'],
                              hover_color=COLORS['background'])
            btn.pack(fill="x")
            
            # Add hover tooltip (Microsoft-style help)
            self.create_tooltip(btn, HELP_TEXTS.get(help_key, ""))
    
    def nav_click(self, command, help_key):
        """Handle navigation click with help context"""
        self.current_function = help_key
        command()  # Execute the navigation command
        self.show_function_help(help_key)  # Show contextual help
    
    def create_tooltip(self, widget, text):
        """Create Microsoft-style tooltip for widget"""
        def on_enter(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                
            self.tooltip = ctk.CTkToplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.configure(fg_color=COLORS['text'])
            
            label = ctk.CTkLabel(self.tooltip, text=text,
                               font=ctk.CTkFont(size=10),
                               text_color="white",
                               fg_color=COLORS['text'])
            label.pack(padx=8, pady=4)
            
            # Position tooltip
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() - 30
            self.tooltip.geometry(f"+{x}+{y}")
        
        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def show_home_dashboard(self):
        """Show Microsoft-style home dashboard"""
        self.clear_main_content()
        
        # Welcome section with Microsoft styling
        welcome_frame = ctk.CTkFrame(self.main_content, height=100, fg_color=COLORS['surface'])
        welcome_frame.pack(fill="x", padx=20, pady=20)
        welcome_frame.pack_propagate(False)
        
        # Welcome content
        welcome_content = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        welcome_content.pack(expand=True, fill="both", padx=30, pady=20)
        
        welcome_title = ctk.CTkLabel(welcome_content, text="Bảng điều khiển", 
                                   font=ctk.CTkFont(size=28, weight="bold"),
                                   text_color=COLORS['text'])
        welcome_title.pack(anchor="w")
        
        welcome_subtitle = ctk.CTkLabel(welcome_content, 
                                      text=f"Chào mừng trở lại, {self.current_user}. Đây là tổng quan về hệ thống HRMS của bạn.",
                                      font=ctk.CTkFont(size=14),
                                      text_color=COLORS['text_secondary'])
        welcome_subtitle.pack(anchor="w", pady=(5, 0))
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(self.main_content)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Get statistics from database
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'active'")
        total_employees = self.cursor.fetchone()[0]
        
        # Microsoft-style statistics cards
        stats_data = [
            ("Tổng nhân sự", str(total_employees), COLORS['primary'], "people"),
            ("Sắp nghỉ hưu", "12", COLORS['warning'], "time"), 
            ("Đến kỳ nâng lương", "25", COLORS['success'], "salary"),
            ("Hợp đồng hết hạn", "6", COLORS['error'], "contract"),
            ("Khen thưởng tháng", "8", "#8b5cf6", "award"),
            ("Quy hoạch hết hạn", "15", "#f59e0b", "planning")
        ]
        
        # Create Microsoft-style cards in 2 rows x 3 columns
        for i, (label, value, color, icon_key) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            # Card container with Microsoft Fluent Design
            card = ctk.CTkFrame(stats_frame, height=140, fg_color=COLORS['surface'],
                              border_width=1, border_color=COLORS['background'])
            card.grid(row=row, column=col, padx=12, pady=12, sticky="ew")
            
            # Card header with icon and color accent
            card_header = ctk.CTkFrame(card, height=40, fg_color=color)
            card_header.pack(fill="x", padx=0, pady=0)
            card_header.pack_propagate(False)
            
            icon = ctk.CTkLabel(card_header, text=ICONS[icon_key], 
                              font=ctk.CTkFont(size=18), text_color="white")
            icon.pack(side="left", padx=15, pady=10)
            
            # Card content
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=20, pady=15)
            
            value_label = ctk.CTkLabel(content_frame, text=value,
                                     font=ctk.CTkFont(size=32, weight="bold"),
                                     text_color=COLORS['text'])
            value_label.pack(anchor="w")
            
            label_label = ctk.CTkLabel(content_frame, text=label,
                                     font=ctk.CTkFont(size=12),
                                     text_color=COLORS['text_secondary'])
            label_label.pack(anchor="w", pady=(5, 0))
        
        # Configure grid for responsive layout
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            stats_frame.grid_rowconfigure(i, weight=1)
        
        # Recent activities with Microsoft styling
        activities_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS['surface'])
        activities_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Activities header
        activities_header = ctk.CTkFrame(activities_frame, height=60, fg_color=COLORS['background'])
        activities_header.pack(fill="x", padx=0, pady=0)
        activities_header.pack_propagate(False)
        
        activities_title = ctk.CTkLabel(activities_header, text="Hoạt động gần đây", 
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color=COLORS['text'])
        activities_title.pack(side="left", padx=20, pady=15)
        
        # View all button
        view_all_btn = ctk.CTkButton(activities_header, text="Xem tất cả",
                                   width=100, height=30,
                                   font=ctk.CTkFont(size=11),
                                   fg_color="transparent",
                                   text_color=COLORS['primary'],
                                   hover_color=COLORS['background'])
        view_all_btn.pack(side="right", padx=20, pady=15)
        
        # Activities content
        activities_content = ctk.CTkScrollableFrame(activities_frame, height=300)
        activities_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Activities list with Microsoft-style items
        activities = [
            ("salary", "Nguyễn Văn A", "Nâng lương từ A2/3.2 lên A2/3.45", "2 giờ trước", COLORS['success']),
            ("time", "Trần Thị B", "Cảnh báo nghỉ hưu trong 6 tháng", "4 giờ trước", COLORS['warning']),
            ("contract", "Lê Văn C", "Gia hạn hợp đồng thành công", "1 ngày trước", COLORS['primary']),
            ("check", "Phạm Thị D", "Đủ điều kiện bổ nhiệm Phó Trưởng phòng", "2 ngày trước", COLORS['success']),
            ("award", "Hoàng Văn E", "Đạt danh hiệu Lao động tiên tiến", "3 ngày trước", "#8b5cf6"),
            ("people", "Nguyễn Thị F", "Nhân viên mới hoàn thành thử việc", "1 tuần trước", COLORS['primary'])
        ]
        
        for icon_key, name, action, time, color in activities:
            # Activity item container
            activity_item = ctk.CTkFrame(activities_content, fg_color=COLORS['surface'],
                                       border_width=1, border_color=COLORS['background'])
            activity_item.pack(fill="x", pady=5, padx=5)
            
            # Activity content
            activity_content = ctk.CTkFrame(activity_item, fg_color="transparent")
            activity_content.pack(fill="x", padx=15, pady=12)
            
            # Icon with colored background
            icon_frame = ctk.CTkFrame(activity_content, width=35, height=35, 
                                    fg_color=color, corner_radius=17)
            icon_frame.pack(side="left", padx=(0, 15))
            icon_frame.pack_propagate(False)
            
            icon = ctk.CTkLabel(icon_frame, text=ICONS[icon_key], 
                              font=ctk.CTkFont(size=12), text_color="white")
            icon.pack(expand=True)
            
            # Text content
            text_frame = ctk.CTkFrame(activity_content, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            name_label = ctk.CTkLabel(text_frame, text=name,
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color=COLORS['text'])
            name_label.pack(anchor="w")
            
            action_label = ctk.CTkLabel(text_frame, text=action,
                                      font=ctk.CTkFont(size=11),
                                      text_color=COLORS['text_secondary'])
            action_label.pack(anchor="w")
            
            # Time
            time_label = ctk.CTkLabel(activity_content, text=time,
                                    font=ctk.CTkFont(size=10),
                                    text_color=COLORS['text_secondary'])
            time_label.pack(side="right", padx=(15, 0))
    
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
        """Show comprehensive salary management with 36/24 month logic"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color=COLORS['primary'])
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="💰 Nâng lương định kỳ", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="36 tháng (Chuyên viên+) | 24 tháng (Nhân viên) | Phụ cấp thâm niên", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        # Main content with sample data
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(content_frame, height=100)
        stats_frame.pack(fill="x", pady=15)
        stats_frame.pack_propagate(False)
        
        stats = [("Đủ 36 tháng", "18", COLORS['primary']), ("Đủ 24 tháng", "25", COLORS['success']), 
                ("Phụ cấp thâm niên", "12", COLORS['warning']), ("Tạm hoãn", "3", COLORS['error'])]
        
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11), text_color="white").pack(pady=5)
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Sample employee list
        list_title = ctk.CTkLabel(content_frame, text="📋 Danh sách đủ điều kiện nâng lương", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        list_title.pack(pady=(20, 10))
        
        employees = [
            ("NV001", "Nguyễn Văn A", "Chuyên viên chính", "A2/3.2 → A2/3.45", "36 tháng", "✅"),
            ("NV002", "Trần Thị B", "Chuyên viên", "A1/2.34 → A1/2.67", "36 tháng", "✅"),  
            ("NV003", "Lê Văn C", "Nhân viên", "B1/1.86 → B1/2.1", "24 tháng", "✅"),
            ("NV004", "Phạm Thị D", "Chuyên viên chính", "A2/4.2 → +5% thâm niên", "Bậc tối đa", "🔄"),
            ("NV005", "Hoàng Văn E", "Chuyên viên", "A1/3.0 → A2/3.33", "36 tháng", "⏳")
        ]
        
        for emp in employees:
            emp_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            emp_frame.pack(fill="x", pady=5)
            
            # Employee info
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(fill="both", padx=15, pady=10)
            
            # Row 1: Basic info
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            ctk.CTkLabel(row1, text=f"{emp[0]} - {emp[1]}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            ctk.CTkLabel(row1, text=emp[2], font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row1, text=emp[5], font=ctk.CTkFont(size=14)).pack(side="right")
            
            # Row 2: Salary info
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(3, 0))
            
            ctk.CTkLabel(row2, text=emp[3], font=ctk.CTkFont(size=10), text_color=COLORS['success']).pack(side="left")
            ctk.CTkLabel(row2, text=f"Logic: {emp[4]}", font=ctk.CTkFont(size=9), text_color=COLORS['text_secondary']).pack(side="right")
        
        # Export buttons
        export_frame = ctk.CTkFrame(content_frame, height=80)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Xuất văn bản", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        buttons_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        buttons_frame.pack()
        
        ctk.CTkButton(buttons_frame, text="Công văn rà soát", width=140).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Thông báo KQ", width=140).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Quyết định", width=140).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Excel", width=100, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_retirement_tracking(self):
        """Show comprehensive retirement tracking with alerts and early salary"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color=COLORS['warning'])
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="⏰ Theo dõi nghỉ hưu", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Cảnh báo 6/3/1 tháng | Nâng lương trước hạn khi nghỉ hưu", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        # Main content
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Alert statistics
        stats_frame = ctk.CTkFrame(content_frame, height=120)
        stats_frame.pack(fill="x", pady=15)
        stats_frame.pack_propagate(False)
        
        stats = [
            ("Tổng sắp nghỉ hưu", "24", COLORS['primary']),
            ("Cần thông báo (6T)", "8", COLORS['warning']),
            ("Cần quyết định (3T)", "12", COLORS['error']),
            ("Đủ nâng lương TH", "4", COLORS['success'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=10), text_color="white").pack(pady=5)
            
            # Priority indicator
            if i == 2:  # Need decision
                ctk.CTkLabel(card, text="🚨 URGENT", font=ctk.CTkFont(size=8, weight="bold"), text_color="white").pack()
            elif i == 1:  # Need notification
                ctk.CTkLabel(card, text="⚠️ IMPORTANT", font=ctk.CTkFont(size=8, weight="bold"), text_color="white").pack()
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Retirement alerts list
        alerts_title = ctk.CTkLabel(content_frame, text="📋 Danh sách cảnh báo nghỉ hưu", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        alerts_title.pack(pady=(20, 10))
        
        # Sample retirement data with different alert levels
        retirement_data = [
            ("NV101", "Nguyễn Thị Lan", "Trưởng phòng", "15/06/1964", "15/06/2024", "3 tháng", "🚨", "Cần QĐ ngay", COLORS['error']),
            ("NV102", "Trần Văn Hùng", "Chuyên viên chính", "20/08/1964", "20/08/2024", "5 tháng", "⚠️", "Cần thông báo", COLORS['warning']),
            ("NV103", "Lê Thị Mai", "Phó trưởng phòng", "10/01/1965", "10/01/2025", "7 tháng", "📢", "Chuẩn bị TB", COLORS['primary']),
            ("NV104", "Phạm Văn Đức", "Chuyên viên chính", "25/03/1964", "25/03/2024", "1 tháng", "🔥", "Khẩn cấp!", COLORS['error']),
            ("NV105", "Hoàng Thị Hoa", "Chuyên viên", "30/11/1964", "30/11/2024", "8 tháng", "⏰", "Theo dõi", COLORS['success'])
        ]
        
        for emp in retirement_data:
            emp_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=2, border_color=emp[8])
            emp_frame.pack(fill="x", pady=8)
            
            # Priority indicator stripe
            priority_stripe = ctk.CTkFrame(emp_frame, width=8, fg_color=emp[8])
            priority_stripe.pack(side="left", fill="y")
            
            # Employee info
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)
            
            # Row 1: Basic info with alert icon
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            ctk.CTkLabel(row1, text=emp[6], font=ctk.CTkFont(size=16)).pack(side="left")
            ctk.CTkLabel(row1, text=f"{emp[0]} - {emp[1]}", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row1, text=emp[2], font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row1, text=emp[7], font=ctk.CTkFont(size=11, weight="bold"), text_color=emp[8]).pack(side="right")
            
            # Row 2: Retirement details
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(5, 0))
            
            ctk.CTkLabel(row2, text=f"Sinh: {emp[3]} → Nghỉ hưu: {emp[4]}", 
                        font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left")
            ctk.CTkLabel(row2, text=f"Còn {emp[5]}", font=ctk.CTkFont(size=10, weight="bold"), 
                        text_color=emp[8]).pack(side="right")
            
            # Action buttons
            actions_frame = ctk.CTkFrame(emp_frame, fg_color="transparent", width=150)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            if "3 tháng" in emp[5] or "1 tháng" in emp[5]:
                ctk.CTkButton(actions_frame, text="Xuất QĐ", width=100, height=28, 
                            fg_color=COLORS['error'], font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Nâng lương TH", width=100, height=28,
                            fg_color=COLORS['success'], font=ctk.CTkFont(size=9)).pack(pady=2)
            elif "5 tháng" in emp[5]:
                ctk.CTkButton(actions_frame, text="Xuất TB", width=100, height=28,
                            fg_color=COLORS['warning'], font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Chi tiết", width=100, height=28,
                            font=ctk.CTkFont(size=9)).pack(pady=2)
            else:
                ctk.CTkButton(actions_frame, text="Chi tiết", width=100, height=28,
                            font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Theo dõi", width=100, height=28,
                            fg_color=COLORS['primary'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Early salary increase section
        early_salary_title = ctk.CTkLabel(content_frame, text="⚡ Nâng lương trước hạn khi nghỉ hưu", 
                                        font=ctk.CTkFont(size=16, weight="bold"))
        early_salary_title.pack(pady=(30, 10))
        
        early_salary_note = ctk.CTkLabel(content_frame, 
                                       text="📝 Nhân viên thông báo nghỉ hưu được xét nâng lương trước thời hạn nếu đủ điều kiện",
                                       font=ctk.CTkFont(size=11), text_color=COLORS['text_secondary'])
        early_salary_note.pack(pady=(0, 10))
        
        # Early salary candidates
        early_candidates = [
            ("NV101", "Nguyễn Thị Lan", "A3/4.8 → A3/5.10", "Đủ điều kiện", "✅"),
            ("NV102", "Trần Văn Hùng", "A2/3.66 → A2/4.06", "Đủ điều kiện", "✅"),
            ("NV104", "Phạm Văn Đức", "A2/3.33 → A2/3.66", "Chưa đủ thời gian", "⏳")
        ]
        
        for candidate in early_candidates:
            cand_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'], height=50)
            cand_frame.pack(fill="x", pady=3)
            cand_frame.pack_propagate(False)
            
            content_frame_inner = ctk.CTkFrame(cand_frame, fg_color="transparent")
            content_frame_inner.pack(fill="both", expand=True, padx=15, pady=8)
            
            ctk.CTkLabel(content_frame_inner, text=candidate[4], font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(content_frame_inner, text=f"{candidate[0]} - {candidate[1]}", 
                        font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(content_frame_inner, text=candidate[2], font=ctk.CTkFont(size=10), 
                        text_color=COLORS['success']).pack(side="left", padx=(15, 0))
            ctk.CTkLabel(content_frame_inner, text=candidate[3], font=ctk.CTkFont(size=10), 
                        text_color=COLORS['text_secondary']).pack(side="right")
            
            if candidate[4] == "✅":
                ctk.CTkButton(content_frame_inner, text="Phê duyệt", width=80, height=25,
                            fg_color=COLORS['success'], font=ctk.CTkFont(size=9)).pack(side="right", padx=(0, 10))
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=80)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Xuất văn bản nghỉ hưu", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📢 Thông báo 6 tháng", width=150, 
                    fg_color=COLORS['warning']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📄 Quyết định 3 tháng", width=150, 
                    fg_color=COLORS['error']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="⚡ QĐ nâng lương TH", width=150, 
                    fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_planning_check(self):
        """Show comprehensive planning check with age limits and quota management"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color=COLORS['success'])
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="📋 Kiểm tra quy hoạch cán bộ", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Kiểm tra tuổi, quota, điều kiện quy hoạch theo từng vị trí", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        # Main content
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Planning statistics overview
        stats_frame = ctk.CTkFrame(content_frame, height=120)
        stats_frame.pack(fill="x", pady=15)
        stats_frame.pack_propagate(False)
        
        planning_stats = [
            ("Tổng quy hoạch", "45", COLORS['primary']),
            ("Đang hoạt động", "38", COLORS['success']),
            ("Sắp hết hạn", "7", COLORS['warning']),
            ("Quá tuổi", "5", COLORS['error'])
        ]
        
        for i, (label, value, color) in enumerate(planning_stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=10), text_color="white").pack(pady=5)
            
            # Status indicators
            if "hết hạn" in label:
                ctk.CTkLabel(card, text="⚠️ CẦN GIA HẠN", font=ctk.CTkFont(size=8, weight="bold"), text_color="white").pack()
            elif "Quá tuổi" in label:
                ctk.CTkLabel(card, text="🚫 VÔ HIỆU", font=ctk.CTkFont(size=8, weight="bold"), text_color="white").pack()
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Position-based planning analysis
        position_title = ctk.CTkLabel(content_frame, text="📊 Phân tích quy hoạch theo vị trí", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        position_title.pack(pady=(20, 10))
        
        # Position quota table
        position_data = [
            ("Giám đốc", 1, 1, 0, "45-60", "Đủ", "✅"),
            ("Phó Giám đốc", 2, 2, 0, "40-58", "Đủ", "✅"),
            ("Trưởng phòng", 8, 6, 2, "35-55", "Thiếu", "⚠️"),
            ("Phó Trưởng phòng", 12, 10, 2, "32-52", "Thiếu", "⚠️"),
            ("Chuyên viên chính", 15, 14, 1, "30-50", "Đủ", "✅"),
            ("Trưởng chi nhánh", 3, 2, 1, "35-55", "Thiếu", "❌")
        ]
        
        # Position table
        for pos_info in position_data:
            pos_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            pos_frame.pack(fill="x", pady=5)
            
            # Status indicator
            status = pos_info[6]
            if status == "✅":
                indicator_color = COLORS['success']
            elif status == "⚠️":
                indicator_color = COLORS['warning']
            else:
                indicator_color = COLORS['error']
            
            ctk.CTkFrame(pos_frame, width=6, fg_color=indicator_color).pack(side="left", fill="y")
            
            # Position info
            info_frame = ctk.CTkFrame(pos_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)
            
            # Row 1: Position and status
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            ctk.CTkLabel(row1, text=pos_info[0], font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
            ctk.CTkLabel(row1, text=f"Tuổi: {pos_info[4]}", font=ctk.CTkFont(size=10), 
                        text_color=COLORS['text_secondary']).pack(side="left", padx=(20, 0))
            ctk.CTkLabel(row1, text=f"{status} {pos_info[5]}", font=ctk.CTkFont(size=11, weight="bold"), 
                        text_color=indicator_color).pack(side="right")
            
            # Row 2: Quota details
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(5, 0))
            
            quota_text = f"Định mức: {pos_info[1]} | Hiện có: {pos_info[2]} | Cần bổ sung: {pos_info[3]}"
            ctk.CTkLabel(row2, text=quota_text, font=ctk.CTkFont(size=10), 
                        text_color=COLORS['text_secondary']).pack(side="left")
            
            # Action buttons
            actions_frame = ctk.CTkFrame(pos_frame, fg_color="transparent", width=120)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            ctk.CTkButton(actions_frame, text="Xem DS", width=80, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
            
            if pos_info[3] > 0:  # Need more people
                ctk.CTkButton(actions_frame, text="Đề xuất", width=80, height=25,
                            fg_color=COLORS['warning'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Individual planning list
        individual_title = ctk.CTkLabel(content_frame, text="👥 Danh sách cá nhân trong quy hoạch", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        individual_title.pack(pady=(30, 10))
        
        # Individual planning data with age checking
        individual_planning = [
            ("NV201", "Nguyễn Văn Minh", "Chuyên viên chính", "Trưởng phòng", 38, "2022-01-15", "2027-01-15", "Trong hạn", "✅"),
            ("NV202", "Trần Thị Hương", "Phó Trưởng phòng", "Trưởng phòng", 42, "2021-06-01", "2026-06-01", "Sắp hết hạn", "⚠️"),
            ("NV203", "Lê Văn Đức", "Chuyên viên chính", "Phó Trưởng phòng", 56, "2020-03-10", "2025-03-10", "Quá tuổi", "❌"),
            ("NV204", "Phạm Thị Lan", "Chuyên viên", "Chuyên viên chính", 35, "2023-08-20", "2028-08-20", "Mới quy hoạch", "✅"),
            ("NV205", "Hoàng Văn Tâm", "Phó Trưởng phòng", "Trưởng phòng", 45, "2019-12-05", "2024-12-05", "Hết hạn", "🚫")
        ]
        
        for person in individual_planning:
            person_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            person_frame.pack(fill="x", pady=5)
            
            # Status indicator
            status = person[8]
            if status == "✅":
                indicator_color = COLORS['success']
            elif status == "⚠️":
                indicator_color = COLORS['warning'] 
            elif status == "❌":
                indicator_color = COLORS['error']
            else:
                indicator_color = "#6b7280"  # Gray for expired
            
            ctk.CTkFrame(person_frame, width=6, fg_color=indicator_color).pack(side="left", fill="y")
            
            # Person info
            info_frame = ctk.CTkFrame(person_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            # Row 1: Basic info with status
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            ctk.CTkLabel(row1, text=f"{person[0]} - {person[1]}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            ctk.CTkLabel(row1, text=f"Tuổi: {person[4]}", font=ctk.CTkFont(size=10), 
                        text_color=COLORS['text_secondary']).pack(side="left", padx=(15, 0))
            ctk.CTkLabel(row1, text=f"{status} {person[7]}", font=ctk.CTkFont(size=10, weight="bold"), 
                        text_color=indicator_color).pack(side="right")
            
            # Row 2: Planning details
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(3, 0))
            
            planning_text = f"{person[2]} → {person[3]} | Từ {person[5]} đến {person[6]}"
            ctk.CTkLabel(row2, text=planning_text, font=ctk.CTkFont(size=10), 
                        text_color=COLORS['text_secondary']).pack(side="left")
            
            # Actions based on status
            actions_frame = ctk.CTkFrame(person_frame, fg_color="transparent", width=120)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            ctk.CTkButton(actions_frame, text="Chi tiết", width=80, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
            
            if "Sắp hết hạn" in person[7] or "Hết hạn" in person[7]:
                ctk.CTkButton(actions_frame, text="Gia hạn", width=80, height=25,
                            fg_color=COLORS['warning'], font=ctk.CTkFont(size=9)).pack(pady=2)
            elif "Quá tuổi" in person[7]:
                ctk.CTkButton(actions_frame, text="Loại bỏ", width=80, height=25,
                            fg_color=COLORS['error'], font=ctk.CTkFont(size=9)).pack(pady=2)
            else:
                ctk.CTkButton(actions_frame, text="Đề xuất BN", width=80, height=25,
                            fg_color=COLORS['success'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Export and settings section
        bottom_section = ctk.CTkFrame(content_frame, height=80)
        bottom_section.pack(fill="x", pady=20)
        bottom_section.pack_propagate(False)
        
        export_title = ctk.CTkLabel(bottom_section, text="🔧 Cài đặt và xuất báo cáo", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        bottom_buttons = ctk.CTkFrame(bottom_section, fg_color="transparent")
        bottom_buttons.pack()
        
        ctk.CTkButton(bottom_buttons, text="⚙️ Cài đặt giới hạn tuổi", width=160).pack(side="left", padx=10)
        ctk.CTkButton(bottom_buttons, text="📊 Báo cáo tổng hợp", width=160, 
                    fg_color=COLORS['primary']).pack(side="left", padx=10)
        ctk.CTkButton(bottom_buttons, text="📈 Excel phân tích", width=160, 
                    fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_work_history(self):
        """Show comprehensive work history management with timeline"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="#8b5cf6")
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="💼 Quá trình công tác", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Timeline công tác | Thêm/Sửa/Xóa giai đoạn | Xuất hồ sơ", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        # Employee selector
        selector_frame = ctk.CTkFrame(self.main_content, height=60, fg_color=COLORS['background'])
        selector_frame.pack(fill="x", padx=20, pady=10)
        selector_frame.pack_propagate(False)
        
        ctk.CTkLabel(selector_frame, text="Chọn nhân viên:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=20, pady=15)
        emp_combo = ctk.CTkOptionMenu(selector_frame, values=["NV001 - Nguyễn Văn A", "NV002 - Trần Thị B", "NV003 - Lê Văn C"], width=250)
        emp_combo.pack(side="left", padx=10)
        ctk.CTkButton(selector_frame, text="📋 Xem timeline", width=120).pack(side="right", padx=20)
        
        # Main content
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Work history timeline
        timeline_title = ctk.CTkLabel(content_frame, text="📅 Timeline công tác - Nguyễn Văn A", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        timeline_title.pack(pady=(10, 20))
        
        # Timeline data
        timeline_data = [
            ("2024-01-15", "Hiện tại", "Chuyên viên chính", "Phòng TCHC", "Quản lý hồ sơ cán bộ", "Đang làm việc", "active"),
            ("2022-03-01", "2023-12-31", "Chuyên viên", "Phòng TCHC", "Hỗ trợ công tác nhân sự", "Hoàn thành tốt", "completed"),
            ("2020-08-15", "2022-02-28", "Nhân viên", "Phòng TCKT", "Công tác kế toán tổng hợp", "Chuyển phòng", "completed"),
            ("2018-06-01", "2020-08-14", "Nhân viên", "Phòng TCKT", "Thực tập sinh → Nhân viên", "Kết thúc thử việc", "completed")
        ]
        
        for i, (start_date, end_date, position, dept, duties, result, status) in enumerate(timeline_data):
            # Timeline item
            timeline_item = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            timeline_item.pack(fill="x", pady=8)
            
            # Timeline connector
            if i == 0:  # Current position
                connector_color = COLORS['success']
                status_icon = "🟢"
            else:
                connector_color = COLORS['primary']
                status_icon = "🔵"
            
            connector_frame = ctk.CTkFrame(timeline_item, width=20, fg_color="transparent")
            connector_frame.pack(side="left", fill="y", padx=(10, 0))
            
            ctk.CTkLabel(connector_frame, text=status_icon, font=ctk.CTkFont(size=16)).pack(pady=15)
            
            if i < len(timeline_data) - 1:  # Not the last item
                ctk.CTkFrame(connector_frame, width=3, height=50, fg_color=connector_color).pack()
            
            # Timeline content
            content_frame_inner = ctk.CTkFrame(timeline_item, fg_color="transparent")
            content_frame_inner.pack(side="left", fill="both", expand=True, padx=15, pady=12)
            
            # Row 1: Period and position
            row1 = ctk.CTkFrame(content_frame_inner, fg_color="transparent")
            row1.pack(fill="x")
            
            period_text = f"{start_date} - {end_date}" if end_date != "Hiện tại" else f"{start_date} - Hiện tại"
            ctk.CTkLabel(row1, text=period_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=connector_color).pack(side="left")
            ctk.CTkLabel(row1, text=f"{position} - {dept}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(20, 0))
            ctk.CTkLabel(row1, text=result, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="right")
            
            # Row 2: Duties
            row2 = ctk.CTkFrame(content_frame_inner, fg_color="transparent")
            row2.pack(fill="x", pady=(3, 0))
            
            ctk.CTkLabel(row2, text=f"Nhiệm vụ: {duties}", font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left")
            
            # Action buttons
            actions_frame = ctk.CTkFrame(timeline_item, fg_color="transparent", width=100)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            ctk.CTkButton(actions_frame, text="Sửa", width=60, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
            if status != "active":
                ctk.CTkButton(actions_frame, text="Xóa", width=60, height=25, fg_color=COLORS['error'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Add new period section
        add_section = ctk.CTkFrame(content_frame, height=100, fg_color=COLORS['background'])
        add_section.pack(fill="x", pady=20)
        add_section.pack_propagate(False)
        
        add_title = ctk.CTkLabel(add_section, text="➕ Thêm giai đoạn mới", font=ctk.CTkFont(size=14, weight="bold"))
        add_title.pack(pady=10)
        
        add_form = ctk.CTkFrame(add_section, fg_color="transparent")
        add_form.pack(expand=True)
        
        # Form fields in a row
        form_row = ctk.CTkFrame(add_form, fg_color="transparent")
        form_row.pack()
        
        ctk.CTkEntry(form_row, placeholder_text="Từ ngày", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(form_row, placeholder_text="Đến ngày", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(form_row, placeholder_text="Chức vụ", width=120).pack(side="left", padx=5)
        ctk.CTkEntry(form_row, placeholder_text="Đơn vị", width=100).pack(side="left", padx=5)
        ctk.CTkButton(form_row, text="Thêm", width=80, fg_color=COLORS['success']).pack(side="left", padx=10)
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=60)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Xuất hồ sơ công tác", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📄 Sơ yếu lý lịch", width=140).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📋 Quá trình công tác", width=140, fg_color=COLORS['primary']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📊 Excel timeline", width=140, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_contracts(self):
        """Show comprehensive contract management for BKS and employees"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="#f59e0b")
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="📄 Hợp đồng lao động", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="BKS + Nhân viên | Cảnh báo hết hạn | Gia hạn tự động", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Contract statistics
        stats_frame = ctk.CTkFrame(content_frame, height=120)
        stats_frame.pack(fill="x", pady=15)
        stats_frame.pack_propagate(False)
        
        contract_stats = [
            ("Tổng HĐ", "156", COLORS['primary']),
            ("Còn hiệu lực", "142", COLORS['success']),
            ("Sắp hết hạn", "8", COLORS['warning']),
            ("HĐ BKS", "14", "#f59e0b")
        ]
        
        for i, (label, value, color) in enumerate(contract_stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=10), text_color="white").pack(pady=5)
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Contract list
        contract_title = ctk.CTkLabel(content_frame, text="📋 Danh sách hợp đồng", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        contract_title.pack(pady=(20, 10))
        
        contracts_data = [
            ("NV001", "Nguyễn Văn A", "HĐ không xác định thời hạn", "2020-08-01", "Vô thời hạn", "Còn hiệu lực", "✅"),
            ("BKS01", "Trần Thị B", "HĐ Ban kiểm soát", "2023-01-15", "2025-01-14", "Sắp hết hạn", "⚠️"),
            ("NV025", "Lê Văn C", "HĐ có thời hạn 2 năm", "2022-06-01", "2024-05-31", "Hết hạn", "🚫"),
            ("BKS02", "Phạm Thị D", "HĐ Ban kiểm soát", "2022-08-20", "2024-08-19", "Cần gia hạn", "⚠️"),
            ("NV050", "Hoàng Văn E", "HĐ thử việc", "2024-01-10", "2024-03-09", "Chuyển chính thức", "✅")
        ]
        
        for contract in contracts_data:
            contract_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            contract_frame.pack(fill="x", pady=5)
            
            # Status indicator
            status = contract[6]
            if status == "✅":
                indicator_color = COLORS['success']
            elif status == "⚠️":
                indicator_color = COLORS['warning']
            else:
                indicator_color = COLORS['error']
            
            ctk.CTkFrame(contract_frame, width=6, fg_color=indicator_color).pack(side="left", fill="y")
            
            # Contract info
            info_frame = ctk.CTkFrame(contract_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            # Row 1: Basic info
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            employee_text = f"{contract[0]} - {contract[1]}"
            if "BKS" in contract[0]:
                employee_text += " (Ban kiểm soát)"
            
            ctk.CTkLabel(row1, text=employee_text, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            ctk.CTkLabel(row1, text=f"{status} {contract[5]}", font=ctk.CTkFont(size=10, weight="bold"), text_color=indicator_color).pack(side="right")
            
            # Row 2: Contract details
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(3, 0))
            
            contract_detail = f"{contract[2]} | {contract[3]} → {contract[4]}"
            ctk.CTkLabel(row2, text=contract_detail, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left")
            
            # Action buttons
            actions_frame = ctk.CTkFrame(contract_frame, fg_color="transparent", width=120)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            ctk.CTkButton(actions_frame, text="Chi tiết", width=80, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
            
            if "Sắp hết hạn" in contract[5] or "Cần gia hạn" in contract[5]:
                ctk.CTkButton(actions_frame, text="Gia hạn", width=80, height=25, fg_color=COLORS['warning'], font=ctk.CTkFont(size=9)).pack(pady=2)
            elif "Hết hạn" in contract[5]:
                ctk.CTkButton(actions_frame, text="Tạo mới", width=80, height=25, fg_color=COLORS['success'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=60)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Báo cáo hợp đồng", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📊 Tổng hợp HĐ", width=140).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="⚠️ Cảnh báo hết hạn", width=140, fg_color=COLORS['warning']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📈 Excel BKS", width=140, fg_color="#f59e0b").pack(side="left", padx=10)
    
    def show_appointment_check(self):
        """Show comprehensive appointment condition checking"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color=COLORS['success'])
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="✅ Điều kiện bổ nhiệm", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Kiểm tra đầy đủ | Cảnh báo 90 ngày | Hồ sơ đề xuất", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Check form
        check_frame = ctk.CTkFrame(content_frame, height=100, fg_color=COLORS['background'])
        check_frame.pack(fill="x", pady=15)
        check_frame.pack_propagate(False)
        
        ctk.CTkLabel(check_frame, text="🔍 Kiểm tra điều kiện bổ nhiệm", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        form_row = ctk.CTkFrame(check_frame, fg_color="transparent")
        form_row.pack()
        
        ctk.CTkLabel(form_row, text="Nhân viên:").pack(side="left", padx=10)
        emp_combo = ctk.CTkOptionMenu(form_row, values=["NV001 - Nguyễn Văn A", "NV002 - Trần Thị B"], width=200)
        emp_combo.pack(side="left", padx=10)
        
        ctk.CTkLabel(form_row, text="Vị trí:").pack(side="left", padx=10)
        pos_combo = ctk.CTkOptionMenu(form_row, values=["Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên chính"], width=150)
        pos_combo.pack(side="left", padx=10)
        
        ctk.CTkButton(form_row, text="🔍 Kiểm tra", width=100, fg_color=COLORS['primary']).pack(side="left", padx=20)
        
        # Check results
        results_title = ctk.CTkLabel(content_frame, text="📋 Kết quả kiểm tra - Nguyễn Văn A → Trưởng phòng", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        results_title.pack(pady=(20, 10))
        
        conditions = [
            ("✅", "Quy hoạch", "Có trong quy hoạch Trưởng phòng (2022-2027)", COLORS['success']),
            ("✅", "Học vấn", "Thạc sĩ Luật - Đạt yêu cầu tối thiểu Đại học", COLORS['success']),
            ("✅", "Chứng chỉ", "Có chứng chỉ Quản lý Nhà nước hạng III", COLORS['success']),
            ("✅", "Kinh nghiệm", "8 năm kinh nghiệm (≥5 năm yêu cầu)", COLORS['success']),
            ("⚠️", "Tuổi", "38 tuổi - Gần giới hạn tối đa 40 tuổi", COLORS['warning']),
            ("✅", "Đánh giá", "Hoàn thành tốt nhiệm vụ 3 năm liên tiếp", COLORS['success'])
        ]
        
        for status, condition, detail, color in conditions:
            cond_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=color)
            cond_frame.pack(fill="x", pady=3)
            
            ctk.CTkFrame(cond_frame, width=5, fg_color=color).pack(side="left", fill="y")
            
            info_frame = ctk.CTkFrame(cond_frame, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=15, pady=8)
            
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x")
            
            ctk.CTkLabel(row, text=status, font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(row, text=condition, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row, text=detail, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(20, 0))
        
        # Overall result
        result_frame = ctk.CTkFrame(content_frame, height=60, fg_color=COLORS['success'])
        result_frame.pack(fill="x", pady=20)
        result_frame.pack_propagate(False)
        
        ctk.CTkLabel(result_frame, text="🎉 ĐỦ ĐIỀU KIỆN BỔ NHIỆM", font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(pady=15)
        
        # Reappointment alerts
        alerts_title = ctk.CTkLabel(content_frame, text="⏰ Cảnh báo bổ nhiệm lại (90 ngày)", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        alerts_title.pack(pady=(20, 10))
        
        reappointments = [
            ("NV010", "Lê Thị Mai", "Phó Trưởng phòng", "2024-03-15", "45 ngày", "🚨"),
            ("NV015", "Phạm Văn Đức", "Trưởng phòng", "2024-04-20", "78 ngày", "⚠️"),
            ("NV020", "Hoàng Thị Lan", "Chuyên viên chính", "2024-05-10", "98 ngày", "📢")
        ]
        
        for emp_id, name, position, reappoint_date, days_left, priority in reappointments:
            alert_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'], height=50)
            alert_frame.pack(fill="x", pady=3)
            alert_frame.pack_propagate(False)
            
            content_frame_inner = ctk.CTkFrame(alert_frame, fg_color="transparent")
            content_frame_inner.pack(fill="both", expand=True, padx=15, pady=8)
            
            ctk.CTkLabel(content_frame_inner, text=priority, font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(content_frame_inner, text=f"{emp_id} - {name}", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(content_frame_inner, text=f"{position} - Còn {days_left}", font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(15, 0))
            ctk.CTkButton(content_frame_inner, text="Kiểm tra", width=80, height=25, font=ctk.CTkFont(size=9)).pack(side="right")
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=60)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Hồ sơ đề xuất", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📋 Tờ trình đề xuất", width=140).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📊 Báo cáo điều kiện", width=140, fg_color=COLORS['primary']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📈 Thống kê BN", width=140, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_award_check(self):
        """Show comprehensive award condition checking"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="#8b5cf6")
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="🏆 Điều kiện khen thưởng", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Tiêu chí khen thưởng | Đánh giá thành tích | Đề xuất", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Award form
        form_frame = ctk.CTkFrame(content_frame, height=80, fg_color=COLORS['background'])
        form_frame.pack(fill="x", pady=15)
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="🔍 Kiểm tra tiêu chuẩn khen thưởng", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        form_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_row.pack()
        
        ctk.CTkLabel(form_row, text="Nhân viên:").pack(side="left", padx=10)
        ctk.CTkOptionMenu(form_row, values=["NV001 - Nguyễn Văn A", "NV002 - Trần Thị B"], width=180).pack(side="left", padx=10)
        
        ctk.CTkLabel(form_row, text="Loại khen thưởng:").pack(side="left", padx=10)
        ctk.CTkOptionMenu(form_row, values=["Giấy khen cá nhân", "Bằng khen cục trưởng", "Lao động tiên tiến"], width=150).pack(side="left", padx=10)
        
        ctk.CTkButton(form_row, text="🔍 Kiểm tra", width=100, fg_color="#8b5cf6").pack(side="left", padx=20)
        
        # Award criteria results
        criteria_title = ctk.CTkLabel(content_frame, text="📋 Tiêu chí đánh giá - Nguyễn Văn A (Giấy khen cá nhân)", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        criteria_title.pack(pady=(20, 10))
        
        award_criteria = [
            ("✅", "Hoàn thành nhiệm vụ", "Hoàn thành xuất sắc nhiệm vụ được giao năm 2023", COLORS['success']),
            ("✅", "Không vi phạm kỷ luật", "Không có hình thức kỷ luật nào trong 12 tháng qua", COLORS['success']),
            ("✅", "Thành tích nổi bật", "Tổ chức thành công dự án số hóa hồ sơ nhân sự", COLORS['success']),
            ("✅", "Thời gian công tác", "6 năm kinh nghiệm làm việc (≥1 năm yêu cầu)", COLORS['success']),
            ("⚠️", "Lần khen thưởng gần nhất", "Lần cuối nhận khen thưởng: 8 tháng trước (khuyến khích ít nhất 12 tháng)", COLORS['warning'])
        ]
        
        for status, criterion, detail, color in award_criteria:
            criteria_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=color)
            criteria_frame.pack(fill="x", pady=3)
            
            ctk.CTkFrame(criteria_frame, width=5, fg_color=color).pack(side="left", fill="y")
            
            info_frame = ctk.CTkFrame(criteria_frame, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=15, pady=8)
            
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x")
            
            ctk.CTkLabel(row, text=status, font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(row, text=criterion, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row, text=detail, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(20, 0))
        
        # Award result
        result_frame = ctk.CTkFrame(content_frame, height=60, fg_color=COLORS['warning'])
        result_frame.pack(fill="x", pady=20)
        result_frame.pack_propagate(False)
        
        ctk.CTkLabel(result_frame, text="⚠️ CầN XÂN NHẮC THỜI GIAN KHEN THƯỜNG LẦN TRƯỚC", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=15)
        
        # Award candidates list
        candidates_title = ctk.CTkLabel(content_frame, text="🎖️ Ưu tiên khen thưởng năm 2024", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        candidates_title.pack(pady=(20, 10))
        
        candidates = [
            ("NV005", "Hoàng Văn Tâm", "Sáng kiến cải tiến quy trình", "Giấy khen", "✅"),
            ("NV012", "Nguyễn Thị Họng", "Dẫn đầu dự án ISO 9001:2015", "Bằng khen", "✅"),
            ("NV018", "Lê Văn Quân", "10 năm không nghỉ phép", "Lao động tiên tiến", "✅"),
            ("NV025", "Trần Thị Mai", "Hỗ trợ đồng nghiệp vượt khó COVID", "Giấy khen", "⚠️")
        ]
        
        for emp_id, name, achievement, award_type, status in candidates:
            cand_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'], height=50)
            cand_frame.pack(fill="x", pady=3)
            cand_frame.pack_propagate(False)
            
            content_frame_inner = ctk.CTkFrame(cand_frame, fg_color="transparent")
            content_frame_inner.pack(fill="both", expand=True, padx=15, pady=8)
            
            ctk.CTkLabel(content_frame_inner, text=status, font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(content_frame_inner, text=f"{emp_id} - {name}", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(content_frame_inner, text=achievement, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(15, 0))
            ctk.CTkLabel(content_frame_inner, text=award_type, font=ctk.CTkFont(size=10, weight="bold"), text_color="#8b5cf6").pack(side="right", padx=(0, 10))
            
            if status == "✅":
                ctk.CTkButton(content_frame_inner, text="Đề xuất", width=80, height=25, fg_color="#8b5cf6", font=ctk.CTkFont(size=9)).pack(side="right")
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=60)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Đề xuất khen thưởng", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📋 Tờ trình đề xuất", width=140).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="🏆 Danh sách ưu tiên", width=140, fg_color="#8b5cf6").pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📈 Thống kê KT", width=140, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_early_salary(self):
        """Show early salary increase management for outstanding achievements"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="#f59e0b")
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="⚡ Nâng lương trước hạn", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Thành tích xuất sắc | Đánh giá đặc biệt | Quyết định nâng lương", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Early salary statistics
        stats_frame = ctk.CTkFrame(content_frame, height=100)
        stats_frame.pack(fill="x", pady=15)
        stats_frame.pack_propagate(False)
        
        early_stats = [
            ("Đề xuất mới", "6", COLORS['primary']),
            ("Đang xét duyệt", "4", COLORS['warning']),
            ("Đã phê duyệt", "8", COLORS['success']),
            ("Từ chối", "2", COLORS['error'])
        ]
        
        for i, (label, value, color) in enumerate(early_stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=10), text_color="white").pack(pady=5)
        
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Early salary candidates
        candidates_title = ctk.CTkLabel(content_frame, text="🎆 Ứng viên nâng lương trước hạn", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        candidates_title.pack(pady=(20, 10))
        
        early_candidates = [
            ("NV008", "Nguyễn Thị Linh", "A1/2.67", "A2/3.0", "Sáng kiến tiết kiệm 50M/năm", "Chờ duyệt", "⚡"),
            ("NV015", "Trần Văn Minh", "A2/3.33", "A2/3.66", "Lãnh đạo dự án thành công", "Đã duyệt", "✅"),
            ("NV022", "Lê Thị Hoa", "B1/2.1", "B1/2.34", "Giải nhất sáng kiến cấp Bộ", "Đã duyệt", "✅"),
            ("NV035", "Phạm Văn Đức", "A1/2.34", "A1/2.67", "Nghiên cứu khoa học được ứng dụng", "Chờ duyệt", "⚡"),
            ("NV041", "Hoàng Thị Mai", "A2/3.0", "A2/3.33", "Giải quyết sự cố nghiêm trọng", "Từ chối", "❌")
        ]
        
        for emp_id, name, current_salary, proposed_salary, achievement, status, icon in early_candidates:
            candidate_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
            candidate_frame.pack(fill="x", pady=5)
            
            # Status indicator
            if "✅" in icon:
                indicator_color = COLORS['success']
            elif "⚡" in icon:
                indicator_color = "#f59e0b"
            else:
                indicator_color = COLORS['error']
            
            ctk.CTkFrame(candidate_frame, width=6, fg_color=indicator_color).pack(side="left", fill="y")
            
            # Candidate info
            info_frame = ctk.CTkFrame(candidate_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
            
            # Row 1: Basic info
            row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row1.pack(fill="x")
            
            ctk.CTkLabel(row1, text=icon, font=ctk.CTkFont(size=14)).pack(side="left")
            ctk.CTkLabel(row1, text=f"{emp_id} - {name}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(row1, text=status, font=ctk.CTkFont(size=10, weight="bold"), text_color=indicator_color).pack(side="right")
            
            # Row 2: Salary and achievement
            row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
            row2.pack(fill="x", pady=(3, 0))
            
            salary_text = f"{current_salary} → {proposed_salary}"
            ctk.CTkLabel(row2, text=salary_text, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS['success']).pack(side="left")
            ctk.CTkLabel(row2, text=achievement, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="left", padx=(20, 0))
            
            # Action buttons
            actions_frame = ctk.CTkFrame(candidate_frame, fg_color="transparent", width=120)
            actions_frame.pack(side="right", padx=15)
            actions_frame.pack_propagate(False)
            
            if "Chờ duyệt" in status:
                ctk.CTkButton(actions_frame, text="Phê duyệt", width=80, height=25, fg_color=COLORS['success'], font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Từ chối", width=80, height=25, fg_color=COLORS['error'], font=ctk.CTkFont(size=9)).pack(pady=2)
            elif "Đã duyệt" in status:
                ctk.CTkButton(actions_frame, text="Xuất QĐ", width=80, height=25, fg_color="#f59e0b", font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Chi tiết", width=80, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
            else:
                ctk.CTkButton(actions_frame, text="Lý do", width=80, height=25, font=ctk.CTkFont(size=9)).pack(pady=2)
                ctk.CTkButton(actions_frame, text="Xét lại", width=80, height=25, fg_color=COLORS['warning'], font=ctk.CTkFont(size=9)).pack(pady=2)
        
        # Add new nomination
        add_frame = ctk.CTkFrame(content_frame, height=80, fg_color=COLORS['background'])
        add_frame.pack(fill="x", pady=20)
        add_frame.pack_propagate(False)
        
        ctk.CTkLabel(add_frame, text="➕ Đề xuất nâng lương trước hạn mới", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        add_row = ctk.CTkFrame(add_frame, fg_color="transparent")
        add_row.pack()
        
        ctk.CTkOptionMenu(add_row, values=["NV050 - Nguyễn Văn Tân", "NV055 - Trần Thị Lan"], width=180).pack(side="left", padx=10)
        ctk.CTkEntry(add_row, placeholder_text="Thành tích xuất sắc", width=200).pack(side="left", padx=10)
        ctk.CTkButton(add_row, text="Đề xuất", width=100, fg_color="#f59e0b").pack(side="left", padx=10)
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=60)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Quyết định nâng lương", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📋 Tờ trình đề xuất", width=140).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📄 Quyết định", width=140, fg_color="#f59e0b").pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📈 Báo cáo năm", width=140, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_reports(self):
        """Show comprehensive statistical reports and analysis"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color=COLORS['primary'])
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="📊 Báo cáo thống kê", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="Charts | Phân tích cơ cấu | Báo cáo toàn diện", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Key statistics
        key_stats = ctk.CTkFrame(content_frame, height=160)
        key_stats.pack(fill="x", pady=15)
        key_stats.pack_propagate(False)
        
        ctk.CTkLabel(key_stats, text="📋 Tổng quan chỉ tiêu chính", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        stats_grid = ctk.CTkFrame(key_stats, fg_color="transparent")
        stats_grid.pack(fill="x", padx=20, pady=10)
        
        key_metrics = [
            ("Tổng nhân sự", "156", COLORS['primary']), ("Nâng lương 2024", "43", COLORS['success']),
            ("Nghỉ hưu 2024", "8", COLORS['warning']), ("Thôi việc", "12", COLORS['error']),
            ("Khen thưởng", "25", "#8b5cf6"), ("HĐ hết hạn", "14", "#f59e0b")
        ]
        
        for i, (label, value, color) in enumerate(key_metrics):
            card = ctk.CTkFrame(stats_grid, fg_color=color, width=180)
            card.grid(row=i//3, column=i%3, padx=8, pady=5, sticky="ew")
            
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11), text_color="white").pack(pady=5)
        
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Age structure
        age_section = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'])
        age_section.pack(fill="x", pady=20)
        
        age_header = ctk.CTkFrame(age_section, height=40, fg_color="#8b5cf6")
        age_header.pack(fill="x")
        age_header.pack_propagate(False)
        
        ctk.CTkLabel(age_header, text="🎂 Phân tích cơ cấu tuổi", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(side="left", padx=15, pady=10)
        
        age_content = ctk.CTkFrame(age_section, fg_color="transparent")
        age_content.pack(fill="x", padx=15, pady=15)
        
        age_groups = [
            ("Dưới 30 tuổi", "28 người (18%)", COLORS['success']),
            ("30-40 tuổi", "52 người (33%)", COLORS['primary']),
            ("40-50 tuổi", "45 người (29%)", COLORS['warning']),
            ("Trên 50 tuổi", "31 người (20%)", COLORS['error'])
        ]
        
        for group, count, color in age_groups:
            group_frame = ctk.CTkFrame(age_content, fg_color=COLORS['background'], height=35)
            group_frame.pack(fill="x", pady=3)
            group_frame.pack_propagate(False)
            
            info_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=15, pady=5)
            
            ctk.CTkLabel(info_frame, text=group, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
            ctk.CTkLabel(info_frame, text=count, font=ctk.CTkFont(size=11), text_color=color).pack(side="right")
        
        # Qualifications
        qual_section = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'])
        qual_section.pack(fill="x", pady=20)
        
        qual_header = ctk.CTkFrame(qual_section, height=40, fg_color=COLORS['success'])
        qual_header.pack(fill="x")
        qual_header.pack_propagate(False)
        
        ctk.CTkLabel(qual_header, text="🎓 Cơ cấu học vấn", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(side="left", padx=15, pady=10)
        
        qual_grid = ctk.CTkFrame(qual_section, fg_color="transparent")
        qual_grid.pack(fill="x", padx=15, pady=15)
        
        qualifications = [
            ("Tiến sĩ: 8 (5%)", COLORS['error']), ("Thạc sĩ: 45 (29%)", COLORS['success']),
            ("Đại học: 85 (54%)", COLORS['primary']), ("Cao đẳng: 15 (10%)", COLORS['warning']),
            ("Lý luật III: 65", "#8b5cf6"), ("An ninh III: 32", "#f59e0b")
        ]
        
        for i, (qual, color) in enumerate(qualifications):
            qual_item = ctk.CTkFrame(qual_grid, fg_color=COLORS['background'], height=35)
            qual_item.grid(row=i//3, column=i%3, padx=5, pady=3, sticky="ew")
            qual_item.pack_propagate(False)
            
            ctk.CTkLabel(qual_item, text=qual, font=ctk.CTkFont(size=10), text_color=color).pack(pady=8)
        
        for i in range(3):
            qual_grid.grid_columnconfigure(i, weight=1)
        
        # Export buttons
        export_frame = ctk.CTkFrame(content_frame, height=80)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Xuất báo cáo", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📈 Tháng", width=120, fg_color=COLORS['primary']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📊 Quý", width=120, fg_color=COLORS['success']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📉 Năm", width=120, fg_color=COLORS['warning']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📊 Excel", width=120, fg_color=COLORS['success']).pack(side="left", padx=10)
    
    def show_insurance(self):
        """Show comprehensive social insurance management"""
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="#dc2626")
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(header_frame, text="🏥 Báo bảo hiểm xã hội", 
                           font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title.pack(side="left", padx=20, pady=20)
        
        info_label = ctk.CTkLabel(header_frame, text="BHXH | Xuất Excel | Nhắc nhở tự động", 
                                font=ctk.CTkFont(size=11), text_color="white")
        info_label.pack(side="right", padx=20, pady=20)
        
        content_frame = ctk.CTkScrollableFrame(self.main_content)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Insurance alerts
        alerts_frame = ctk.CTkFrame(content_frame, height=120)
        alerts_frame.pack(fill="x", pady=15)
        alerts_frame.pack_propagate(False)
        
        insurance_alerts = [
            ("Cần điều chỉnh", "12", "#dc2626"),
            ("Nghỉ thai sản", "3", COLORS['warning']),
            ("Nghỉ ốm", "5", COLORS['error']),
            ("Nghỉ hưu", "8", COLORS['success'])
        ]
        
        for i, (label, count, color) in enumerate(insurance_alerts):
            alert_card = ctk.CTkFrame(alerts_frame, fg_color=color)
            alert_card.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(alert_card, text=count, font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(alert_card, text=label, font=ctk.CTkFont(size=10), text_color="white").pack(pady=5)
            ctk.CTkLabel(alert_card, text="CẦN XỬ LÝ", font=ctk.CTkFont(size=8, weight="bold"), text_color="white").pack()
        
        for i in range(4):
            alerts_frame.grid_columnconfigure(i, weight=1)
        
        # Monthly report
        monthly_title = ctk.CTkLabel(content_frame, text="📋 Báo cáo BHXH tháng 12/2024", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        monthly_title.pack(pady=(20, 10))
        
        # Categories
        categories = [
            ("Nhân viên mới tham gia BHXH", [
                ("NV156", "Nguyễn Văn Tân", "15/12/2024", "Tờ khai mới", "✅"),
                ("NV157", "Trần Thị Lan", "20/12/2024", "Tờ khai mới", "✅")
            ]),
            ("Điều chỉnh lương/phụ cấp", [
                ("NV008", "Lê Văn Đức", "01/12/2024", "Điều chỉnh lương", "⚠️"),
                ("NV015", "Phạm Thị Hồng", "15/12/2024", "Điều chỉnh lương", "⚠️")
            ]),
            ("Chấm dứt BHXH", [
                ("NV045", "Hoàng Văn Minh", "31/12/2024", "Nghỉ hưu", "💫"),
                ("NV067", "Nguyễn Thị Mai", "25/12/2024", "Thôi việc", "💫")
            ])
        ]
        
        for category, items in categories:
            # Category header
            cat_header = ctk.CTkFrame(content_frame, height=40, fg_color="#dc2626")
            cat_header.pack(fill="x", pady=(10, 5))
            cat_header.pack_propagate(False)
            
            ctk.CTkLabel(cat_header, text=category, font=ctk.CTkFont(size=12, weight="bold"), text_color="white").pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(cat_header, text=f"{len(items)} trường hợp", font=ctk.CTkFont(size=10), text_color="white").pack(side="right", padx=15, pady=10)
            
            # Items
            for emp_id, name, date, action, status in items:
                item_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['surface'], border_width=1, border_color=COLORS['background'])
                item_frame.pack(fill="x", pady=2)
                
                # Status indicator
                if status == "✅":
                    indicator_color = COLORS['success']
                elif status == "⚠️":
                    indicator_color = COLORS['warning']
                else:
                    indicator_color = COLORS['error']
                
                ctk.CTkFrame(item_frame, width=5, fg_color=indicator_color).pack(side="left", fill="y")
                
                # Item info
                info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)
                
                # Row
                row = ctk.CTkFrame(info_frame, fg_color="transparent")
                row.pack(fill="x")
                
                ctk.CTkLabel(row, text=status, font=ctk.CTkFont(size=12)).pack(side="left")
                ctk.CTkLabel(row, text=f"{emp_id} - {name}", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(10, 0))
                ctk.CTkLabel(row, text=action, font=ctk.CTkFont(size=10), text_color="#dc2626").pack(side="left", padx=(20, 0))
                ctk.CTkLabel(row, text=date, font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack(side="right")
                
                # Action button
                if status == "⚠️":
                    ctk.CTkButton(item_frame, text="Xử lý", width=70, height=25, fg_color="#dc2626", font=ctk.CTkFont(size=9)).pack(side="right", padx=15)
        
        # Quick actions
        quick_actions = ctk.CTkFrame(content_frame, height=60, fg_color=COLORS['background'])
        quick_actions.pack(fill="x", pady=20)
        quick_actions.pack_propagate(False)
        
        ctk.CTkLabel(quick_actions, text="⚡ Thao tác nhanh", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        quick_buttons = ctk.CTkFrame(quick_actions, fg_color="transparent")
        quick_buttons.pack()
        
        ctk.CTkButton(quick_buttons, text="➕ Thêm BHXH", width=130, fg_color=COLORS['success']).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="✏️ Điều chỉnh", width=130, fg_color=COLORS['warning']).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="💫 Chấm dứt", width=130, fg_color=COLORS['error']).pack(side="left", padx=10)
        
        # Export section
        export_frame = ctk.CTkFrame(content_frame, height=80)
        export_frame.pack(fill="x", pady=20)
        export_frame.pack_propagate(False)
        
        export_title = ctk.CTkLabel(export_frame, text="📤 Xuất báo cáo BHXH", font=ctk.CTkFont(size=14, weight="bold"))
        export_title.pack(pady=10)
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack()
        
        ctk.CTkButton(export_buttons, text="📈 Báo cáo tháng", width=140, fg_color="#dc2626").pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📊 Excel tổng hợp", width=140, fg_color=COLORS['success']).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text="📋 Tờ khai BHXH", width=140, fg_color=COLORS['primary']).pack(side="left", padx=10)
    
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
