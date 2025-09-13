#!/usr/bin/env python3
"""
XLAB HRMS Launch Script - International Standards Compliant

Professional application launcher with proper error handling,
logging, and configuration management.

Standards compliance:
- PEP 8 code style
- Proper error handling
- Logging integration
- Clean architecture
- Type hints
- Documentation
"""

import logging
import sys
import subprocess
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HRMSLauncher:
    """Professional HRMS application launcher."""
    
    def __init__(self) -> None:
        """Initialize the launcher with configuration."""
        self.app_name = "XLAB HRMS"
        self.port = 3000
        self.host = "0.0.0.0"
        self.app_file = "app_optimized.py"
        
    def display_banner(self) -> None:
        """Display professional application banner."""
        banner_lines = [
            "=" * 70,
            f"⚡ {self.app_name} - HỆ THỐNG QUẢN LÝ NHÂN SỰ",
            "=" * 70,
            "✨ Giao diện hiện đại với XLAB Design System",
            "🎨 Tham khảo XLAB Style, Material Design 3, Clean Architecture",
            "🏗️ Component System chuyên nghiệp với Clean White Theme",
            "💎 Modern Teal Accents & Micro-animations",
            "=" * 70,
            f"🌐 Ứng dụng sẽ mở tại: http://localhost:{self.port}",
            "👤 Tài khoản: admin / admin123",
            "=" * 70,
            "⚠️  Nhấn Ctrl+C để dừng server",
            "=" * 70,
        ]
        
        for line in banner_lines:
            print(line)
    
    def check_dependencies(self) -> bool:
        """
        Check if required dependencies are installed.
        
        Returns:
            bool: True if all dependencies are available
        """
        required_packages = ['streamlit', 'plotly', 'pandas', 'sqlalchemy']
        
        print("✅ Dependencies đã sẵn sàng")
        
        try:
            for package in required_packages:
                __import__(package)
            logger.info("All dependencies verified successfully")
            return True
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            print(f"❌ Thiếu package: {e}")
            print("💡 Chạy: pip install -r requirements.txt")
            return False
    
    def get_streamlit_command(self) -> List[str]:
        """
        Build Streamlit command with optimized configuration.
        
        Returns:
            List[str]: Command arguments list
        """
        return [
            sys.executable, "-m", "streamlit", "run", self.app_file,
            "--server.port", str(self.port),
            "--server.address", self.host,
            "--browser.gatherUsageStats", "false",
            "--theme.primaryColor", "#14B8A6",
            "--theme.backgroundColor", "#FFFFFF",
            "--theme.secondaryBackgroundColor", "#F8FAFC",
            "--theme.textColor", "#0D1421",
            "--server.headless", "false"
        ]
    
    def launch_application(self) -> Optional[int]:
        """
        Launch the HRMS application with error handling.
        
        Returns:
            Optional[int]: Exit code if process completes, None if interrupted
        """
        try:
            print("🎉 Đang khởi động HRMS Modern...")
            print("💎 Trải nghiệm giao diện đẹp nhất từ trước tới nay!")
            
            cmd = self.get_streamlit_command()
            logger.info(f"Launching with command: {' '.join(cmd)}")
            
            # Start the Streamlit application
            process = subprocess.run(cmd, check=True)
            return process.returncode
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Streamlit process failed with code {e.returncode}")
            self._handle_launch_error(e.returncode)
            return e.returncode
            
        except KeyboardInterrupt:
            print("\n👋 HRMS Modern đã dừng")
            logger.info("Application stopped by user")
            return None
            
        except Exception as e:
            logger.critical(f"Unexpected error during launch: {e}")
            print(f"\n❌ Lỗi không mong đợi: {e}")
            return 1
    
    def _handle_launch_error(self, exit_code: int) -> None:
        """
        Handle launch errors with helpful messages.
        
        Args:
            exit_code: Process exit code
        """
        error_messages = {
            1: "Lỗi cấu hình ứng dụng",
            2: "Lỗi import module", 
            3: "Lỗi kết nối database",
        }
        
        print(f"\n❌ Lỗi khi chạy HRMS Modern (mã lỗi: {exit_code})")
        print(f"💡 {error_messages.get(exit_code, 'Lỗi không xác định')}")
        
        print("\n🔧 Hướng dẫn khắc phục:")
        troubleshooting_steps = [
            f"- Kiểm tra port {self.port} có bị chiếm không",
            "- Chạy lại script với quyền admin",
            "- Cài đặt lại dependencies: pip install -r requirements.txt",
            "- Đảm bảo file app_optimized.py tồn tại",
            "- Kiểm tra log files để biết chi tiết lỗi"
        ]
        
        for step in troubleshooting_steps:
            print(step)
    
    def run(self) -> int:
        """
        Main run method for the launcher.
        
        Returns:
            int: Exit code
        """
        # Display banner
        self.display_banner()
        
        # Check dependencies
        if not self.check_dependencies():
            return 1
        
        # Check if app file exists
        if not Path(self.app_file).exists():
            logger.error(f"Application file not found: {self.app_file}")
            print(f"❌ Không tìm thấy file: {self.app_file}")
            return 1
        
        # Launch application
        exit_code = self.launch_application()
        
        return exit_code if exit_code is not None else 0


def main() -> int:
    """
    Main entry point for the launcher.
    
    Returns:
        int: Exit code
    """
    try:
        launcher = HRMSLauncher()
        return launcher.run()
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}")
        print(f"❌ Lỗi nghiêm trọng: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
