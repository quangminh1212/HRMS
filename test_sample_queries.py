#!/usr/bin/env python3
"""
Test các query mẫu trên dữ liệu 100 nhân viên
Kiểm tra các tính năng HRMS với dữ liệu thực
"""

from src.models.models_enhanced import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def test_queries():
    """Test các query cơ bản"""
    Session = sessionmaker(bind=get_engine())
    session = Session()
    
    print("🔍 TEST CÁC CHỨC NĂNG HRMS VỚI DỮ LIỆU THỰC")
    print("="*60)
    
    # 1. Thống kê tổng quan
    total_employees = session.query(Employee).count()
    male_count = session.query(Employee).filter(Employee.gender == GenderEnum.MALE).count()
    female_count = session.query(Employee).filter(Employee.gender == GenderEnum.FEMALE).count()
    
    print(f"📊 THỐNG KÊ TỔNG QUAN:")
    print(f"   - Tổng nhân sự: {total_employees} người")
    print(f"   - Nam: {male_count} người ({male_count/total_employees*100:.1f}%)")
    print(f"   - Nữ: {female_count} người ({female_count/total_employees*100:.1f}%)")
    
    # 2. Theo phòng ban
    print(f"\n📋 THEO PHÒNG BAN:")
    dept_stats = session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()
    for dept, count in sorted(dept_stats, key=lambda x: x[1], reverse=True):
        print(f"   - {dept}: {count} người")
    
    # 3. Theo chức vụ
    print(f"\n💼 THEO CHỨC VỤ:")
    pos_stats = session.query(Employee.position, func.count(Employee.id)).group_by(Employee.position).all()
    for pos, count in sorted(pos_stats, key=lambda x: x[1], reverse=True)[:10]:
        print(f"   - {pos}: {count} người")
    
    # 4. Sắp nghỉ hưu (trong 2 năm tới)
    print(f"\n⏰ SẮP NGHỈ HƯU (trong 24 tháng):")
    retirement_candidates = []
    for emp in session.query(Employee).all():
        if emp.date_of_birth:
            retirement_age = 60 if emp.gender == GenderEnum.FEMALE else 62
            retirement_date = date(
                emp.date_of_birth.year + retirement_age,
                emp.date_of_birth.month,
                emp.date_of_birth.day
            )
            months_to_retirement = (retirement_date.year - date.today().year) * 12 + (retirement_date.month - date.today().month)
            
            if 0 < months_to_retirement <= 24:
                retirement_candidates.append((emp.full_name, emp.department, months_to_retirement))
    
    retirement_candidates.sort(key=lambda x: x[2])
    for name, dept, months in retirement_candidates[:10]:
        print(f"   - {name} ({dept}): còn {months} tháng")
    
    # 5. Đủ điều kiện nâng lương (giả sử 36 tháng)
    print(f"\n💰 ĐỦ ĐIỀU KIỆN NÂNG LƯƠNG:")
    salary_candidates = []
    for emp in session.query(Employee).all():
        if emp.current_salary_date:
            months_since_increase = (date.today().year - emp.current_salary_date.year) * 12 + (date.today().month - emp.current_salary_date.month)
            
            # Giả sử chuyên viên cần 36 tháng, nhân viên cần 24 tháng
            required_months = 24 if "nhân viên" in emp.position.lower() else 36
            
            if months_since_increase >= required_months:
                salary_candidates.append((emp.full_name, emp.position, months_since_increase, emp.current_salary_coefficient))
    
    salary_candidates.sort(key=lambda x: x[2], reverse=True)
    for name, pos, months, coeff in salary_candidates[:10]:
        print(f"   - {name} ({pos}): {months} tháng, hệ số {coeff}")
    
    # 6. Theo trình độ
    print(f"\n🎓 THEO TRÌNH ĐỘ:")
    edu_stats = session.query(Employee.education_level, func.count(Employee.id)).group_by(Employee.education_level).all()
    for edu, count in edu_stats:
        if edu:
            print(f"   - {edu.value}: {count} người")
    
    # 7. Đảng viên
    party_members = session.query(Employee).filter(Employee.party_join_date.isnot(None)).count()
    print(f"\n🏛️ ĐẢNG VIÊN: {party_members} người ({party_members/total_employees*100:.1f}%)")
    
    session.close()
    
    print("\n" + "="*60)
    print("✅ Test hoàn tất - Dữ liệu test đã sẵn sàng cho HRMS!")
    print("🚀 Có thể chạy ứng dụng và test các tính năng:")
    print("   python run.py")
    print("   http://localhost:3000")
    print("="*60)

if __name__ == "__main__":
    test_queries()
