#!/usr/bin/env python3
"""
HRMS UI Options Comprehensive Testing with Playwright

Test tất cả các lựa chọn UI trong run.bat:
1. HRMS Modern (MỚI NHẤT) - Auto Keep-Alive
2. Quick Start - Auto Keep-Alive  
3. Launcher Menu - Auto Keep-Alive
4. Streamlit Classic - Auto Keep-Alive
5. Flet (Flutter UI) - Auto Keep-Alive
6. NiceGUI (Tailwind) - Auto Keep-Alive
7. Manual Mode - Chạy 1 lần

Standards compliance:
- Playwright automation
- Comprehensive UI testing
- Error handling
- Performance monitoring
- Screenshot capture
"""

import asyncio
import subprocess
import time
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import psutil
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HRMSUITester:
    """Comprehensive UI testing for all HRMS options."""
    
    def __init__(self):
        """Initialize the tester."""
        self.project_root = Path.cwd()
        self.test_results = {}
        self.screenshots_dir = self.project_root / "test_screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Test configurations for each option
        self.test_configs = {
            "1": {
                "name": "HRMS Modern",
                "description": "Giao diện đẹp nhất + Auto Keep-Alive",
                "expected_port": 3000,
                "expected_title": "HRMS",
                "test_timeout": 30
            },
            "2": {
                "name": "Quick Start",
                "description": "Khởi động nhanh + Auto Keep-Alive",
                "expected_port": 3000,
                "expected_title": "HRMS",
                "test_timeout": 45  # Longer due to dependency installation
            },
            "3": {
                "name": "Launcher Menu",
                "description": "Chọn nhiều framework + Auto Keep-Alive",
                "expected_port": 8080,
                "expected_title": "HRMS",
                "test_timeout": 25,
                "is_desktop": True
            },
            "4": {
                "name": "Streamlit Classic",
                "description": "Phiên bản ổn định + Auto Keep-Alive",
                "expected_port": 8501,
                "expected_title": "HRMS",
                "test_timeout": 30
            },
            "5": {
                "name": "Flet (Flutter UI)",
                "description": "Cross-platform + Auto Keep-Alive",
                "expected_port": 8550,
                "expected_title": "HRMS",
                "test_timeout": 35,
                "is_desktop": True
            },
            "6": {
                "name": "NiceGUI (Tailwind)",
                "description": "Web hiện đại + Auto Keep-Alive",
                "expected_port": 8080,
                "expected_title": "HRMS",
                "test_timeout": 30
            },
            "7": {
                "name": "Manual Mode",
                "description": "Chạy 1 lần không auto restart",
                "expected_port": 3000,
                "expected_title": "HRMS",
                "test_timeout": 25,
                "no_keep_alive": True
            }
        }
    
    def kill_existing_processes(self) -> None:
        """Kill any existing Python processes that might interfere."""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] == 'python.exe':
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if any(keyword in cmdline.lower() for keyword in 
                               ['streamlit', 'flet', 'nicegui', 'launcher', 'run.py', 'app']):
                            logger.info(f"Killing existing process: {proc.info['pid']}")
                            proc.kill()
                            proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
        except Exception as e:
            logger.warning(f"Error killing processes: {e}")
    
    def wait_for_port(self, port: int, timeout: int = 30) -> bool:
        """Wait for a port to become available."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=5)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)
        return False
    
    def start_run_bat_option(self, option: str) -> Optional[subprocess.Popen]:
        """Start run.bat with specific option."""
        try:
            # Create a batch script to automate the selection
            temp_script = self.project_root / f"temp_run_{option}.bat"
            
            script_content = f"""@echo off
echo {option} | run.bat
"""
            temp_script.write_text(script_content, encoding='utf-8')
            
            # Start the process
            process = subprocess.Popen(
                [str(temp_script)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            logger.info(f"Started option {option} with PID: {process.pid}")
            return process
            
        except Exception as e:
            logger.error(f"Failed to start option {option}: {e}")
            return None
    
    async def test_web_interface(self, config: Dict[str, Any], option: str) -> Dict[str, Any]:
        """Test web interface using Playwright."""
        result = {
            "success": False,
            "error": None,
            "screenshot": None,
            "page_title": None,
            "response_time": None,
            "elements_found": []
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Navigate to the application
                url = f"http://localhost:{config['expected_port']}"
                start_time = time.time()
                
                try:
                    await page.goto(url, timeout=30000)
                    result["response_time"] = time.time() - start_time
                    
                    # Wait for page to load
                    await page.wait_for_load_state("networkidle", timeout=15000)
                    
                    # Get page title
                    result["page_title"] = await page.title()
                    
                    # Take screenshot
                    screenshot_path = self.screenshots_dir / f"option_{option}_{config['name'].replace(' ', '_')}.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    result["screenshot"] = str(screenshot_path)
                    
                    # Check for common HRMS elements
                    elements_to_check = [
                        "text=HRMS",
                        "text=Nhân sự",
                        "text=Quản lý",
                        "text=admin",
                        "text=Đăng nhập",
                        "input[type=password]",
                        "button",
                        "[data-testid]"
                    ]
                    
                    for selector in elements_to_check:
                        try:
                            element = await page.wait_for_selector(selector, timeout=5000)
                            if element:
                                result["elements_found"].append(selector)
                        except:
                            pass
                    
                    # Try to interact with login if present
                    try:
                        username_input = await page.query_selector("input[type=text], input[placeholder*=admin]")
                        password_input = await page.query_selector("input[type=password]")
                        
                        if username_input and password_input:
                            await username_input.fill("admin")
                            await password_input.fill("admin123")
                            
                            login_button = await page.query_selector("button:has-text('Đăng nhập'), button:has-text('Login')")
                            if login_button:
                                await login_button.click()
                                await page.wait_for_timeout(3000)
                                
                                # Take screenshot after login
                                login_screenshot = self.screenshots_dir / f"option_{option}_after_login.png"
                                await page.screenshot(path=str(login_screenshot), full_page=True)
                    except Exception as e:
                        logger.info(f"Login interaction failed (expected for some UIs): {e}")
                    
                    result["success"] = True
                    
                except Exception as e:
                    result["error"] = f"Page navigation failed: {e}"
                
                await browser.close()
                
        except ImportError:
            result["error"] = "Playwright not installed"
        except Exception as e:
            result["error"] = f"Browser test failed: {e}"
        
        return result
    
    def test_desktop_interface(self, config: Dict[str, Any], option: str) -> Dict[str, Any]:
        """Test desktop interface (Flet, Launcher)."""
        result = {
            "success": False,
            "error": None,
            "process_running": False,
            "window_detected": False
        }
        
        try:
            # Check if process is running
            time.sleep(10)  # Give time for desktop app to start
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'python' in proc.info['name'].lower() and any(
                        keyword in cmdline.lower() for keyword in ['flet', 'launcher']
                    ):
                        result["process_running"] = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # For desktop apps, we consider them successful if process is running
            if result["process_running"]:
                result["success"] = True
            else:
                result["error"] = "Desktop application process not detected"
                
        except Exception as e:
            result["error"] = f"Desktop test failed: {e}"
        
        return result
    
    async def test_single_option(self, option: str) -> Dict[str, Any]:
        """Test a single UI option."""
        config = self.test_configs[option]
        logger.info(f"🧪 Testing Option {option}: {config['name']}")
        
        result = {
            "option": option,
            "name": config["name"],
            "description": config["description"],
            "start_time": datetime.now().isoformat(),
            "success": False,
            "error": None,
            "process_started": False,
            "port_accessible": False,
            "ui_test_result": None,
            "keep_alive_verified": False
        }
        
        process = None
        try:
            # Kill existing processes
            self.kill_existing_processes()
            time.sleep(3)
            
            # Start the application
            process = self.start_run_bat_option(option)
            if not process:
                result["error"] = "Failed to start process"
                return result
            
            result["process_started"] = True
            
            # Wait for application to start
            logger.info(f"Waiting for application to start on port {config['expected_port']}...")
            time.sleep(10)  # Initial wait
            
            # Check if it's a web interface
            if not config.get("is_desktop", False):
                # Wait for port to be accessible
                if self.wait_for_port(config["expected_port"], config["test_timeout"]):
                    result["port_accessible"] = True
                    
                    # Test web interface with Playwright
                    ui_result = await self.test_web_interface(config, option)
                    result["ui_test_result"] = ui_result
                    
                    if ui_result["success"]:
                        result["success"] = True
                else:
                    result["error"] = f"Port {config['expected_port']} not accessible within timeout"
            else:
                # Test desktop interface
                ui_result = self.test_desktop_interface(config, option)
                result["ui_test_result"] = ui_result
                
                if ui_result["success"]:
                    result["success"] = True
                    result["port_accessible"] = True  # Desktop apps don't use ports
            
            # Test Keep-Alive functionality (except for Manual Mode)
            if not config.get("no_keep_alive", False) and result["success"]:
                logger.info("Testing Keep-Alive functionality...")
                
                # Kill the process and see if it restarts
                if process and process.poll() is None:
                    process.terminate()
                    time.sleep(5)
                    
                    # Check if port is still accessible (indicating restart)
                    if not config.get("is_desktop", False):
                        if self.wait_for_port(config["expected_port"], 30):
                            result["keep_alive_verified"] = True
                            logger.info("✅ Keep-Alive functionality verified")
                        else:
                            logger.warning("⚠️ Keep-Alive functionality not verified")
                    else:
                        # For desktop apps, check if process restarted
                        time.sleep(10)
                        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                            try:
                                cmdline = ' '.join(proc.info['cmdline'] or [])
                                if 'python' in proc.info['name'].lower() and any(
                                    keyword in cmdline.lower() for keyword in ['flet', 'launcher']
                                ):
                                    result["keep_alive_verified"] = True
                                    break
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
            
        except Exception as e:
            result["error"] = f"Test execution failed: {e}"
            logger.error(f"Error testing option {option}: {e}")
        
        finally:
            # Cleanup
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=10)
                except:
                    try:
                        process.kill()
                    except:
                        pass
            
            # Clean up temp script
            temp_script = self.project_root / f"temp_run_{option}.bat"
            if temp_script.exists():
                temp_script.unlink()
            
            # Kill any remaining processes
            self.kill_existing_processes()
        
        result["end_time"] = datetime.now().isoformat()
        logger.info(f"✅ Completed testing option {option}: {'SUCCESS' if result['success'] else 'FAILED'}")
        
        return result
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run tests for all UI options."""
        logger.info("🚀 Starting comprehensive UI testing for all HRMS options...")
        
        # Install Playwright if needed
        try:
            await self.install_playwright()
        except Exception as e:
            logger.warning(f"Playwright installation issue: {e}")
        
        all_results = []
        
        # Test each option
        for option in self.test_configs.keys():
            try:
                result = await self.test_single_option(option)
                all_results.append(result)
                
                # Wait between tests to avoid conflicts
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Failed to test option {option}: {e}")
                all_results.append({
                    "option": option,
                    "name": self.test_configs[option]["name"],
                    "success": False,
                    "error": f"Test setup failed: {e}"
                })
        
        # Generate summary report
        summary = self.generate_summary_report(all_results)
        
        # Save detailed results
        report_file = self.project_root / "ui_test_results.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": summary,
                "detailed_results": all_results,
                "test_timestamp": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📊 Test results saved to: {report_file}")
        
        return {
            "summary": summary,
            "detailed_results": all_results
        }
    
    async def install_playwright(self) -> None:
        """Install Playwright if not already installed."""
        try:
            import playwright
            logger.info("✅ Playwright already installed")
        except ImportError:
            logger.info("📦 Installing Playwright...")
            subprocess.run(["pip", "install", "playwright"], check=True)
            subprocess.run(["playwright", "install", "chromium"], check=True)
            logger.info("✅ Playwright installed successfully")
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary report."""
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get("success", False))
        
        summary = {
            "total_options_tested": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": (successful_tests / total_tests) * 100 if total_tests > 0 else 0,
            "keep_alive_verified": sum(1 for r in results if r.get("keep_alive_verified", False)),
            "web_interfaces_tested": sum(1 for r in results if r.get("port_accessible", False)),
            "desktop_interfaces_tested": sum(1 for r in results if self.test_configs[r["option"]].get("is_desktop", False) and r.get("success", False))
        }
        
        return summary
    
    def print_summary_report(self, summary: Dict[str, Any], results: List[Dict[str, Any]]) -> None:
        """Print summary report to console."""
        print("\n" + "="*80)
        print("🧪 HRMS UI OPTIONS COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        print(f"\n📊 TỔNG QUAN:")
        print(f"  Tổng số lựa chọn test: {summary['total_options_tested']}")
        print(f"  Test thành công: {summary['successful_tests']}")
        print(f"  Test thất bại: {summary['failed_tests']}")
        print(f"  Tỷ lệ thành công: {summary['success_rate']:.1f}%")
        print(f"  Keep-Alive verified: {summary['keep_alive_verified']}")
        print(f"  Web interfaces tested: {summary['web_interfaces_tested']}")
        print(f"  Desktop interfaces tested: {summary['desktop_interfaces_tested']}")
        
        print(f"\n📋 CHI TIẾT TỪNG LỰAC CHỌN:")
        for result in results:
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            keep_alive = "🔄 Yes" if result.get("keep_alive_verified", False) else "⏹️ No"
            
            print(f"\n[{result['option']}] {result['name']}")
            print(f"    Status: {status}")
            print(f"    Keep-Alive: {keep_alive}")
            print(f"    Description: {result.get('description', 'N/A')}")
            
            if result.get("error"):
                print(f"    Error: {result['error']}")
            
            if result.get("ui_test_result"):
                ui_result = result["ui_test_result"]
                if ui_result.get("screenshot"):
                    print(f"    Screenshot: {ui_result['screenshot']}")
                if ui_result.get("response_time"):
                    print(f"    Response time: {ui_result['response_time']:.2f}s")


async def main():
    """Main entry point."""
    try:
        tester = HRMSUITester()
        results = await tester.run_all_tests()
        
        tester.print_summary_report(results["summary"], results["detailed_results"])
        
        # Return appropriate exit code
        success_rate = results["summary"]["success_rate"]
        if success_rate >= 80:
            print("\n🎉 UI testing completed successfully!")
            return 0
        else:
            print("\n⚠️ Some UI tests failed. Please check the detailed results.")
            return 1
            
    except Exception as e:
        logger.error(f"UI testing failed: {e}")
        print(f"❌ UI testing failed: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
