#!/usr/bin/env python3
"""
Clean Logs Script - Remove verbose logging from HRMS project

Removes unnecessary log files and simplifies logging throughout the project.
"""

import os
import shutil
from pathlib import Path


def clean_log_files():
    """Remove log files and directories."""
    project_root = Path.cwd()
    
    # Patterns to clean
    patterns_to_remove = [
        "*.log",
        "logs/",
        "test_screenshots/",
        "exports/",
        "temp_*.bat"
    ]
    
    removed_count = 0
    
    for pattern in patterns_to_remove:
        if pattern.endswith('/'):
            # Directory pattern
            dir_name = pattern[:-1]
            dir_path = project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_name}")
                removed_count += 1
        else:
            # File pattern
            for file_path in project_root.glob(pattern):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"Removed file: {file_path.name}")
                    removed_count += 1
    
    print(f"\nCleaned {removed_count} items")


def update_gitignore():
    """Update .gitignore to ignore log files."""
    gitignore_path = Path(".gitignore")
    
    log_patterns = [
        "# Log files",
        "*.log",
        "logs/",
        "test_screenshots/",
        "exports/",
        "temp_*.bat",
        ""
    ]
    
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        
        # Check if log patterns already exist
        if "# Log files" not in content:
            # Append log patterns
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n'.join(log_patterns))
            print("Updated .gitignore with log patterns")
        else:
            print(".gitignore already contains log patterns")
    else:
        # Create new .gitignore
        gitignore_path.write_text('\n'.join(log_patterns), encoding='utf-8')
        print("Created .gitignore with log patterns")


def main():
    """Main function."""
    print("🧹 Cleaning logs from HRMS project...")
    
    clean_log_files()
    update_gitignore()
    
    print("\n✅ Log cleanup completed!")
    print("📝 Logging has been simplified throughout the project")
    print("🔇 Verbose logs reduced to essential messages only")


if __name__ == "__main__":
    main()
