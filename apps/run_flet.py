#!/usr/bin/env python3
"""
Script chạy HRMS với Flet (Flutter for Python)
Giao diện hiện đại và đẹp mắt
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Cài đặt dependencies cần thiết"""
    print("🔧 Đang cài đặt Flet và dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "flet>=0.21.2"], check=True)
        print("✅ Đã cài đặt Flet thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt Flet: {e}")
        return False

def main():
    """Chạy ứng dụng HRMS với Flet"""
    
    print("=" * 60)
    print("🚀 HRMS - Hệ thống Quản lý Nhân sự (Flet Version)")
    print("=" * 60)
    print("✨ Giao diện hiện đại với Flutter Components")
    print("🎯 100% Python với UI đẹp như Flutter")
    print("=" * 60)
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:8080")
    print("👤 Tài khoản: admin / admin123")
    print("=" * 60)
    print("⚠️  Nhấn Ctrl+C để dừng ứng dụng")
    print("=" * 60)
    
    # Kiểm tra xem flet đã được cài đặt chưa
    try:
        import flet
        print("✅ Flet đã sẵn sàng")
    except ImportError:
        print("❌ Chưa cài đặt Flet")
        if not install_dependencies():
            sys.exit(1)
    
    # Chạy ứng dụng Flet
    try:
        print("🎉 Đang khởi động HRMS Flet...")
        print("📱 Giao diện sẽ tự động mở trong trình duyệt")
        
        # Import và chạy app
        from app_flet import main as flet_main
        import flet as ft
        
        ft.app(
            target=flet_main,
            view=ft.AppView.WEB_BROWSER,
            port=8080,
            host="localhost",
            web_renderer=ft.WebRenderer.HTML
        )
        
    except KeyboardInterrupt:
        print("\n👋 HRMS Flet đã dừng")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy HRMS Flet: {e}")
        print("💡 Hướng dẫn khắc phục:")
        print("   - Kiểm tra port 8080 có bị chiếm không")
        print("   - Chạy lại script với quyền admin")
        print("   - Cài đặt lại dependencies: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
