#!/usr/bin/env python3
"""
Database Structure Checker for HRMS
"""

import sqlite3
import pandas as pd

def check_database():
    """Check database structure and content."""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("📊 Database Tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check employees table structure
        if ('employees',) in tables:
            cursor.execute("PRAGMA table_info(employees);")
            columns = cursor.fetchall()
            print("\n👥 Employees Table Structure:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Check sample data
            cursor.execute("SELECT COUNT(*) FROM employees;")
            count = cursor.fetchone()[0]
            print(f"\n📈 Employees Count: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM employees LIMIT 3;")
                sample = cursor.fetchall()
                print("\n📋 Sample Data:")
                for row in sample:
                    print(f"  {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database()
