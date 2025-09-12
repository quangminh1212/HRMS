#!/usr/bin/env python3
"""
Generate test data cho HRMS - 100 nhân viên với dữ liệu hợp lý
Tạo file Excel và import vào database
"""

import pandas as pd
import random
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
from pathlib import Path

# Vietnamese names and data
VIETNAMESE_SURNAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
    "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Vương", "Đinh", "Cao", "Mai",
    "Lâm", "Đào", "Tran", "Thái", "Hà", "Đoàn", "Trịnh", "Kiều", "Lương", "Tô"
]

MALE_MIDDLE_NAMES = [
    "Văn", "Anh", "Minh", "Thành", "Đức", "Hoàng", "Quang", "Tuấn", "Hữu", "Công",
    "Thanh", "Duy", "Tấn", "Xuân", "Bảo", "Huy", "Khang", "Phúc", "Thịnh", "Trung"
]

FEMALE_MIDDLE_NAMES = [
    "Thị", "Minh", "Thu", "Hương", "Lan", "Linh", "Mai", "Ngọc", "Phương", "Thúy",
    "Huyền", "Kim", "Thanh", "Quỳnh", "Tuyết", "Yến", "Xuân", "Hồng", "Vân", "Như"
]

MALE_GIVEN_NAMES = [
    "An", "Bình", "Cường", "Dũng", "Đạt", "Giang", "Hải", "Khoa", "Long", "Nam",
    "Phong", "Quân", "Sơn", "Tùng", "Vinh", "Hưng", "Đức", "Thành", "Minh", "Tuấn",
    "Hoàng", "Tân", "Kiên", "Trung", "Huy", "Bảo", "Thắng", "Hiệp", "Phú", "Toàn"
]

FEMALE_GIVEN_NAMES = [
    "Anh", "Bích", "Chi", "Diệu", "Hà", "Linh", "Nga", "Oanh", "Phương", "Quỳnh",
    "Thảo", "Uyên", "Vân", "Yến", "Hương", "Mai", "Nhung", "Trang", "Hiền", "Ly",
    "Hạnh", "Hằng", "Huyền", "Khánh", "Lam", "My", "Nhi", "Thúy", "Tâm", "Vy"
]

DEPARTMENTS = [
    "Phòng Tổ chức - Cán bộ",
    "Phòng Kế hoạch - Tài chính", 
    "Phòng Hành chính - Quản trị",
    "Phòng Công nghệ thông tin",
    "Phòng Marketing",
    "Phòng Kinh doanh",
    "Phòng Nhân sự",
    "Phòng Kế toán",
    "Phòng Pháp chế",
    "Phòng Đầu tư phát triển",
    "Ban Giám đốc",
    "Ban Kiểm soát nội bộ"
]

POSITIONS = {
    "Ban Giám đốc": ["Giám đốc", "Phó Giám đốc", "Trợ lý Giám đốc"],
    "Ban Kiểm soát nội bộ": ["Trưởng ban kiểm soát", "Kiểm soát viên"],
    "Phòng Tổ chức - Cán bộ": ["Trưởng phòng", "Phó trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Kế hoạch - Tài chính": ["Trưởng phòng", "Phó trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Hành chính - Quản trị": ["Trưởng phòng", "Phó trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Công nghệ thông tin": ["Trưởng phòng", "Chuyên viên chính", "Chuyên viên", "Kỹ thuật viên"],
    "Phòng Marketing": ["Trưởng phòng", "Phó trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Kinh doanh": ["Trưởng phòng", "Phó trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Nhân sự": ["Trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Kế toán": ["Trưởng phòng", "Kế toán trưởng", "Chuyên viên", "Nhân viên"],
    "Phòng Pháp chế": ["Trưởng phòng", "Chuyên viên", "Nhân viên"],
    "Phòng Đầu tư phát triển": ["Trưởng phòng", "Chuyên viên chính", "Chuyên viên"]
}

SALARY_GRADES = {
    "Giám đốc": ("A4", 12, 8.5),
    "Phó Giám đốc": ("A3", 10, 7.2), 
    "Trưởng ban kiểm soát": ("A3", 9, 6.8),
    "Trưởng phòng": ("A2", 8, 5.8),
    "Phó trưởng phòng": ("A2", 6, 4.9),
    "Kế toán trưởng": ("A2", 7, 5.2),
    "Chuyên viên chính": ("A1", 5, 4.2),
    "Chuyên viên": ("A1", 4, 3.8),
    "Kỹ thuật viên": ("A0", 4, 3.2),
    "Kiểm soát viên": ("A1", 4, 3.6),
    "Nhân viên": ("A0", 3, 2.8),
    "Trợ lý Giám đốc": ("A1", 4, 3.9)
}

ETHNICITIES = ["Kinh", "Tày", "Thái", "Hoa", "Khmer", "Mường", "Nùng", "H'Mông"]
RELIGIONS = ["Không", "Phật giáo", "Công giáo", "Cao Đài", "Hòa Hảo", "Tin Lành"]

PROVINCES = [
    "Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "Quảng Ninh", "Khánh Hòa", "Lâm Đồng", "Bình Dương", "Đồng Nai",
    "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu",
    "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Phước", "Bình Thuận",
    "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông", "Điện Biên"
]

UNIVERSITIES = [
    "Đại học Bách khoa Hà Nội",
    "Đại học Quốc gia Hà Nội",
    "Đại học Kinh tế Quốc dân",
    "Đại học Ngoại thương",
    "Đại học Luật Hà Nội",
    "Đại học Công đoàn",
    "Đại học Sư phạm Hà Nội",
    "Đại học Bách khoa TP.HCM",
    "Đại học Quốc gia TP.HCM",
    "Đại học Kinh tế TP.HCM",
    "Đại học Tôn Đức Thắng",
    "Đại học Công nghiệp TP.HCM"
]

MAJORS = [
    "Quản trị kinh doanh", "Kế toán", "Tài chính - Ngân hàng", "Marketing",
    "Công nghệ thông tin", "Kỹ thuật phần mềm", "Luật", "Kinh tế",
    "Nhân sự", "Logistics", "Ngoại ngữ", "Truyền thông", "Thiết kế"
]

def generate_vietnamese_name(gender):
    """Tạo tên tiếng Việt"""
    surname = random.choice(VIETNAMESE_SURNAMES)
    
    if gender == "Nam":
        middle = random.choice(MALE_MIDDLE_NAMES)
        given = random.choice(MALE_GIVEN_NAMES)
    else:
        middle = random.choice(FEMALE_MIDDLE_NAMES)
        given = random.choice(FEMALE_GIVEN_NAMES)
    
    return f"{surname} {middle} {given}"

def generate_employee_data(num_employees=100):
    """Generate dữ liệu 100 nhân viên"""
    employees = []
    
    for i in range(num_employees):
        # Basic info
        gender = random.choice(["Nam", "Nữ"])
        full_name = generate_vietnamese_name(gender)
        
        # Age from 25 to 60
        age = random.randint(25, 60)
        birth_date = date.today() - relativedelta(years=age, days=random.randint(0, 365))
        
        # Department and position
        department = random.choice(DEPARTMENTS)
        position = random.choice(POSITIONS[department])
        
        # Salary info
        if position in SALARY_GRADES:
            grade, level, coeff = SALARY_GRADES[position]
            # Add some variation
            level = max(1, level + random.randint(-2, 2))
            coeff = round(coeff + random.uniform(-0.5, 0.5), 2)
        else:
            grade, level, coeff = ("A0", 3, 2.8)
        
        # Work dates
        work_years = random.randint(2, age-23)  # Ít nhất 2 năm kinh nghiệm
        social_insurance_start = birth_date + relativedelta(years=23) + relativedelta(days=random.randint(0, 365*2))
        org_start = social_insurance_start + relativedelta(months=random.randint(0, 24))
        
        # Salary date (last increase)
        months_since_increase = random.randint(6, 48)
        current_salary_date = date.today() - relativedelta(months=months_since_increase)
        
        # Party date (some people)
        party_date = None
        if random.random() < 0.4 and work_years >= 5:  # 40% là đảng viên, cần ít nhất 5 năm công tác
            party_years = random.randint(5, work_years)
            party_date = social_insurance_start + relativedelta(years=party_years)
        
        # Contact info
        phone = f"0{random.choice([3,7,8,9])}{random.randint(10000000, 99999999)}"
        email_name = full_name.lower().replace(" ", "").replace("đ", "d").replace("ă", "a").replace("â", "a")
        email = f"{email_name[:10]}@company.com"
        
        employee = {
            "STT": i + 1,
            "Họ và tên": full_name,
            "Ngày sinh": birth_date.strftime("%d/%m/%Y"),
            "Giới tính": gender,
            "Dân tộc": np.random.choice(ETHNICITIES, p=[0.85, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]),
            "Tôn giáo": np.random.choice(RELIGIONS, p=[0.6, 0.15, 0.15, 0.03, 0.02, 0.05]),
            "Quê quán": random.choice(PROVINCES),
            "Chức vụ": position,
            "Đơn vị": department, 
            "Ngày vào Đảng": party_date.strftime("%d/%m/%Y") if party_date else "",
            "Trình độ LLCT": random.choice(["Sơ cấp", "Trung cấp", "Cao cấp", ""]),
            "Trình độ CM": random.choice(["Đại học", "Thạc sĩ", "Tiến sĩ"]),
            "Trường": random.choice(UNIVERSITIES),
            "Ngành": random.choice(MAJORS),
            "Ngạch lương": grade,
            "Bậc lương": level,
            "Hệ số lương": coeff,
            "Ngày hưởng lương": current_salary_date.strftime("%d/%m/%Y"),
            "Phụ cấp chức vụ": round(random.uniform(0, 1.5), 1) if "trưởng" in position.lower() else 0,
            "Ngày bắt đầu BHXH": social_insurance_start.strftime("%d/%m/%Y"),
            "Ngày vào cơ quan": org_start.strftime("%d/%m/%Y"),
            "Quy hoạch hiện tại": get_planning(position, department),
            "Điện thoại": phone,
            "Email": email,
            "Đánh giá gần nhất": random.choice(["Hoàn thành xuất sắc", "Hoàn thành tốt", "Hoàn thành"]),
            "Khen thưởng": get_random_awards(),
            "Trạng thái": random.choice(["Đang công tác", "Đang công tác", "Đang công tác", "Nghỉ thai sản", "Đi học"])
        }
        
        employees.append(employee)
    
    return employees

def get_planning(position, department):
    """Tạo quy hoạch phù hợp"""
    if "Giám đốc" in position:
        return ""
    elif "Trưởng phòng" in position:
        return "Phó Giám đốc" if random.random() < 0.3 else ""
    elif "Phó trưởng phòng" in position:
        return "Trưởng phòng"
    elif "Chuyên viên chính" in position:
        return random.choice(["Phó trưởng phòng", ""])
    elif "Chuyên viên" in position:
        return random.choice(["Chuyên viên chính", "Phó trưởng phòng", ""])
    else:
        return ""

def get_random_awards():
    """Tạo khen thưởng ngẫu nhiên"""
    awards = []
    if random.random() < 0.8:  # 80% có khen thưởng
        possible_awards = [
            "Lao động tiên tiến 2023",
            "Lao động tiên tiến 2022", 
            "Chiến sĩ thi đua cơ sở 2023",
            "Bằng khen cấp Bộ 2022",
            "Giấy khen 2023"
        ]
        num_awards = random.randint(1, 3)
        awards = random.sample(possible_awards, min(num_awards, len(possible_awards)))
    
    return "; ".join(awards)

def create_excel_file(employees_data):
    """Tạo file Excel"""
    df = pd.DataFrame(employees_data)
    
    # Tạo thư mục nếu chưa có
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    filename = exports_dir / f"nhan_su_test_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Tạo file Excel với formatting
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Sheet chính
        df.to_excel(writer, sheet_name='Danh sách nhân sự', index=False)
        
        # Tạo sheet thống kê
        stats_data = {
            "Thống kê": [
                "Tổng số nhân sự",
                "Nam", 
                "Nữ",
                "Trình độ Đại học",
                "Trình độ Thạc sĩ", 
                "Trình độ Tiến sĩ",
                "Đảng viên",
                "Tuổi trung bình"
            ],
            "Số lượng": [
                len(df),
                len(df[df['Giới tính'] == 'Nam']),
                len(df[df['Giới tính'] == 'Nữ']),
                len(df[df['Trình độ CM'] == 'Đại học']),
                len(df[df['Trình độ CM'] == 'Thạc sĩ']),
                len(df[df['Trình độ CM'] == 'Tiến sĩ']),
                len(df[df['Ngày vào Đảng'] != '']),
                f"{calculate_average_age(df):.1f} tuổi"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_excel(writer, sheet_name='Thống kê', index=False)
        
        # Sheet theo phòng ban
        dept_stats = df.groupby('Đơn vị').size().reset_index(name='Số người')
        dept_stats.to_excel(writer, sheet_name='Theo phòng ban', index=False)
    
    print(f"✅ Đã tạo file Excel: {filename}")
    print(f"📊 Dữ liệu {len(employees_data)} nhân viên")
    return filename

def calculate_average_age(df):
    """Tính tuổi trung bình"""
    today = date.today()
    ages = []
    for birth_str in df['Ngày sinh']:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        ages.append(age)
    return sum(ages) / len(ages)

def import_to_database(employees_data):
    """Import dữ liệu vào database"""
    try:
        from src.models.models_enhanced import init_enhanced_database, Employee, Education, get_engine
        from sqlalchemy.orm import sessionmaker
        
        # Khởi tạo database
        engine = init_enhanced_database()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Xóa dữ liệu cũ (nếu có)
        session.query(Employee).delete()
        session.commit()
        
        imported_count = 0
        
        for emp_data in employees_data:
            try:
                # Chuyển đổi dữ liệu
                birth_date = datetime.strptime(emp_data['Ngày sinh'], "%d/%m/%Y").date()
                party_date = None
                if emp_data['Ngày vào Đảng']:
                    party_date = datetime.strptime(emp_data['Ngày vào Đảng'], "%d/%m/%Y").date()
                
                salary_date = datetime.strptime(emp_data['Ngày hưởng lương'], "%d/%m/%Y").date()
                insurance_start = datetime.strptime(emp_data['Ngày bắt đầu BHXH'], "%d/%m/%Y").date()
                org_start = datetime.strptime(emp_data['Ngày vào cơ quan'], "%d/%m/%Y").date()
                
                # Map giới tính
                from src.models.models_enhanced import GenderEnum, WorkStatusEnum, EducationLevelEnum, PoliticalTheoryEnum
                
                gender = GenderEnum.MALE if emp_data['Giới tính'] == 'Nam' else GenderEnum.FEMALE
                
                # Map trình độ
                education_map = {
                    'Đại học': EducationLevelEnum.BACHELOR,
                    'Thạc sĩ': EducationLevelEnum.MASTER, 
                    'Tiến sĩ': EducationLevelEnum.DOCTOR
                }
                education_level = education_map.get(emp_data['Trình độ CM'], EducationLevelEnum.BACHELOR)
                
                # Map LLCT
                political_map = {
                    'Sơ cấp': PoliticalTheoryEnum.BASIC,
                    'Trung cấp': PoliticalTheoryEnum.INTERMEDIATE,
                    'Cao cấp': PoliticalTheoryEnum.ADVANCED
                }
                political_level = political_map.get(emp_data['Trình độ LLCT']) if emp_data['Trình độ LLCT'] else None
                
                # Map trạng thái
                status_map = {
                    'Đang công tác': WorkStatusEnum.ACTIVE,
                    'Nghỉ thai sản': WorkStatusEnum.MATERNITY_LEAVE,
                    'Đi học': WorkStatusEnum.STUDY_LEAVE
                }
                work_status = status_map.get(emp_data['Trạng thái'], WorkStatusEnum.ACTIVE)
                
                # Tạo employee
                employee = Employee(
                    full_name=emp_data['Họ và tên'],
                    date_of_birth=birth_date,
                    gender=gender,
                    ethnicity=emp_data['Dân tộc'],
                    religion=emp_data['Tôn giáo'] if emp_data['Tôn giáo'] != 'Không' else None,
                    hometown=emp_data['Quê quán'],
                    party_join_date=party_date,
                    position=emp_data['Chức vụ'],
                    department=emp_data['Đơn vị'],
                    political_theory_level=political_level,
                    education_level=education_level,
                    work_status=work_status,
                    current_salary_grade=emp_data['Ngạch lương'],
                    current_salary_level=int(emp_data['Bậc lương']),
                    current_salary_coefficient=float(emp_data['Hệ số lương']),
                    current_salary_date=salary_date,
                    position_allowance=float(emp_data['Phụ cấp chức vụ']) if emp_data['Phụ cấp chức vụ'] else None,
                    social_insurance_start_date=insurance_start,
                    organization_start_date=org_start,
                    current_planning=emp_data['Quy hoạch hiện tại'] if emp_data['Quy hoạch hiện tại'] else None,
                    phone=emp_data['Điện thoại'],
                    email=emp_data['Email']
                )
                
                session.add(employee)
                session.flush()  # Để lấy ID
                
                # Thêm thông tin giáo dục
                education = Education(
                    employee_id=employee.id,
                    level=education_level,
                    field_of_study=emp_data['Ngành'],
                    institution=emp_data['Trường'],
                    country="Việt Nam",
                    study_mode="Chính quy"
                )
                session.add(education)
                
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Lỗi import nhân viên {emp_data['Họ và tên']}: {str(e)}")
                continue
        
        session.commit()
        session.close()
        
        print(f"✅ Đã import {imported_count}/{len(employees_data)} nhân viên vào database")
        return imported_count
        
    except Exception as e:
        print(f"❌ Lỗi khi import database: {str(e)}")
        return 0

def main():
    """Main function"""
    print("🚀 Bắt đầu tạo dữ liệu test cho HRMS...")
    
    # Generate data
    employees_data = generate_employee_data(100)
    
    # Create Excel file
    excel_file = create_excel_file(employees_data)
    
    # Import to database
    imported_count = import_to_database(employees_data)
    
    print("\n" + "="*60)
    print("📊 KẾT QUẢ TẠO DỮ LIỆU TEST")
    print("="*60)
    print(f"✅ File Excel: {excel_file}")
    print(f"✅ Nhân viên trong Excel: {len(employees_data)} người")
    print(f"✅ Import vào database: {imported_count} người")
    print(f"📱 Có thể test ngay trên HRMS tại: http://localhost:8501")
    print("👤 Login: admin / admin123")
    print("="*60)

if __name__ == "__main__":
    main()
