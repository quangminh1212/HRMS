#!/usr/bin/env python3
"""
Test HRMS Final - Đợi app load hoàn toàn và test login
"""

import asyncio
import time
from playwright.async_api import async_playwright


async def wait_for_app_ready(page, max_wait=120):
    """Đợi app sẵn sàng hoàn toàn."""
    print("⏳ Đợi HRMS app sẵn sàng...")
    
    for i in range(max_wait):
        try:
            # Kiểm tra xem có "Please wait..." không
            please_wait_elements = await page.query_selector_all("text=Please wait")
            
            if not please_wait_elements:
                # Kiểm tra xem có form đăng nhập không
                login_form = await page.query_selector("form")
                username_input = await page.query_selector("input[type='text']")
                
                if login_form and username_input:
                    print("✅ App đã sẵn sàng với form đăng nhập!")
                    return True
                elif username_input:
                    print("✅ App đã sẵn sàng!")
                    return True
                    
            if i % 10 == 0:  # Print every 10 seconds
                print(f"⏳ Đợi... ({i+1}/{max_wait}s)")
                
            await page.wait_for_timeout(1000)
            
        except Exception as e:
            if i % 20 == 0:  # Print error every 20 seconds
                print(f"⚠️ Lỗi khi kiểm tra (giây {i+1}): {e}")
            await page.wait_for_timeout(1000)
    
    print("❌ Timeout - App chưa sẵn sàng sau 2 phút")
    return False


async def test_login_functionality(page):
    """Test chức năng đăng nhập."""
    print("🔐 Test chức năng đăng nhập...")
    
    try:
        # Tìm các input fields
        username_input = await page.query_selector("input[type='text']")
        password_input = await page.query_selector("input[type='password']")
        
        if username_input and password_input:
            print("✅ Tìm thấy form đăng nhập")
            
            # Clear và nhập thông tin
            await username_input.clear()
            await username_input.fill("admin")
            
            await password_input.clear()
            await password_input.fill("admin123")
            
            print("✅ Đã nhập thông tin đăng nhập")
            
            # Tìm và click nút đăng nhập
            login_buttons = await page.query_selector_all("button")
            login_button = None
            
            for button in login_buttons:
                button_text = await button.text_content()
                if "đăng nhập" in button_text.lower() or "login" in button_text.lower():
                    login_button = button
                    break
            
            if not login_button and login_buttons:
                # Thử button đầu tiên nếu không tìm thấy
                login_button = login_buttons[0]
            
            if login_button:
                await login_button.click()
                print("✅ Đã click nút đăng nhập")
                
                # Đợi sau khi đăng nhập
                await page.wait_for_timeout(5000)
                
                # Kiểm tra đăng nhập thành công
                page_content = await page.content()
                if "dashboard" in page_content.lower() or "tổng quan" in page_content.lower():
                    print("🎉 Đăng nhập thành công - Đã vào dashboard!")
                    return True
                else:
                    print("⚠️ Đăng nhập có thể chưa thành công")
                    return False
            else:
                print("❌ Không tìm thấy nút đăng nhập")
                return False
        else:
            print("❌ Không tìm thấy form đăng nhập")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi test đăng nhập: {e}")
        return False


async def main():
    """Main test function."""
    print("🧪 HRMS Final Test - Comprehensive Testing")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to localhost:3000
            print("🌐 Truy cập http://localhost:3000...")
            await page.goto("http://localhost:3000", timeout=30000)
            
            # Take initial screenshot
            await page.screenshot(path="hrms_initial.png")
            print("📸 Screenshot ban đầu: hrms_initial.png")
            
            # Wait for app to be ready
            if not await wait_for_app_ready(page):
                print("❌ App không sẵn sàng - Kết thúc test")
                return
            
            # Take screenshot when ready
            await page.screenshot(path="hrms_ready.png")
            print("📸 Screenshot khi sẵn sàng: hrms_ready.png")
            
            # Test login functionality
            login_success = await test_login_functionality(page)
            
            if login_success:
                # Take screenshot after login
                await page.screenshot(path="hrms_logged_in.png")
                print("📸 Screenshot sau đăng nhập: hrms_logged_in.png")
                
                # Test navigation
                print("🧭 Test navigation...")
                sidebar_buttons = await page.query_selector_all("[data-testid='stSidebar'] button")
                
                if sidebar_buttons:
                    print(f"✅ Tìm thấy {len(sidebar_buttons)} menu items")
                    
                    # Click vào menu đầu tiên
                    if len(sidebar_buttons) > 1:  # Skip logout button
                        await sidebar_buttons[0].click()
                        await page.wait_for_timeout(3000)
                        print("✅ Đã test click menu")
                else:
                    print("⚠️ Không tìm thấy menu items")
                
                # Final screenshot
                await page.screenshot(path="hrms_final.png")
                print("📸 Screenshot cuối: hrms_final.png")
            
            print("\n🎉 Test hoàn thành!")
            print("📸 Kiểm tra các screenshot để xem kết quả chi tiết")
            
        except Exception as e:
            print(f"❌ Lỗi trong test: {e}")
            await page.screenshot(path="hrms_error.png")
            print("📸 Screenshot lỗi: hrms_error.png")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
