#!/usr/bin/env python3
"""
HRMS - Hệ thống Quản lý Nhân sự (NiceGUI Version)
Giao diện web hiện đại với Tailwind CSS
"""

from nicegui import ui, app
from datetime import datetime
import asyncio

class HRMSNiceGUI:
    def __init__(self):
        self.current_user = None
        self.logged_in = False
        
    def create_login_page(self):
        """Tạo trang đăng nhập"""
        ui.colors(primary='#667eea')
        
        with ui.column().classes('w-full h-screen').style('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)'):
            # Spacer
            ui.element('div').classes('flex-grow')
            
            # Login card
            with ui.card().classes('w-96 mx-auto p-8').style('backdrop-filter: blur(10px); background: rgba(255,255,255,0.95)'):
                # Logo và tiêu đề
                with ui.column().classes('items-center mb-8'):
                    ui.icon('business', size='4rem').classes('text-indigo-600 mb-4')
                    ui.label('HRMS').classes('text-4xl font-bold text-gray-800')
                    ui.label('Hệ thống Quản lý Nhân sự').classes('text-gray-600')
                
                # Form inputs
                username = ui.input('Tên đăng nhập', placeholder='admin').classes('w-full mb-4')
                username.props('outlined dense')
                
                password = ui.input('Mật khẩu', placeholder='admin123', password=True).classes('w-full mb-6')
                password.props('outlined dense')
                
                # Login button
                ui.button('Đăng nhập', 
                         on_click=lambda: self.handle_login(username.value, password.value)
                ).classes('w-full bg-indigo-600 text-white py-3 text-lg font-semibold rounded-lg hover:bg-indigo-700 transition-colors')
                
                # Demo info
                with ui.card().classes('mt-6 p-4 bg-blue-50 border-l-4 border-blue-400'):
                    ui.label('Tài khoản demo:').classes('font-bold text-blue-800')
                    ui.label('👤 Username: admin').classes('text-blue-700')
                    ui.label('🔒 Password: admin123').classes('text-blue-700')
            
            # Spacer
            ui.element('div').classes('flex-grow')
    
    def handle_login(self, username: str, password: str):
        """Xử lý đăng nhập"""
        if username == 'admin' and password == 'admin123':
            self.current_user = username
            self.logged_in = True
            ui.navigate.to('/dashboard')
        else:
            ui.notify('Tên đăng nhập hoặc mật khẩu không đúng!', color='negative')
    
    def create_dashboard(self):
        """Tạo dashboard chính"""
        with ui.header().classes('bg-indigo-600 text-white shadow-lg'):
            with ui.row().classes('w-full items-center'):
                ui.icon('business').classes('mr-2')
                ui.label('HRMS').classes('text-xl font-bold')
                ui.space()
                
                # Notifications
                ui.badge('3', color='red').props('floating').with_(
                    ui.button(icon='notifications').props('flat round color=white')
                )
                
                # User menu
                with ui.button(f'Chào {self.current_user}', icon='account_circle').props('flat color=white'):
                    with ui.menu():
                        ui.menu_item('Thông tin tài khoản', lambda: None)
                        ui.menu_item('Đăng xuất', lambda: self.handle_logout())
        
        # Sidebar navigation
        with ui.left_drawer().classes('bg-gray-50').props('width=250'):
            with ui.column().classes('p-4'):
                ui.label('Menu chính').classes('text-lg font-bold text-gray-800 mb-4')
                
                nav_items = [
                    ('dashboard', '🏠 Trang chủ'),
                    ('employees', '👥 Nhân sự'),
                    ('salary', '💰 Lương'),
                    ('retirement', '⏰ Nghỉ hưu'),
                    ('planning', '📋 Quy hoạch'),
                    ('contracts', '📄 Hợp đồng'),
                    ('reports', '📊 Báo cáo'),
                ]
                
                for route, label in nav_items:
                    ui.button(label, on_click=lambda r=route: ui.navigate.to(f'/{r}')).classes(
                        'w-full justify-start mb-2 text-gray-700 hover:bg-indigo-100 hover:text-indigo-700'
                    ).props('flat')
        
        # Main content
        with ui.column().classes('p-6 space-y-6'):
            # Page title
            ui.label('📊 Bảng điều khiển').classes('text-3xl font-bold text-gray-800 mb-6')
            
            # Metric cards
            with ui.row().classes('w-full gap-6'):
                self.create_metric_card('👥', 'Tổng nhân sự', '150', '+5', 'text-blue-600 bg-blue-100')
                self.create_metric_card('⏰', 'Sắp nghỉ hưu', '12', '-2', 'text-orange-600 bg-orange-100')
                self.create_metric_card('💰', 'Đến kỳ nâng lương', '25', '+8', 'text-green-600 bg-green-100')
                self.create_metric_card('📄', 'Hợp đồng hết hạn', '6', '+1', 'text-red-600 bg-red-100')
            
            # Charts section
            with ui.row().classes('w-full gap-6 mt-8'):
                # Chart 1
                with ui.card().classes('flex-1 p-6'):
                    ui.label('📊 Cơ cấu theo độ tuổi').classes('text-xl font-bold mb-4')
                    ui.label('Biểu đồ sẽ được hiển thị ở đây').classes('text-gray-500')
                
                # Chart 2  
                with ui.card().classes('flex-1 p-6'):
                    ui.label('🎯 Cơ cấu theo giới tính').classes('text-xl font-bold mb-4')
                    ui.label('Biểu đồ sẽ được hiển thị ở đây').classes('text-gray-500')
            
            # Alerts section
            with ui.card().classes('w-full p-6 mt-8'):
                ui.label('⚠️ Cảnh báo và nhắc nhở').classes('text-xl font-bold mb-4')
                
                with ui.row().classes('w-full gap-6'):
                    # Warning 1
                    with ui.card().classes('flex-1 p-4 border-l-4 border-orange-400 bg-orange-50'):
                        ui.label('⚡ Nâng lương sắp tới').classes('font-bold text-orange-800 mb-2')
                        ui.label('25 nhân viên đủ điều kiện nâng lương trong quý này').classes('text-orange-700 mb-2')
                        ui.label('📅 Cần xử lý trước ngày 15/12/2024').classes('text-sm text-orange-600 italic')
                    
                    # Warning 2
                    with ui.card().classes('flex-1 p-4 border-l-4 border-blue-400 bg-blue-50'):
                        ui.label('🏖️ Nghỉ hưu').classes('font-bold text-blue-800 mb-2')
                        ui.label('12 nhân viên sẽ nghỉ hưu trong 6 tháng tới').classes('text-blue-700 mb-2')
                        ui.label('📋 Cần chuẩn bị thủ tục và hồ sơ').classes('text-sm text-blue-600 italic')
    
    def create_metric_card(self, icon: str, title: str, value: str, change: str, icon_classes: str):
        """Tạo metric card"""
        with ui.card().classes('flex-1 p-6 hover:shadow-lg transition-shadow'):
            with ui.row().classes('items-center'):
                with ui.element('div').classes(f'p-3 rounded-full {icon_classes}'):
                    ui.label(icon).classes('text-2xl')
                
                with ui.column().classes('ml-4 flex-grow'):
                    ui.label(title).classes('text-gray-600 text-sm')
                    ui.label(value).classes('text-2xl font-bold text-gray-900')
                    change_color = 'text-green-600' if change.startswith('+') else 'text-red-600'
                    ui.label(change).classes(f'text-sm {change_color}')
    
    def create_employees_page(self):
        """Trang nhân sự"""
        with ui.header().classes('bg-indigo-600 text-white shadow-lg'):
            with ui.row().classes('w-full items-center'):
                ui.icon('business').classes('mr-2')
                ui.label('HRMS').classes('text-xl font-bold')
                ui.space()
                ui.button('Quay lại Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat color=white')
        
        with ui.column().classes('p-6 space-y-6'):
            ui.label('👥 Tra cứu thông tin nhân sự').classes('text-3xl font-bold text-gray-800')
            
            # Search section
            with ui.card().classes('p-6'):
                ui.label('🔍 Tìm kiếm nhân viên').classes('text-xl font-bold mb-4')
                
                with ui.row().classes('w-full gap-4 items-end'):
                    search_input = ui.input('Tên nhân viên', placeholder='VD: Nguyễn Văn A').classes('flex-grow')
                    search_input.props('outlined')
                    
                    ui.button('Tìm kiếm', icon='search', 
                            on_click=lambda: ui.notify(f'Đang tìm kiếm: {search_input.value}')
                    ).classes('bg-indigo-600 text-white')
            
            # Results placeholder
            with ui.card().classes('p-6 flex-grow'):
                ui.label('📋 Kết quả tìm kiếm').classes('text-xl font-bold mb-4')
                ui.label('Kết quả tìm kiếm sẽ hiển thị ở đây...').classes('text-gray-500')
    
    def handle_logout(self):
        """Xử lý đăng xuất"""
        self.current_user = None
        self.logged_in = False
        ui.navigate.to('/login')

# Khởi tạo app
hrms_app = HRMSNiceGUI()

# Routes
@ui.page('/login')
def login_page():
    hrms_app.create_login_page()

@ui.page('/dashboard')
def dashboard_page():
    if not hrms_app.logged_in:
        ui.navigate.to('/login')
        return
    hrms_app.create_dashboard()

@ui.page('/employees')
def employees_page():
    if not hrms_app.logged_in:
        ui.navigate.to('/login')
        return
    hrms_app.create_employees_page()

@ui.page('/salary')
def salary_page():
    if not hrms_app.logged_in:
        ui.navigate.to('/login')
        return
    ui.label('💰 Trang lương đang được phát triển...')

# Redirect root to login
@ui.page('/')
def index():
    ui.navigate.to('/login')

def main():
    """Chạy ứng dụng NiceGUI"""
    print("=" * 60)
    print("🚀 HRMS - Hệ thống Quản lý Nhân sự (NiceGUI)")
    print("=" * 60)
    print("✨ Giao diện web hiện đại với Tailwind CSS")
    print("🎯 Real-time updates và responsive design")
    print("=" * 60)
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:8090")
    print("👤 Tài khoản: admin / admin123")
    print("=" * 60)
    
    ui.run(
        port=8090,
        title='HRMS - Hệ thống Quản lý Nhân sự',
        favicon='🏢',
        dark=False,
        show=True
    )

if __name__ == '__main__':
    main()
