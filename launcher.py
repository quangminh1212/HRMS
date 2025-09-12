#!/usr/bin/env python3
"""
HRMS Launcher - Chọn giao diện yêu thích
Hỗ trợ nhiều framework UI hiện đại cho Python
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """In banner đẹp"""
    print("=" * 70)
    print("🏢 HRMS - HỆ THỐNG QUẢN LÝ NHÂN SỰ 🏢")
    print("=" * 70)
    print("🌟 Chọn giao diện yêu thích của bạn:")
    print()

def print_ui_options():
    """In các lựa chọn UI"""
    options = [
        {
            "num": "1", 
            "name": "HRMS Modern (NEW)", 
            "icon": "💎",
            "desc": "Giao diện thiết kế lại hoàn toàn, Material Design 3",
            "pros": "✅ Đẹp nhất, Design System chuyên nghiệp, Component-based",
            "cons": "⚠️ Phiên bản mới, cần feedback"
        },
        {
            "num": "2", 
            "name": "Streamlit (Classic)", 
            "icon": "🌐",
            "desc": "Web app với CSS hiện đại, glassmorphism",
            "pros": "✅ Ổn định, dễ sử dụng, responsive",
            "cons": "⚠️ Giao diện cũ hơn"
        },
        {
            "num": "3", 
            "name": "Flet (Flutter)", 
            "icon": "📱",
            "desc": "Giao diện đẹp như Flutter, hiện đại nhất",
            "pros": "✅ UI tuyệt đẹp, animations mượt, cross-platform",
            "cons": "⚠️ Tương đối mới, cần học thêm"
        },
        {
            "num": "4", 
            "name": "CustomTkinter", 
            "icon": "💻",
            "desc": "Desktop app hiện đại, giống macOS/Windows",
            "pros": "✅ Native desktop, nhanh, theme đẹp",
            "cons": "⚠️ Chỉ desktop, không web"
        },
        {
            "num": "5", 
            "name": "NiceGUI", 
            "icon": "✨",
            "desc": "Web UI hiện đại với Tailwind CSS",
            "pros": "✅ Rất đẹp, Tailwind built-in, real-time",
            "cons": "⚠️ Mới, ecosystem nhỏ"
        },
        {
            "num": "6", 
            "name": "Gradio", 
            "icon": "🎯",
            "desc": "Tối ưu cho data science interface",
            "pros": "✅ Cực kỳ dễ dùng, components sẵn có",
            "cons": "⚠️ Ít tùy biến giao diện"
        }
    ]
    
    for opt in options:
        print(f"{opt['icon']} [{opt['num']}] {opt['name']}")
        print(f"    📝 {opt['desc']}")
        print(f"    {opt['pros']}")
        print(f"    {opt['cons']}")
        print()

def install_framework(framework):
    """Cài đặt framework được chọn"""
    print(f"🔧 Đang cài đặt {framework}...")
    
    packages = {
        "flet": "flet>=0.21.2",
        "customtkinter": "customtkinter>=5.2.0", 
        "nicegui": "nicegui>=1.4.21",
        "gradio": "gradio>=4.15.0",
        "streamlit": "streamlit>=1.28.1"
    }
    
    if framework in packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", packages[framework]
            ], check=True)
            print(f"✅ Đã cài đặt {framework} thành công!")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Lỗi khi cài đặt {framework}")
            return False
    return False

def run_modern():
    """Chạy phiên bản HRMS Modern"""
    print("🚀 Khởi động HRMS Modern...")
    try:
        subprocess.run([sys.executable, "run.py"])
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def run_streamlit():
    """Chạy phiên bản Streamlit Classic"""
    print("🚀 Khởi động HRMS với Streamlit Classic...")
    try:
        subprocess.run([sys.executable, "run_classic.py"])
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def run_flet():
    """Chạy phiên bản Flet"""
    print("🚀 Khởi động HRMS với Flet...")
    try:
        subprocess.run([sys.executable, "run_flet.py"])
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def create_customtkinter_app():
    """Tạo app CustomTkinter (placeholder)"""
    print("🚧 CustomTkinter version đang được phát triển...")
    print("📝 Sẽ có trong phiên bản tiếp theo")
    input("\nNhấn Enter để quay lại menu...")

def run_nicegui():
    """Chạy phiên bản NiceGUI"""
    print("🚀 Khởi động HRMS với NiceGUI...")
    try:
        subprocess.run([sys.executable, "run_nicegui.py"])
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def create_gradio_app():
    """Tạo app Gradio (placeholder)"""
    print("🚧 Gradio version đang được phát triển...")
    print("📝 Sẽ có trong phiên bản tiếp theo") 
    input("\nNhấn Enter để quay lại menu...")

def main():
    """Main launcher function"""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner()
        print_ui_options()
        
        print("🎮 Các tùy chọn khác:")
        print("📦 [7] Cài đặt tất cả frameworks")
        print("🔧 [8] Kiểm tra dependencies")
        print("❌ [0] Thoát")
        print()
        
        choice = input("👉 Chọn giao diện (1-8, 0 để thoát): ").strip()
        
        if choice == "0":
            print("👋 Tạm biệt! Cảm ơn bạn đã sử dụng HRMS!")
            break
            
        elif choice == "1":
            print("\n💎 Bạn đã chọn HRMS Modern!")
            print("🎨 Giao diện thiết kế lại hoàn toàn với Material Design 3")
            print("✨ Component System chuyên nghiệp & Design Tokens")
            input("\nNhấn Enter để khởi động...")
            run_modern()
            
        elif choice == "2":
            print("\n🌐 Bạn đã chọn Streamlit Classic!")
            print("💫 Giao diện web ổn định với glassmorphism effect")
            input("\nNhấn Enter để khởi động...")
            run_streamlit()
            
        elif choice == "3":
            print("\n📱 Bạn đã chọn Flet!")
            print("🎨 Giao diện đẹp nhất với Flutter components")
            input("\nNhấn Enter để khởi động...")
            run_flet()
            
        elif choice == "4":
            print("\n💻 Bạn đã chọn CustomTkinter!")
            create_customtkinter_app()
            
        elif choice == "5":
            print("\n✨ Bạn đã chọn NiceGUI!")
            print("🎨 Giao diện web hiện đại với Tailwind CSS")
            input("\nNhấn Enter để khởi động...")
            run_nicegui()
            
        elif choice == "6":
            print("\n🎯 Bạn đã chọn Gradio!")
            create_gradio_app()
            
        elif choice == "7":
            print("\n📦 Cài đặt tất cả frameworks...")
            frameworks = ["streamlit", "flet", "customtkinter", "nicegui", "gradio"]
            
            for fw in frameworks:
                install_framework(fw)
                
            print("\n✅ Hoàn tất cài đặt!")
            input("Nhấn Enter để tiếp tục...")
            
        elif choice == "8":
            print("\n🔧 Kiểm tra dependencies...")
            
            # Kiểm tra Python version
            print(f"🐍 Python: {sys.version}")
            
            # Kiểm tra các package
            packages = ["streamlit", "flet", "customtkinter", "nicegui", "gradio", "plotly", "pandas"]
            
            for pkg in packages:
                try:
                    __import__(pkg)
                    print(f"✅ {pkg}: Đã cài đặt")
                except ImportError:
                    print(f"❌ {pkg}: Chưa cài đặt")
            
            input("\nNhấn Enter để tiếp tục...")
            
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để thử lại...")

if __name__ == "__main__":
    main()
