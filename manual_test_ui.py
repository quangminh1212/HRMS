#!/usr/bin/env python3
"""
Manual UI Testing Script for HRMS

Script hướng dẫn test thủ công tất cả các lựa chọn UI
"""

import time
import requests
import subprocess
from pathlib import Path

def test_option(option_num: str, option_name: str, port: int, timeout: int = 30):
    """Test a single UI option manually."""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING OPTION {option_num}: {option_name}")
    print(f"{'='*60}")
    
    print(f"1. Mở Command Prompt mới")
    print(f"2. Chạy: run.bat")
    print(f"3. Chọn option: {option_num}")
    print(f"4. Đợi ứng dụng khởi động...")
    
    input("Nhấn Enter khi đã chạy xong bước trên...")
    
    # Check if port is accessible
    print(f"\n🔍 Kiểm tra port {port}...")
    
    for i in range(timeout):
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Port {port} accessible - {option_name} đang chạy!")
                
                # Open browser
                import webbrowser
                webbrowser.open(f"http://localhost:{port}")
                
                print(f"\n📋 Checklist cho {option_name}:")
                print("  □ Giao diện hiển thị đúng")
                print("  □ Có thể đăng nhập (admin/admin123)")
                print("  □ Menu navigation hoạt động")
                print("  □ Dữ liệu hiển thị đúng")
                
                result = input("\nOption này có hoạt động tốt không? (y/n): ").lower()
                
                if result == 'y':
                    print(f"✅ {option_name} - PASS")
                    return True
                else:
                    print(f"❌ {option_name} - FAIL")
                    return False
                    
        except requests.exceptions.RequestException:
            print(f"⏳ Đang đợi... ({i+1}/{timeout})")
            time.sleep(1)
    
    print(f"❌ {option_name} - Không thể kết nối sau {timeout}s")
    return False

def main():
    """Main testing function."""
    print("🏢 HRMS UI OPTIONS MANUAL TESTING")
    print("="*50)
    print("Script này sẽ hướng dẫn bạn test từng option một cách thủ công")
    print("Đảm bảo không có process nào đang chạy trước khi bắt đầu")
    
    input("\nNhấn Enter để bắt đầu...")
    
    # Test configurations
    options = [
        ("1", "HRMS Modern", 3000),
        ("2", "Quick Start", 3000),
        ("3", "Launcher Menu", 8080),
        ("4", "Streamlit Classic", 8501),
        ("5", "Flet (Flutter UI)", 8550),
        ("6", "NiceGUI (Tailwind)", 8080),
        ("7", "Manual Mode", 3000)
    ]
    
    results = []
    
    for option_num, option_name, port in options:
        try:
            result = test_option(option_num, option_name, port)
            results.append((option_num, option_name, result))
            
            # Ask to continue
            if option_num != "7":  # Not the last option
                continue_test = input(f"\nTiếp tục test option tiếp theo? (y/n): ").lower()
                if continue_test != 'y':
                    break
                    
                print("\n⚠️ Hãy dừng ứng dụng hiện tại trước khi test option tiếp theo")
                input("Nhấn Enter khi đã dừng...")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Test bị dừng bởi người dùng")
            break
        except Exception as e:
            print(f"\n❌ Lỗi khi test {option_name}: {e}")
            results.append((option_num, option_name, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 KẾT QUẢ TEST TỔNG HỢP")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for option_num, option_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"[{option_num}] {option_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Tổng kết:")
    print(f"  Tổng số test: {total}")
    print(f"  Thành công: {passed}")
    print(f"  Thất bại: {total - passed}")
    print(f"  Tỷ lệ thành công: {(passed/total)*100:.1f}%" if total > 0 else "0%")
    
    if passed == total:
        print("\n🎉 Tất cả UI options đều hoạt động tốt!")
    elif passed >= total * 0.7:
        print("\n👍 Phần lớn UI options hoạt động tốt!")
    else:
        print("\n⚠️ Cần kiểm tra và sửa lỗi một số UI options.")

if __name__ == "__main__":
    main()
