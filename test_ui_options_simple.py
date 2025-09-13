#!/usr/bin/env python3
"""
HRMS UI Options Simple Testing

Test đơn giản và hiệu quả cho tất cả các lựa chọn UI trong run.bat
"""

import subprocess
import time
import logging
import requests
import psutil
from pathlib import Path
from typing import Dict, List, Any
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleUITester:
    """Simple UI testing for all HRMS options."""
    
    def __init__(self):
        """Initialize the tester."""
        self.project_root = Path.cwd()
        self.test_results = []
        
        # Test configurations
        self.options = {
            "1": {"name": "HRMS Modern", "port": 3000, "timeout": 30},
            "2": {"name": "Quick Start", "port": 3000, "timeout": 45},
            "3": {"name": "Launcher Menu", "port": 8080, "timeout": 25, "desktop": True},
            "4": {"name": "Streamlit Classic", "port": 8501, "timeout": 30},
            "5": {"name": "Flet (Flutter UI)", "port": 8550, "timeout": 35, "desktop": True},
            "6": {"name": "NiceGUI (Tailwind)", "port": 8080, "timeout": 30},
            "7": {"name": "Manual Mode", "port": 3000, "timeout": 25, "no_keep_alive": True}
        }
    
    def kill_python_processes(self):
        """Kill existing Python processes."""
        killed = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python.exe':
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmdline.lower() for keyword in 
                           ['streamlit', 'flet', 'nicegui', 'run.py', 'app']):
                        proc.kill()
                        killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed > 0:
            logger.info(f"Killed {killed} existing Python processes")
            time.sleep(3)
    
    def check_port(self, port: int, timeout: int = 30) -> bool:
        """Check if port is accessible."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ Port {port} is accessible")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(3)
        
        logger.warning(f"❌ Port {port} not accessible after {timeout}s")
        return False
    
    def test_option(self, option: str) -> Dict[str, Any]:
        """Test a single option."""
        config = self.options[option]
        logger.info(f"\n🧪 Testing Option {option}: {config['name']}")
        
        result = {
            "option": option,
            "name": config["name"],
            "success": False,
            "port_accessible": False,
            "process_started": False,
            "keep_alive_tested": False,
            "error": None
        }
        
        try:
            # Kill existing processes
            self.kill_python_processes()
            
            # Start run.bat with the option
            logger.info(f"Starting {config['name']}...")
            
            # Create input for run.bat
            process = subprocess.Popen(
                ["run.bat"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.project_root)
            )
            
            # Send the option number
            process.stdin.write(f"{option}\n")
            process.stdin.flush()
            
            result["process_started"] = True
            logger.info(f"Process started with PID: {process.pid}")
            
            # Wait for application to start
            time.sleep(15)
            
            # Check if it's a web interface
            if not config.get("desktop", False):
                if self.check_port(config["port"], config["timeout"]):
                    result["port_accessible"] = True
                    result["success"] = True
                    
                    # Test Keep-Alive (except Manual Mode)
                    if not config.get("no_keep_alive", False):
                        logger.info("Testing Keep-Alive functionality...")
                        
                        # Kill the process
                        process.terminate()
                        time.sleep(10)
                        
                        # Check if port is still accessible
                        if self.check_port(config["port"], 30):
                            result["keep_alive_tested"] = True
                            logger.info("✅ Keep-Alive verified")
                        else:
                            logger.warning("⚠️ Keep-Alive not working")
                else:
                    result["error"] = f"Port {config['port']} not accessible"
            else:
                # For desktop apps, check if process is running
                time.sleep(10)
                desktop_running = False
                
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'python' in proc.info['name'].lower() and any(
                            keyword in cmdline.lower() for keyword in ['flet', 'launcher']
                        ):
                            desktop_running = True
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                if desktop_running:
                    result["success"] = True
                    result["port_accessible"] = True
                    logger.info("✅ Desktop application running")
                else:
                    result["error"] = "Desktop application not detected"
            
        except Exception as e:
            result["error"] = f"Test failed: {e}"
            logger.error(f"Error testing option {option}: {e}")
        
        finally:
            # Cleanup
            try:
                if 'process' in locals() and process.poll() is None:
                    process.terminate()
                    process.wait(timeout=10)
            except:
                pass
            
            self.kill_python_processes()
        
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        logger.info(f"Option {option} result: {status}")
        
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests for all options."""
        logger.info("🚀 Starting UI testing for all HRMS options...")
        
        results = []
        
        for option in self.options.keys():
            try:
                result = self.test_option(option)
                results.append(result)
                
                # Wait between tests
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Failed to test option {option}: {e}")
                results.append({
                    "option": option,
                    "name": self.options[option]["name"],
                    "success": False,
                    "error": f"Test setup failed: {e}"
                })
        
        # Generate summary
        total = len(results)
        successful = sum(1 for r in results if r["success"])
        keep_alive_working = sum(1 for r in results if r.get("keep_alive_tested", False))
        
        summary = {
            "total_tests": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total) * 100 if total > 0 else 0,
            "keep_alive_working": keep_alive_working
        }
        
        # Save results
        report = {
            "summary": summary,
            "results": results
        }
        
        report_file = self.project_root / "ui_test_simple_results.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Print summary
        self.print_summary(summary, results)
        
        return report
    
    def print_summary(self, summary: Dict[str, Any], results: List[Dict[str, Any]]):
        """Print test summary."""
        print("\n" + "="*70)
        print("🧪 HRMS UI OPTIONS TEST REPORT")
        print("="*70)
        
        print(f"\n📊 TỔNG QUAN:")
        print(f"  Tổng số test: {summary['total_tests']}")
        print(f"  Thành công: {summary['successful']}")
        print(f"  Thất bại: {summary['failed']}")
        print(f"  Tỷ lệ thành công: {summary['success_rate']:.1f}%")
        print(f"  Keep-Alive hoạt động: {summary['keep_alive_working']}")
        
        print(f"\n📋 CHI TIẾT:")
        for result in results:
            status = "✅" if result["success"] else "❌"
            keep_alive = "🔄" if result.get("keep_alive_tested", False) else "⏹️"
            
            print(f"  [{result['option']}] {status} {result['name']} {keep_alive}")
            if result.get("error"):
                print(f"      Error: {result['error']}")
        
        print(f"\n🔄 = Keep-Alive verified, ⏹️ = No Keep-Alive or not tested")


def main():
    """Main entry point."""
    try:
        tester = SimpleUITester()
        report = tester.run_all_tests()
        
        success_rate = report["summary"]["success_rate"]
        if success_rate >= 70:
            print("\n🎉 UI testing completed successfully!")
            return 0
        else:
            print("\n⚠️ Some UI tests failed.")
            return 1
            
    except Exception as e:
        logger.error(f"Testing failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
