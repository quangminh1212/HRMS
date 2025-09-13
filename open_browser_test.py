#!/usr/bin/env python3
"""
Mở browser để test localhost:3000 trực tiếp
"""

import webbrowser
import time
import requests


def check_server():
    """Kiểm tra server."""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"✅ Server OK - Status: {response.status_code}")
        return True
    except:
        print("❌ Server không phản hồi")
        return False


def main():
    """Main function."""
    print("🌐 Test localhost:3000 bằng browser")
    print("=" * 40)
    
    if check_server():
        print("🚀 Mở browser...")
        webbrowser.open("http://localhost:3000")
        print("✅ Browser đã mở!")
        print("👀 Kiểm tra browser để xem app có hoạt động không")
    else:
        print("❌ Server chưa chạy")


if __name__ == "__main__":
    main()
