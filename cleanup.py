#!/usr/bin/env python3
"""
HRMS Project Cleanup Script - International Standards Compliant

Automatically cleans up temporary files, cache directories, and other
generated files to maintain a clean project structure.

Features:
- Removes Python cache files (__pycache__)
- Cleans up temporary files
- Removes generated exports
- Maintains .gitignore compliance
- Logging for all operations
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectCleaner:
    """Professional project cleanup utility."""
    
    def __init__(self, project_root: Path = None):
        """Initialize the cleaner with project root directory."""
        self.project_root = project_root or Path.cwd()
        self.cleaned_items: Set[str] = set()
        
    def clean_python_cache(self) -> None:
        """Remove all __pycache__ directories and .pyc files."""
        logger.info("Cleaning Python cache files...")
        
        # Remove __pycache__ directories
        for pycache_dir in self.project_root.rglob("__pycache__"):
            if pycache_dir.is_dir():
                try:
                    shutil.rmtree(pycache_dir)
                    self.cleaned_items.add(str(pycache_dir))
                    logger.info(f"Removed: {pycache_dir}")
                except Exception as e:
                    logger.error(f"Failed to remove {pycache_dir}: {e}")
        
        # Remove .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                self.cleaned_items.add(str(pyc_file))
                logger.info(f"Removed: {pyc_file}")
            except Exception as e:
                logger.error(f"Failed to remove {pyc_file}: {e}")
    
    def clean_temporary_files(self) -> None:
        """Remove temporary files and directories."""
        logger.info("Cleaning temporary files...")
        
        temp_patterns = [
            "*.tmp", "*.temp", "*.log", "*.bak", "*.swp", "*.swo", "*~"
        ]
        
        for pattern in temp_patterns:
            for temp_file in self.project_root.rglob(pattern):
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                        self.cleaned_items.add(str(temp_file))
                        logger.info(f"Removed: {temp_file}")
                except Exception as e:
                    logger.error(f"Failed to remove {temp_file}: {e}")
    
    def clean_generated_files(self) -> None:
        """Remove generated export files."""
        logger.info("Cleaning generated files...")
        
        # Remove exports directory if it exists
        exports_dir = self.project_root / "exports"
        if exports_dir.exists() and exports_dir.is_dir():
            try:
                shutil.rmtree(exports_dir)
                self.cleaned_items.add(str(exports_dir))
                logger.info(f"Removed: {exports_dir}")
            except Exception as e:
                logger.error(f"Failed to remove {exports_dir}: {e}")
        
        # Remove logs directory if empty
        logs_dir = self.project_root / "logs"
        if logs_dir.exists() and logs_dir.is_dir():
            try:
                if not any(logs_dir.iterdir()):  # Check if empty
                    logs_dir.rmdir()
                    self.cleaned_items.add(str(logs_dir))
                    logger.info(f"Removed empty directory: {logs_dir}")
            except Exception as e:
                logger.error(f"Failed to remove {logs_dir}: {e}")
    
    def clean_ide_files(self) -> None:
        """Remove IDE-specific files and directories."""
        logger.info("Cleaning IDE files...")
        
        ide_patterns = [
            ".vscode", ".idea", "*.swp", "*.swo", ".DS_Store", "Thumbs.db"
        ]
        
        for pattern in ide_patterns:
            for ide_item in self.project_root.rglob(pattern):
                try:
                    if ide_item.is_file():
                        ide_item.unlink()
                        self.cleaned_items.add(str(ide_item))
                        logger.info(f"Removed: {ide_item}")
                    elif ide_item.is_dir():
                        shutil.rmtree(ide_item)
                        self.cleaned_items.add(str(ide_item))
                        logger.info(f"Removed: {ide_item}")
                except Exception as e:
                    logger.error(f"Failed to remove {ide_item}: {e}")
    
    def run_cleanup(self) -> None:
        """Run complete project cleanup."""
        logger.info("Starting project cleanup...")
        
        self.clean_python_cache()
        self.clean_temporary_files()
        self.clean_generated_files()
        self.clean_ide_files()
        
        logger.info(f"Cleanup completed. Removed {len(self.cleaned_items)} items.")
        
        if self.cleaned_items:
            logger.info("Cleaned items:")
            for item in sorted(self.cleaned_items):
                logger.info(f"  - {item}")


def main():
    """Main entry point."""
    try:
        cleaner = ProjectCleaner()
        cleaner.run_cleanup()
        print("✅ Project cleanup completed successfully!")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        print(f"❌ Cleanup failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
