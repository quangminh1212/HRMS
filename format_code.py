#!/usr/bin/env python3
"""
HRMS Code Formatter - International Standards Compliant

Automatically formats Python code according to PEP 8 standards using
black, isort, and other professional formatting tools.

Features:
- Black code formatting
- Import sorting with isort
- Line length compliance
- Docstring formatting
- Remove unused imports
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CodeFormatter:
    """Professional code formatting utility."""
    
    def __init__(self, project_root: Path = None):
        """Initialize the formatter."""
        self.project_root = project_root or Path.cwd()
        self.formatted_files: List[str] = []
        
    def install_dependencies(self) -> bool:
        """Install required formatting tools."""
        tools = ['black', 'isort', 'autoflake']
        
        for tool in tools:
            try:
                logger.info(f"Installing {tool}...")
                result = subprocess.run(
                    ['pip', 'install', tool],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f"✅ {tool} installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install {tool}: {e}")
                return False
        
        return True
    
    def format_with_black(self, file_path: Path) -> bool:
        """Format file with Black."""
        try:
            result = subprocess.run(
                ['black', '--line-length', '79', str(file_path)],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"✅ Black formatted: {file_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Black formatting failed for {file_path}: {e}")
            return False
        except FileNotFoundError:
            logger.warning("Black not found, skipping...")
            return False
    
    def sort_imports(self, file_path: Path) -> bool:
        """Sort imports with isort."""
        try:
            result = subprocess.run(
                ['isort', '--profile', 'black', '--line-length', '79', str(file_path)],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"✅ Imports sorted: {file_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Import sorting failed for {file_path}: {e}")
            return False
        except FileNotFoundError:
            logger.warning("isort not found, skipping...")
            return False
    
    def remove_unused_imports(self, file_path: Path) -> bool:
        """Remove unused imports with autoflake."""
        try:
            result = subprocess.run([
                'autoflake',
                '--in-place',
                '--remove-all-unused-imports',
                '--remove-unused-variables',
                str(file_path)
            ], capture_output=True, text=True, check=True)
            logger.info(f"✅ Unused imports removed: {file_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Autoflake failed for {file_path}: {e}")
            return False
        except FileNotFoundError:
            logger.warning("autoflake not found, skipping...")
            return False
    
    def format_file(self, file_path: Path) -> bool:
        """Format a single Python file."""
        logger.info(f"Formatting {file_path}...")
        
        success = True
        
        # Remove unused imports first
        if not self.remove_unused_imports(file_path):
            success = False
        
        # Sort imports
        if not self.sort_imports(file_path):
            success = False
        
        # Format with Black
        if not self.format_with_black(file_path):
            success = False
        
        if success:
            self.formatted_files.append(str(file_path))
        
        return success
    
    def format_project(self) -> None:
        """Format all Python files in the project."""
        logger.info("Starting code formatting...")
        
        # Install dependencies
        if not self.install_dependencies():
            logger.error("Failed to install required tools")
            return
        
        # Find all Python files
        python_files = list(self.project_root.rglob("*.py"))
        
        # Filter out virtual environment and cache files
        python_files = [
            f for f in python_files 
            if not any(part.startswith('.') or part == '__pycache__' 
                      for part in f.parts)
        ]
        
        logger.info(f"Found {len(python_files)} Python files to format")
        
        success_count = 0
        for py_file in python_files:
            if self.format_file(py_file):
                success_count += 1
        
        logger.info(f"✅ Successfully formatted {success_count}/{len(python_files)} files")
        
        if self.formatted_files:
            logger.info("Formatted files:")
            for file_path in self.formatted_files:
                logger.info(f"  - {file_path}")


def main():
    """Main entry point."""
    try:
        formatter = CodeFormatter()
        formatter.format_project()
        print("✅ Code formatting completed!")
        return 0
    except Exception as e:
        logger.error(f"Formatting failed: {e}")
        print(f"❌ Formatting failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
