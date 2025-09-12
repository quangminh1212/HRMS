#!/usr/bin/env python3
"""
Script chạy HRMS Modern - Giao diện được thiết kế lại hoàn toàn
Tham khảo Material Design 3, Fluent Design, Ant Design
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Chạy ứng dụng HRMS Modern"""
    
    print("=" * 70)
    print("⚡ XLAB HRMS - HỆ THỐNG QUẢN LÝ NHÂN SỰ")  
    print("=" * 70)
    print("✨ Giao diện hiện đại với XLAB Design System")
    print("🎨 Tham khảo XLAB Style, Material Design 3, Clean Architecture")
    print("🏗️ Component System chuyên nghiệp với Clean White Theme")
    print("💎 Modern Teal Accents & Micro-animations")
    print("=" * 70)
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:8501")
    print("👤 Tài khoản: admin / admin123")
    print("=" * 70)
    print("⚠️  Nhấn Ctrl+C để dừng server")
    print("=" * 70)
    
    # Kiểm tra dependencies
    try:
        import streamlit
        import plotly
        print("✅ Dependencies đã sẵn sàng")
    except ImportError:
        print("❌ Chưa đủ dependencies")
        print("🔧 Đang cài đặt dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Chạy ứng dụng Modern HRMS
    try:
        print("🎉 Đang khởi động HRMS Modern...")
        print("💎 Trải nghiệm giao diện đẹp nhất từ trước tới nay!")
        
        # Sử dụng subprocess để chạy streamlit run
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0", 
            "--browser.gatherUsageStats", "false",
            "--theme.primaryColor", "#6750A4",
            "--theme.backgroundColor", "#FFFFFF",
            "--theme.secondaryBackgroundColor", "#F3EDF7",
            "--theme.textColor", "#1C1B1F"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 HRMS Modern đã dừng")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy HRMS Modern: {e}")
        print("💡 Hướng dẫn khắc phục:")
        print("   - Kiểm tra port 8501 có bị chiếm không")
        print("   - Chạy lại script với quyền admin")
        print("   - Cài đặt lại dependencies: pip install -r requirements.txt")
        print("   - Đảm bảo file design.py tồn tại")
        sys.exit(1)

if __name__ == "__main__":
    main()
