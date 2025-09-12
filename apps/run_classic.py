#!/usr/bin/env python3
"""
Script chạy HRMS với Streamlit
Frontend và Backend 100% Python
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Chạy ứng dụng Streamlit HRMS"""
    
    print("=" * 60)
    print("🚀 HRMS - Hệ thống Quản lý Nhân sự (Streamlit Version)")
    print("=" * 60)
    print("✨ Frontend & Backend 100% Python")
    print("🎯 Đáp ứng đầy đủ 11 yêu cầu nghiệp vụ")
    print("=" * 60)
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:3000")
    print("👤 Tài khoản: admin / admin123")
    print("=" * 60)
    print("⚠️  Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    # Kiểm tra xem streamlit đã được cài đặt chưa
    try:
        import streamlit
        print("✅ Streamlit đã sẵn sàng")
    except ImportError:
        print("❌ Chưa cài đặt Streamlit")
        print("🔧 Đang cài đặt dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Chạy ứng dụng Streamlit
    try:
        # Sử dụng subprocess để chạy streamlit run
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app_classic.py",
            "--server.port", "3000",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 HRMS server đã dừng")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy HRMS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
