#!/usr/bin/env python3
"""
Test HRMS hoàn chỉnh - Đợi app load xong rồi test
"""

import asyncio
import time
from playwright.async_api import async_playwright


async def wait_for_streamlit_ready(page):
    """Đợi Streamlit app sẵn sàng."""
    print("⏳ Đợi Streamlit app sẵn sàng...")
    
    # Đợi tối đa 60 giây
    for i in range(60):
        try:
            # Kiểm tra xem có "Please wait..." không
            please_wait = await page.query_selector_all("text=Please wait")
            if not please_wait:
                print("✅ App đã sẵn sàng!")
                return True
                
            print(f"⏳ Đợi... ({i+1}/60s)")
            await page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"⚠️ Lỗi khi kiểm tra: {e}")
            await page.wait_for_timeout(1000)
    
    print("❌ Timeout - App chưa sẵn sàng sau 60s")
    return False


async def test_hrms_login(page):
    """Test đăng nhập HRMS."""
    print("🔐 Test đăng nhập...")
    
    try:
        # Tìm form đăng nhập
        username_input = await page.query_selector("input[type='text']")
        password_input = await page.query_selector("input[type='password']")
        
        if username_input and password_input:
            print("✅ Tìm thấy form đăng nhập")
            
            # Nhập thông tin
            await username_input.fill("admin")
            await password_input.fill("admin123")
            print("✅ Đã nhập thông tin đăng nhập")
            
            # Tìm nút đăng nhập
            login_button = await page.query_selector("button:has-text('Đăng nhập')")
            if not login_button:
                login_button = await page.query_selector("button[type='submit']")
            
            if login_button:
                await login_button.click()
                print("✅ Đã click nút đăng nhập")
                
                # Đợi sau khi đăng nhập
                await page.wait_for_timeout(3000)
                
                # Kiểm tra đăng nhập thành công
                success_msg = await page.query_selector("text=thành công")
                if success_msg:
                    print("🎉 Đăng nhập thành công!")
                    return True
                else:
                    print("⚠️ Chưa thấy thông báo thành công")
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


async def test_hrms_navigation(page):
    """Test điều hướng trong HRMS."""
    print("🧭 Test điều hướng...")
    
    try:
        # Tìm sidebar hoặc menu
        sidebar_items = await page.query_selector_all("[data-testid='stSidebar'] a, [data-testid='stSidebar'] button")
        
        if sidebar_items:
            print(f"✅ Tìm thấy {len(sidebar_items)} menu items")
            
            # Click vào item đầu tiên
            if len(sidebar_items) > 0:
                await sidebar_items[0].click()
                await page.wait_for_timeout(2000)
                print("✅ Đã test click menu")
                return True
        else:
            print("⚠️ Không tìm thấy menu items")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi test navigation: {e}")
        return False


async def main():
    """Main test function."""
    print("🧪 HRMS Complete Test với Playwright")
    print("=" * 50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to localhost:3000
            print("🌐 Truy cập http://localhost:3000...")
            await page.goto("http://localhost:3000", timeout=30000)
            
            # Đợi Streamlit sẵn sàng
            if not await wait_for_streamlit_ready(page):
                print("❌ App không sẵn sàng")
                return
            
            # Chụp screenshot sau khi sẵn sàng
            await page.screenshot(path="hrms_ready.png")
            print("📸 Screenshot app sẵn sàng: hrms_ready.png")
            
            # Test đăng nhập
            login_success = await test_hrms_login(page)
            
            if login_success:
                # Chụp screenshot sau đăng nhập
                await page.screenshot(path="hrms_logged_in.png")
                print("📸 Screenshot sau đăng nhập: hrms_logged_in.png")
                
                # Test navigation
                await test_hrms_navigation(page)
                
                # Chụp screenshot cuối
                await page.screenshot(path="hrms_final.png")
                print("📸 Screenshot cuối: hrms_final.png")
            
            print("\n🎉 Test hoàn thành!")
            print("📸 Kiểm tra các screenshot để xem kết quả")
            
        except Exception as e:
            print(f"❌ Lỗi trong test: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
