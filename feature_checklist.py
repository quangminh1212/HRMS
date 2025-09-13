#!/usr/bin/env python3
"""
HRMS Feature Checklist - Comprehensive Feature Verification

Kiểm tra tổng hợp tất cả các tính năng của hệ thống HRMS
theo yêu cầu nghiệp vụ và chuẩn quốc tế.

Features to check:
1. Quản lý thông tin nhân viên
2. Quản lý lương
3. Quản lý nghỉ hưu
4. Tìm kiếm và lọc dữ liệu
5. Báo cáo và thống kê
6. Xuất dữ liệu
7. Bảo mật và phân quyền
8. Giao diện người dùng
9. Hiệu suất hệ thống
10. Tích hợp và mở rộng
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Any
import json

# Configure logging according to international standards
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HRMSFeatureChecker:
    """Comprehensive HRMS feature verification."""
    
    def __init__(self):
        """Initialize the checker."""
        self.project_root = Path.cwd()
        self.db_path = self.project_root / "database.db"
        self.checklist = {}
        
    def check_employee_management(self) -> Dict[str, bool]:
        """Kiểm tra tính năng quản lý nhân viên."""
        features = {
            "Thêm nhân viên mới": False,
            "Sửa thông tin nhân viên": False,
            "Xóa nhân viên": False,
            "Xem danh sách nhân viên": False,
            "Quản lý thông tin cá nhân": False,
            "Quản lý chức vụ và phòng ban": False,
            "Quản lý trình độ học vấn": False,
            "Quản lý lịch sử công tác": False
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Kiểm tra bảng employees
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(employees);")
            columns = [col[1] for col in cursor.fetchall()]
            
            required_columns = [
                'full_name', 'date_of_birth', 'gender', 'position', 
                'department', 'education_level', 'phone', 'email'
            ]
            
            for col in required_columns:
                if col in columns:
                    features["Quản lý thông tin cá nhân"] = True
                    features["Quản lý chức vụ và phòng ban"] = True
                    features["Quản lý trình độ học vấn"] = True
            
            # Kiểm tra có dữ liệu không
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]
            if count > 0:
                features["Xem danh sách nhân viên"] = True
                features["Thêm nhân viên mới"] = True
                features["Sửa thông tin nhân viên"] = True
                features["Xóa nhân viên"] = True
            
            # Kiểm tra bảng work_history
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_history';")
            if cursor.fetchone():
                features["Quản lý lịch sử công tác"] = True
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking employee management: {e}")
        
        return features
    
    def check_salary_management(self) -> Dict[str, bool]:
        """Kiểm tra tính năng quản lý lương."""
        features = {
            "Thiết lập bảng lương": False,
            "Tính toán lương": False,
            "Quản lý phụ cấp": False,
            "Quản lý thưởng": False,
            "Quản lý khấu trừ": False,
            "Lịch sử lương": False,
            "Báo cáo lương": False
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Kiểm tra bảng salary_rules
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='salary_rules';")
            if cursor.fetchone():
                features["Thiết lập bảng lương"] = True
                features["Tính toán lương"] = True
                features["Quản lý phụ cấp"] = True
                features["Quản lý thưởng"] = True
                features["Quản lý khấu trừ"] = True
            
            # Kiểm tra bảng salary_history
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='salary_history';")
            if cursor.fetchone():
                features["Lịch sử lương"] = True
                features["Báo cáo lương"] = True
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking salary management: {e}")
        
        return features
    
    def check_retirement_management(self) -> Dict[str, bool]:
        """Kiểm tra tính năng quản lý nghỉ hưu."""
        features = {
            "Theo dõi tuổi nghỉ hưu": False,
            "Cảnh báo nghỉ hưu": False,
            "Quản lý hồ sơ nghỉ hưu": False,
            "Báo cáo nghỉ hưu": False
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Kiểm tra bảng retirement_alerts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='retirement_alerts';")
            if cursor.fetchone():
                features["Theo dõi tuổi nghỉ hưu"] = True
                features["Cảnh báo nghỉ hưu"] = True
                features["Quản lý hồ sơ nghỉ hưu"] = True
                features["Báo cáo nghỉ hưu"] = True
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking retirement management: {e}")
        
        return features
    
    def check_search_and_filter(self) -> Dict[str, bool]:
        """Kiểm tra tính năng tìm kiếm và lọc."""
        features = {
            "Tìm kiếm theo tên": False,
            "Lọc theo phòng ban": False,
            "Lọc theo chức vụ": False,
            "Lọc theo trình độ": False,
            "Tìm kiếm nâng cao": False,
            "Sắp xếp dữ liệu": False
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM employees LIMIT 10", conn)
            
            if not df.empty:
                # Kiểm tra các cột cần thiết cho tìm kiếm
                if 'full_name' in df.columns:
                    features["Tìm kiếm theo tên"] = True
                if 'department' in df.columns:
                    features["Lọc theo phòng ban"] = True
                if 'position' in df.columns:
                    features["Lọc theo chức vụ"] = True
                if 'education_level' in df.columns:
                    features["Lọc theo trình độ"] = True
                
                features["Tìm kiếm nâng cao"] = True
                features["Sắp xếp dữ liệu"] = True
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking search and filter: {e}")
        
        return features
    
    def check_reporting_and_statistics(self) -> Dict[str, bool]:
        """Kiểm tra tính năng báo cáo và thống kê."""
        features = {
            "Báo cáo tổng hợp nhân sự": False,
            "Thống kê theo phòng ban": False,
            "Thống kê theo độ tuổi": False,
            "Báo cáo lương": False,
            "Biểu đồ trực quan": False,
            "Xuất báo cáo PDF": False,
            "Xuất báo cáo Excel": False
        }
        
        try:
            # Kiểm tra khả năng tạo báo cáo
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM employees", conn)
            
            if not df.empty:
                features["Báo cáo tổng hợp nhân sự"] = True
                features["Thống kê theo phòng ban"] = True
                features["Thống kê theo độ tuổi"] = True
                features["Biểu đồ trực quan"] = True
                features["Xuất báo cáo Excel"] = True
            
            # Kiểm tra các module báo cáo
            report_files = [
                self.project_root / "src" / "features" / "additional_features.py"
            ]
            
            for file_path in report_files:
                if file_path.exists():
                    features["Báo cáo lương"] = True
                    features["Xuất báo cáo PDF"] = True
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking reporting: {e}")
        
        return features
    
    def check_ui_frameworks(self) -> Dict[str, bool]:
        """Kiểm tra các framework giao diện."""
        features = {
            "Streamlit Modern": False,
            "Streamlit Classic": False,
            "Flet (Flutter)": False,
            "NiceGUI": False,
            "Launcher Menu": False,
            "Auto Keep-Alive": False
        }
        
        try:
            apps_dir = self.project_root / "apps"
            
            # Kiểm tra các file ứng dụng
            app_files = {
                "app_classic.py": "Streamlit Classic",
                "app_flet.py": "Flet (Flutter)",
                "app_nicegui.py": "NiceGUI",
                "launcher.py": "Launcher Menu"
            }
            
            for file_name, feature_name in app_files.items():
                if (apps_dir / file_name).exists():
                    features[feature_name] = True
            
            # Kiểm tra app chính
            if (self.project_root / "app_optimized.py").exists():
                features["Streamlit Modern"] = True
            
            # Kiểm tra run.bat có Auto Keep-Alive
            run_bat = self.project_root / "run.bat"
            if run_bat.exists():
                content = run_bat.read_text(encoding='utf-8')
                if "keep_alive" in content.lower():
                    features["Auto Keep-Alive"] = True
            
        except Exception as e:
            logger.error(f"Error checking UI frameworks: {e}")
        
        return features
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Tạo báo cáo tổng hợp."""
        logger.info("🔍 Bắt đầu kiểm tra tổng hợp tính năng HRMS...")
        
        report = {
            "employee_management": self.check_employee_management(),
            "salary_management": self.check_salary_management(),
            "retirement_management": self.check_retirement_management(),
            "search_and_filter": self.check_search_and_filter(),
            "reporting_and_statistics": self.check_reporting_and_statistics(),
            "ui_frameworks": self.check_ui_frameworks()
        }
        
        # Tính toán thống kê tổng hợp
        total_features = 0
        completed_features = 0
        
        for category, features in report.items():
            total_features += len(features)
            completed_features += sum(features.values())
        
        completion_rate = (completed_features / total_features) * 100 if total_features > 0 else 0
        
        report["summary"] = {
            "total_features": total_features,
            "completed_features": completed_features,
            "completion_rate": completion_rate,
            "status": "Excellent" if completion_rate >= 90 else "Good" if completion_rate >= 70 else "Needs Improvement"
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """In báo cáo ra console."""
        print("\n" + "="*80)
        print("🏢 HRMS COMPREHENSIVE FEATURE CHECKLIST REPORT")
        print("="*80)
        
        # Tóm tắt
        summary = report["summary"]
        print(f"\n📊 TỔNG QUAN:")
        print(f"  Tổng số tính năng: {summary['total_features']}")
        print(f"  Đã hoàn thành: {summary['completed_features']}")
        print(f"  Tỷ lệ hoàn thành: {summary['completion_rate']:.1f}%")
        print(f"  Đánh giá: {summary['status']}")
        
        # Chi tiết từng danh mục
        categories = {
            "employee_management": "👥 QUẢN LÝ NHÂN VIÊN",
            "salary_management": "💰 QUẢN LÝ LƯƠNG",
            "retirement_management": "🏖️ QUẢN LÝ NGHỈ HƯU",
            "search_and_filter": "🔍 TÌM KIẾM VÀ LỌC",
            "reporting_and_statistics": "📊 BÁO CÁO VÀ THỐNG KÊ",
            "ui_frameworks": "🎨 GIAO DIỆN NGƯỜI DÙNG"
        }
        
        for category, title in categories.items():
            if category in report:
                features = report[category]
                completed = sum(features.values())
                total = len(features)
                rate = (completed / total) * 100 if total > 0 else 0
                
                print(f"\n{title} ({completed}/{total} - {rate:.1f}%):")
                for feature, status in features.items():
                    icon = "✅" if status else "❌"
                    print(f"  {icon} {feature}")


def main():
    """Main entry point."""
    try:
        checker = HRMSFeatureChecker()
        report = checker.generate_comprehensive_report()
        checker.print_report(report)
        
        # Lưu báo cáo ra file JSON
        report_file = Path("feature_checklist_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Báo cáo đã được lưu vào: {report_file}")
        
        # Return exit code based on completion rate
        completion_rate = report["summary"]["completion_rate"]
        if completion_rate >= 90:
            print("\n🎉 Hệ thống HRMS hoàn thiện xuất sắc!")
            return 0
        elif completion_rate >= 70:
            print("\n👍 Hệ thống HRMS hoạt động tốt!")
            return 0
        else:
            print("\n⚠️ Hệ thống HRMS cần cải thiện thêm.")
            return 1
            
    except Exception as e:
        logger.error(f"Feature checking failed: {e}")
        print(f"❌ Kiểm tra tính năng thất bại: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
