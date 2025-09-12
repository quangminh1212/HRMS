#!/usr/bin/env python3
"""
Script chạy HRMS với NiceGUI
Giao diện web hiện đại với Tailwind CSS
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Cài đặt dependencies cần thiết"""
    print("🔧 Đang cài đặt NiceGUI và dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "nicegui>=1.4.21"], check=True)
        print("✅ Đã cài đặt NiceGUI thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt NiceGUI: {e}")
        return False

def main():
    """Chạy ứng dụng HRMS với NiceGUI"""
    
    print("=" * 60)
    print("🚀 HRMS - Hệ thống Quản lý Nhân sự (NiceGUI Version)")
    print("=" * 60)
    print("✨ Giao diện web hiện đại với Tailwind CSS")
    print("🎯 Real-time updates và responsive design")
    print("=" * 60)
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:8090")
    print("👤 Tài khoản: admin / admin123")
    print("=" * 60)
    print("⚠️  Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    # Kiểm tra xem nicegui đã được cài đặt chưa
    try:
        import nicegui
        print("✅ NiceGUI đã sẵn sàng")
    except ImportError:
        print("❌ Chưa cài đặt NiceGUI")
        if not install_dependencies():
            sys.exit(1)
    
    # Chạy ứng dụng NiceGUI
    try:
        print("🎉 Đang khởi động HRMS NiceGUI...")
        print("🌐 Giao diện sẽ tự động mở trong trình duyệt")
        
        # Import và chạy app
        from app_nicegui import main as nicegui_main
        nicegui_main()
        
    except KeyboardInterrupt:
        print("\n👋 HRMS NiceGUI đã dừng")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy HRMS NiceGUI: {e}")
        print("💡 Hướng dẫn khắc phục:")
        print("   - Kiểm tra port 8090 có bị chiếm không")
        print("   - Chạy lại script với quyền admin")
        print("   - Cài đặt lại dependencies: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
