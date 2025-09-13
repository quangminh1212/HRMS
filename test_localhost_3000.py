#!/usr/bin/env python3
"""
Test localhost:3000 with Playwright
Kiểm tra HRMS Modern có hoạt động đúng không
"""

import asyncio
import time
from playwright.async_api import async_playwright
import requests


def check_server_status():
    """Kiểm tra server có đang chạy không."""
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ Server response: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server không phản hồi - Connection refused")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server timeout")
        return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra server: {e}")
        return False


async def test_hrms_with_playwright():
    """Test HRMS với Playwright."""
    print("🎭 Bắt đầu test với Playwright...")
    
    async with async_playwright() as p:
        try:
            # Launch browser
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            print("🌐 Đang truy cập http://localhost:3000...")
            
            # Navigate to localhost:3000
            try:
                await page.goto("http://localhost:3000", timeout=30000)
                print("✅ Đã load trang thành công")
            except Exception as e:
                print(f"❌ Không thể load trang: {e}")
                await browser.close()
                return False
            
            # Wait for page to load
            await page.wait_for_timeout(3000)
            
            # Take screenshot
            await page.screenshot(path="hrms_test_screenshot.png")
            print("📸 Đã chụp screenshot: hrms_test_screenshot.png")
            
            # Check page title
            title = await page.title()
            print(f"📄 Page title: {title}")
            
            # Check if login form exists
            try:
                login_form = await page.wait_for_selector("form", timeout=5000)
                if login_form:
                    print("✅ Tìm thấy login form")
                    
                    # Try to find username and password fields
                    username_field = await page.query_selector("input[type='text']")
                    password_field = await page.query_selector("input[type='password']")
                    
                    if username_field and password_field:
                        print("✅ Tìm thấy username và password fields")
                        
                        # Try login
                        await username_field.fill("admin")
                        await password_field.fill("admin123")
                        print("✅ Đã nhập thông tin đăng nhập")
                        
                        # Find and click login button
                        login_button = await page.query_selector("button[type='submit']")
                        if login_button:
                            await login_button.click()
                            print("✅ Đã click nút đăng nhập")
                            
                            # Wait for navigation
                            await page.wait_for_timeout(3000)
                            
                            # Take screenshot after login
                            await page.screenshot(path="hrms_after_login.png")
                            print("📸 Screenshot sau đăng nhập: hrms_after_login.png")
                            
                        else:
                            print("❌ Không tìm thấy nút đăng nhập")
                    else:
                        print("❌ Không tìm thấy username/password fields")
                else:
                    print("❌ Không tìm thấy login form")
            except Exception as e:
                print(f"⚠️ Lỗi khi tìm login form: {e}")
            
            # Check for any error messages on page
            try:
                error_elements = await page.query_selector_all(".stAlert, .error, [data-testid='stAlert']")
                if error_elements:
                    for i, error in enumerate(error_elements):
                        error_text = await error.text_content()
                        print(f"⚠️ Error message {i+1}: {error_text}")
                else:
                    print("✅ Không có error messages")
            except Exception as e:
                print(f"⚠️ Lỗi khi kiểm tra error messages: {e}")
            
            # Get page content for debugging
            content = await page.content()
            if "streamlit" in content.lower():
                print("✅ Streamlit app đã load")
            else:
                print("❌ Không phải Streamlit app hoặc chưa load đúng")
            
            await browser.close()
            print("✅ Test hoàn thành")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi trong quá trình test: {e}")
            try:
                await browser.close()
            except:
                pass
            return False


async def main():
    """Main function."""
    print("🧪 HRMS Localhost:3000 Test với Playwright")
    print("=" * 50)
    
    # Check server first
    print("1. Kiểm tra server status...")
    if not check_server_status():
        print("❌ Server không hoạt động. Vui lòng chạy run.bat trước.")
        return
    
    # Wait a bit for server to be ready
    print("2. Đợi server sẵn sàng...")
    time.sleep(3)
    
    # Test with Playwright
    print("3. Test với Playwright...")
    success = await test_hrms_with_playwright()
    
    if success:
        print("\n🎉 Test thành công!")
        print("📸 Kiểm tra screenshots để xem giao diện")
    else:
        print("\n❌ Test thất bại!")
        print("💡 Kiểm tra lại server và cấu hình")


if __name__ == "__main__":
    asyncio.run(main())
