#!/usr/bin/env python3
"""
HRMS - Hệ thống Quản lý Nhân sự (Flet Version)
Giao diện hiện đại với Flutter Components
"""

import flet as ft
from datetime import datetime, date
import sqlite3
import pandas as pd

class HRMSApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        self.current_page = "dashboard"
        self.setup_page()
        
    def setup_page(self):
        """Thiết lập cấu hình trang"""
        self.page.title = "HRMS - Hệ thống Quản lý Nhân sự"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.window_min_width = 1200
        self.page.window_min_height = 800
        self.page.padding = 0
        self.page.spacing = 0
        
        # Theme tùy chỉnh
        self.page.theme = ft.Theme(
            primary_swatch=ft.colors.INDIGO,
            color_scheme_seed=ft.colors.INDIGO,
        )
        
        self.show_login()
    
    def show_login(self):
        """Hiển thị màn hình đăng nhập"""
        self.page.clean()
        
        # Container chính với gradient background
        main_container = ft.Container(
            width=self.page.window_width,
            height=self.page.window_height,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.colors.INDIGO_400,
                    ft.colors.PURPLE_400,
                    ft.colors.PINK_300,
                ]
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                main_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Logo và tiêu đề
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.icons.BUSINESS_ROUNDED,
                                    size=80,
                                    color=ft.colors.WHITE
                                ),
                                ft.Text(
                                    "HRMS",
                                    size=48,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.WHITE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "Hệ thống Quản lý Nhân sự",
                                    size=18,
                                    color=ft.colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ]
                        ),
                        margin=ft.margin.only(bottom=40)
                    ),
                    
                    # Form đăng nhập
                    ft.Container(
                        width=400,
                        padding=ft.padding.all(40),
                        bgcolor=ft.colors.WHITE,
                        border_radius=20,
                        shadow=ft.BoxShadow(
                            spread_radius=2,
                            blur_radius=20,
                            color=ft.colors.BLACK12
                        ),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Đăng nhập",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.GREY_800
                                ),
                                ft.Container(height=20),
                                
                                # Username field
                                ft.TextField(
                                    label="Tên đăng nhập",
                                    hint_text="admin",
                                    prefix_icon=ft.icons.PERSON,
                                    border_radius=10,
                                    filled=True,
                                    bgcolor=ft.colors.GREY_50,
                                    ref=ft.Ref[ft.TextField]()
                                ),
                                
                                # Password field  
                                ft.TextField(
                                    label="Mật khẩu",
                                    hint_text="••••••••",
                                    prefix_icon=ft.icons.LOCK,
                                    password=True,
                                    border_radius=10,
                                    filled=True,
                                    bgcolor=ft.colors.GREY_50,
                                    ref=ft.Ref[ft.TextField]()
                                ),
                                
                                ft.Container(height=20),
                                
                                # Login button
                                ft.ElevatedButton(
                                    text="Đăng nhập",
                                    width=300,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.INDIGO_400,
                                        color=ft.colors.WHITE,
                                        text_style=ft.TextStyle(
                                            size=16,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=self.handle_login
                                ),
                                
                                ft.Container(height=20),
                                
                                # Thông tin đăng nhập
                                ft.Container(
                                    padding=ft.padding.all(15),
                                    bgcolor=ft.colors.BLUE_50,
                                    border_radius=10,
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Tài khoản demo:",
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.colors.BLUE_800
                                            ),
                                            ft.Text("👤 Username: admin", color=ft.colors.BLUE_700),
                                            ft.Text("🔒 Password: admin123", color=ft.colors.BLUE_700),
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        
        self.page.add(main_container)
        self.username_field = main_container.content.controls[1].content.controls[2]
        self.password_field = main_container.content.controls[1].content.controls[3]
    
    def handle_login(self, e):
        """Xử lý đăng nhập"""
        username = self.username_field.value or ""
        password = self.password_field.value or ""
        
        if username == "admin" and password == "admin123":
            self.current_user = username
            self.show_main_app()
        else:
            self.show_error_dialog("Tên đăng nhập hoặc mật khẩu không đúng!")
    
    def show_error_dialog(self, message):
        """Hiển thị dialog lỗi"""
        dialog = ft.AlertDialog(
            title=ft.Text("Lỗi"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.dialog.close())
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_main_app(self):
        """Hiển thị ứng dụng chính"""
        self.page.clean()
        
        # AppBar hiện đại
        self.page.appbar = ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.BUSINESS_ROUNDED, color=ft.colors.WHITE),
                    ft.Text("HRMS", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                ]
            ),
            bgcolor=ft.colors.INDIGO_600,
            color=ft.colors.WHITE,
            actions=[
                ft.IconButton(
                    icon=ft.icons.NOTIFICATIONS,
                    icon_color=ft.colors.WHITE,
                    badge=ft.Badge(
                        content=ft.Text("3", color=ft.colors.WHITE, size=12),
                        bgcolor=ft.colors.RED_400
                    )
                ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Thông tin tài khoản"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(text="Đăng xuất", on_click=self.handle_logout),
                    ],
                    content=ft.Row(
                        controls=[
                            ft.Text(f"Xin chào, {self.current_user}", color=ft.colors.WHITE),
                            ft.Icon(ft.icons.ACCOUNT_CIRCLE, color=ft.colors.WHITE)
                        ]
                    )
                )
            ]
        )
        
        # Navigation Rail hiện đại
        nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            bgcolor=ft.colors.GREY_50,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label="Trang chủ"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINE,
                    selected_icon=ft.icons.PEOPLE,
                    label="Nhân sự"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PAYMENTS_OUTLINED,
                    selected_icon=ft.icons.PAYMENTS,
                    label="Lương"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SCHEDULE_OUTLINED,
                    selected_icon=ft.icons.SCHEDULE,
                    label="Nghỉ hưu"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ASSIGNMENT_OUTLINED,
                    selected_icon=ft.icons.ASSIGNMENT,
                    label="Quy hoạch"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.DESCRIPTION_OUTLINED,
                    selected_icon=ft.icons.DESCRIPTION,
                    label="Hợp đồng"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.icons.ANALYTICS,
                    label="Báo cáo"
                ),
            ],
            on_change=self.handle_nav_change
        )
        
        # Content area
        self.content_area = ft.Container(
            expand=True,
            padding=ft.padding.all(20),
            content=self.create_dashboard()
        )
        
        # Main layout
        main_row = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1),
                self.content_area
            ]
        )
        
        self.page.add(main_row)
    
    def handle_nav_change(self, e):
        """Xử lý thay đổi navigation"""
        pages = ["dashboard", "employees", "salary", "retirement", "planning", "contracts", "reports"]
        self.current_page = pages[e.control.selected_index]
        self.update_content()
    
    def update_content(self):
        """Cập nhật nội dung theo trang được chọn"""
        if self.current_page == "dashboard":
            content = self.create_dashboard()
        elif self.current_page == "employees":
            content = self.create_employees_page()
        elif self.current_page == "salary":
            content = self.create_salary_page()
        else:
            content = ft.Text(f"Trang {self.current_page} đang phát triển...")
        
        self.content_area.content = content
        self.page.update()
    
    def create_dashboard(self):
        """Tạo dashboard chính"""
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                # Header
                ft.Container(
                    content=ft.Text(
                        "📊 Bảng điều khiển",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREY_800
                    ),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Metrics cards
                ft.Row(
                    controls=[
                        self.create_metric_card("👥", "Tổng nhân sự", "150", "+5", ft.colors.BLUE_400),
                        self.create_metric_card("⏰", "Sắp nghỉ hưu", "12", "-2", ft.colors.ORANGE_400),
                        self.create_metric_card("💰", "Đến kỳ nâng lương", "25", "+8", ft.colors.GREEN_400),
                        self.create_metric_card("📄", "Hợp đồng hết hạn", "6", "+1", ft.colors.RED_400),
                    ]
                ),
                
                ft.Container(height=30),
                
                # Charts section
                ft.Row(
                    expand=True,
                    controls=[
                        # Biểu đồ cơ cấu tuổi
                        ft.Container(
                            expand=1,
                            height=400,
                            padding=ft.padding.all(20),
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.colors.BLACK12
                            ),
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "📊 Cơ cấu theo độ tuổi",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Container(
                                        expand=True,
                                        content=ft.Text("Biểu đồ sẽ được hiển thị ở đây")
                                    )
                                ]
                            )
                        ),
                        
                        ft.Container(width=20),
                        
                        # Biểu đồ giới tính
                        ft.Container(
                            expand=1,
                            height=400,
                            padding=ft.padding.all(20),
                            bgcolor=ft.colors.WHITE,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.colors.BLACK12
                            ),
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "🎯 Cơ cấu theo giới tính",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Container(
                                        expand=True,
                                        content=ft.Text("Biểu đồ sẽ được hiển thị ở đây")
                                    )
                                ]
                            )
                        )
                    ]
                ),
                
                ft.Container(height=30),
                
                # Alerts section
                ft.Container(
                    width=self.page.window_width,
                    padding=ft.padding.all(20),
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.colors.BLACK12
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "⚠️ Cảnh báo và nhắc nhở",
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=15),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        expand=1,
                                        padding=ft.padding.all(15),
                                        bgcolor=ft.colors.ORANGE_50,
                                        border_radius=10,
                                        border=ft.border.all(2, ft.colors.ORANGE_200),
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "⚡ Nâng lương sắp tới",
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.colors.ORANGE_800
                                                ),
                                                ft.Text(
                                                    "25 nhân viên đủ điều kiện nâng lương trong quý này",
                                                    color=ft.colors.ORANGE_700
                                                ),
                                                ft.Text(
                                                    "📅 Cần xử lý trước ngày 15/12/2024",
                                                    size=12,
                                                    color=ft.colors.ORANGE_600,
                                                    italic=True
                                                ),
                                            ]
                                        )
                                    ),
                                    ft.Container(width=20),
                                    ft.Container(
                                        expand=1,
                                        padding=ft.padding.all(15),
                                        bgcolor=ft.colors.BLUE_50,
                                        border_radius=10,
                                        border=ft.border.all(2, ft.colors.BLUE_200),
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "🏖️ Nghỉ hưu",
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.colors.BLUE_800
                                                ),
                                                ft.Text(
                                                    "12 nhân viên sẽ nghỉ hưu trong 6 tháng tới",
                                                    color=ft.colors.BLUE_700
                                                ),
                                                ft.Text(
                                                    "📋 Cần chuẩn bị thủ tục và hồ sơ",
                                                    size=12,
                                                    color=ft.colors.BLUE_600,
                                                    italic=True
                                                ),
                                            ]
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    
    def create_metric_card(self, icon, title, value, change, color):
        """Tạo metric card"""
        return ft.Container(
            expand=1,
            height=120,
            padding=ft.padding.all(20),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.BLACK12
            ),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=60,
                        height=60,
                        bgcolor=color,
                        border_radius=30,
                        content=ft.Text(
                            icon,
                            size=24,
                            text_align=ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=15),
                    ft.Column(
                        expand=True,
                        main_alignment=ft.MainAxisAlignment.CENTER,
                        cross_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(title, size=14, color=ft.colors.GREY_600),
                            ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                change,
                                size=12,
                                color=ft.colors.GREEN_600 if change.startswith("+") else ft.colors.RED_600
                            )
                        ]
                    )
                ]
            )
        )
    
    def create_employees_page(self):
        """Tạo trang tra cứu nhân sự"""
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text(
                    "👥 Tra cứu thông tin nhân sự",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.GREY_800
                ),
                ft.Container(height=20),
                
                # Search section
                ft.Container(
                    padding=ft.padding.all(20),
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.colors.BLACK12
                    ),
                    content=ft.Column(
                        controls=[
                            ft.TextField(
                                label="Tìm kiếm nhân viên",
                                hint_text="VD: Nguyễn Văn A",
                                prefix_icon=ft.icons.SEARCH,
                                border_radius=10,
                                filled=True,
                                bgcolor=ft.colors.GREY_50
                            ),
                            ft.Container(height=10),
                            ft.ElevatedButton(
                                text="🔍 Tìm kiếm",
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.INDIGO_400,
                                    color=ft.colors.WHITE
                                )
                            )
                        ]
                    )
                ),
                
                ft.Container(height=20),
                
                # Results placeholder
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(20),
                    bgcolor=ft.colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.colors.BLACK12
                    ),
                    content=ft.Text("Kết quả tìm kiếm sẽ hiển thị ở đây")
                )
            ]
        )
    
    def create_salary_page(self):
        """Tạo trang quản lý lương"""
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text(
                    "💰 Quản lý nâng lương định kỳ",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.GREY_800
                ),
                ft.Container(height=20),
                ft.Text("Chức năng đang được phát triển..."),
            ]
        )
    
    def handle_logout(self, e):
        """Xử lý đăng xuất"""
        self.current_user = None
        self.show_login()

def main(page: ft.Page):
    """Main function cho Flet app"""
    HRMSApp(page)

if __name__ == "__main__":
    # Chạy ứng dụng Flet
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        port=8080,
        host="localhost"
    )
