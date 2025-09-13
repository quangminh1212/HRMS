#!/usr/bin/env python3
"""
Debug localhost:3000 - Kiểm tra chi tiết vấn đề
"""

import asyncio
import time
import requests
from playwright.async_api import async_playwright


def detailed_server_check():
    """Kiểm tra chi tiết server."""
    print("🔍 Kiểm tra chi tiết server...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Headers: {dict(response.headers)}")
        
        # Check if it's Streamlit
        content = response.text
        if "streamlit" in content.lower():
            print("✅ Đây là Streamlit app")
        else:
            print("❌ Không phải Streamlit app")
            
        # Check for specific content
        if "Please wait" in content:
            print("⚠️ App đang loading (Please wait...)")
        if "admin" in content.lower():
            print("✅ Có form đăng nhập")
            
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False


async def detailed_playwright_test():
    """Test chi tiết với Playwright."""
    print("\n🎭 Test chi tiết với Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Enable console logging
        page.on("console", lambda msg: print(f"🖥️ Console: {msg.text}"))
        page.on("pageerror", lambda error: print(f"❌ Page Error: {error}"))
        
        try:
            print("🌐 Navigating to localhost:3000...")
            await page.goto("http://localhost:3000", wait_until="networkidle", timeout=30000)
            
            # Wait for Streamlit to load
            print("⏳ Đợi Streamlit load...")
            await page.wait_for_timeout(5000)
            
            # Get page content
            content = await page.content()
            print(f"📄 Page content length: {len(content)} characters")
            
            # Check for Streamlit elements
            streamlit_elements = await page.query_selector_all("[data-testid]")
            print(f"🔍 Found {len(streamlit_elements)} Streamlit elements")
            
            # Look for login form specifically
            forms = await page.query_selector_all("form")
            print(f"📝 Found {len(forms)} forms")
            
            # Look for input fields
            inputs = await page.query_selector_all("input")
            print(f"📝 Found {len(inputs)} input fields")
            
            # Look for buttons
            buttons = await page.query_selector_all("button")
            print(f"🔘 Found {len(buttons)} buttons")
            
            # Check for error messages
            alerts = await page.query_selector_all("[data-testid='stAlert']")
            if alerts:
                for i, alert in enumerate(alerts):
                    text = await alert.text_content()
                    print(f"⚠️ Alert {i+1}: {text}")
            
            # Try to find specific Streamlit components
            try:
                # Wait for main content
                main_content = await page.wait_for_selector("[data-testid='stApp']", timeout=10000)
                if main_content:
                    print("✅ Streamlit main app container found")
                else:
                    print("❌ Streamlit main app container not found")
            except:
                print("❌ Timeout waiting for Streamlit app")
            
            # Take final screenshot
            await page.screenshot(path="debug_screenshot.png", full_page=True)
            print("📸 Full page screenshot saved: debug_screenshot.png")
            
            # Get final page state
            title = await page.title()
            url = page.url
            print(f"📄 Final title: {title}")
            print(f"🌐 Final URL: {url}")
            
        except Exception as e:
            print(f"❌ Playwright error: {e}")
        finally:
            await browser.close()


def check_run_py():
    """Kiểm tra file run.py có tồn tại không."""
    import os
    
    print("\n📁 Kiểm tra files...")
    files_to_check = ["run.py", "app.py", "app_optimized.py"]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")


async def main():
    """Main function."""
    print("🔧 DEBUG LOCALHOST:3000")
    print("=" * 50)
    
    # Check files
    check_run_py()
    
    # Check server
    print("\n1. Server Status Check:")
    if not detailed_server_check():
        print("❌ Server không hoạt động")
        return
    
    # Detailed Playwright test
    print("\n2. Detailed Playwright Test:")
    await detailed_playwright_test()
    
    print("\n✅ Debug hoàn thành!")
    print("📸 Kiểm tra debug_screenshot.png để xem chi tiết")


if __name__ == "__main__":
    asyncio.run(main())
