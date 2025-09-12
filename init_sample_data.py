"""
Script để khởi tạo dữ liệu mẫu cho HRMS
"""

from app import app, db
from models import Employee, User, SalaryHistory, WorkHistory, Training, Achievement, Contract
from datetime import datetime, timedelta
from random import choice, randint
from utils import calculate_retirement_date

# Danh sách tên mẫu
FIRST_NAMES = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ', 'Đặng']
MIDDLE_NAMES = ['Văn', 'Thị', 'Đức', 'Minh', 'Hoàng', 'Quốc', 'Thành', 'Xuân', 'Thu', 'Hồng']
LAST_NAMES = ['Anh', 'Bình', 'Cường', 'Dũng', 'Giang', 'Hòa', 'Hương', 'Khang', 'Linh', 'Mai', 'Nam', 'Phúc', 'Quân', 'Tâm', 'Thảo', 'Uyên', 'Vân', 'Yến']

DEPARTMENTS = [
    'Phòng Tổ chức - Hành chính',
    'Phòng Tài chính - Kế toán', 
    'Phòng Kế hoạch - Đầu tư',
    'Phòng Kỹ thuật - Công nghệ',
    'Phòng Kinh doanh',
    'Phòng Marketing',
    'Phòng Nhân sự',
    'Phòng Pháp chế',
    'Ban Quản lý dự án'
]

POSITIONS = [
    'Nhân viên',
    'Chuyên viên',
    'Chuyên viên chính',
    'Chuyên viên cao cấp',
    'Phó phòng',
    'Trưởng phòng',
    'Phó giám đốc',
    'Giám đốc'
]

EDUCATION_LEVELS = [
    'Cử nhân Kinh tế',
    'Cử nhân Quản trị kinh doanh',
    'Cử nhân Công nghệ thông tin',
    'Cử nhân Luật',
    'Thạc sĩ Kinh tế',
    'Thạc sĩ Quản trị kinh doanh',
    'Thạc sĩ Công nghệ thông tin',
    'Tiến sĩ Kinh tế'
]

def create_sample_employees():
    """Tạo dữ liệu nhân viên mẫu"""
    employees = []
    
    for i in range(1, 151):  # Tạo 150 nhân viên
        # Tạo tên ngẫu nhiên
        first_name = choice(FIRST_NAMES)
        middle_name = choice(MIDDLE_NAMES)
        last_name = choice(LAST_NAMES)
        full_name = f"{first_name} {middle_name} {last_name}"
        
        # Tạo thông tin cơ bản
        gender = choice(['Nam', 'Nữ'])
        birth_year = randint(1965, 1995)
        birth_month = randint(1, 12)
        birth_day = randint(1, 28)
        date_of_birth = datetime(birth_year, birth_month, birth_day)
        
        # Tạo thông tin công việc
        department = choice(DEPARTMENTS)
        position = choice(POSITIONS)
        start_year = birth_year + randint(22, 30)
        start_date = datetime(start_year, randint(1, 12), randint(1, 28))
        
        # Tạo thông tin lương
        salary_levels = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
        salary_level = choice(salary_levels)
        salary_coefficient = round(2.34 + (i % 10) * 0.1, 2)
        
        # Tạo employee object
        employee = Employee(
            employee_code=f"NV{str(i).zfill(4)}",
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            ethnicity='Kinh',
            religion=choice(['Không', 'Phật giáo', 'Công giáo']),
            hometown=f"{choice(['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ'])}, Việt Nam",
            position=position,
            department=department,
            party_join_date=datetime(start_year + randint(2, 5), randint(1, 12), randint(1, 28)) if randint(0, 2) == 0 else None,
            political_theory_level=choice(['', 'Sơ cấp', 'Trung cấp', 'Cao cấp']) if randint(0, 2) == 0 else '',
            professional_level=choice(EDUCATION_LEVELS),
            phone=f"09{randint(10000000, 99999999)}",
            email=f"{last_name.lower()}.{first_name.lower()}{i}@company.vn",
            address=f"Số {randint(1, 999)}, Đường {randint(1, 100)}, Quận {randint(1, 12)}, TP.HCM",
            start_date=start_date,
            organization_start_date=start_date,
            current_salary_level=salary_level,
            current_salary_coefficient=salary_coefficient,
            position_allowance=0.2 if 'Trưởng' in position else 0.1 if 'Phó' in position else 0,
            last_salary_increase_date=start_date + timedelta(days=randint(365, 1095)),
            status='active'
        )
        
        # Tính ngày nghỉ hưu
        employee.retirement_date = calculate_retirement_date(date_of_birth, gender)
        
        employees.append(employee)
    
    return employees

def create_sample_work_history(employees):
    """Tạo lịch sử công tác mẫu"""
    work_histories = []
    
    for emp in employees[:50]:  # Tạo cho 50 nhân viên đầu
        for j in range(randint(1, 3)):
            work_history = WorkHistory(
                employee_id=emp.id,
                position=choice(['Nhân viên', 'Chuyên viên']),
                department=choice(DEPARTMENTS),
                organization='Công ty ABC' if j == 0 else 'Cơ quan hiện tại',
                start_date=emp.start_date - timedelta(days=365*(j+1)),
                end_date=emp.start_date - timedelta(days=365*j) if j > 0 else None,
                description='Làm việc tại đơn vị'
            )
            work_histories.append(work_history)
    
    return work_histories

def create_sample_trainings(employees):
    """Tạo dữ liệu đào tạo mẫu"""
    trainings = []
    training_types = ['Đại học', 'Sau đại học', 'LLCT', 'QLNN', 'Ngoại ngữ', 'Tin học']
    
    for emp in employees[:80]:  # Tạo cho 80 nhân viên
        for _ in range(randint(1, 2)):
            training = Training(
                employee_id=emp.id,
                training_type=choice(training_types),
                training_name=f"Khóa học {choice(['Quản lý', 'Chuyên môn', 'Kỹ năng'])}",
                institution=choice(['Đại học Kinh tế', 'Đại học Bách khoa', 'Học viện Hành chính']),
                country='Việt Nam',
                degree=choice(['Cử nhân', 'Thạc sĩ', 'Chứng chỉ']),
                major=choice(['Kinh tế', 'Quản trị', 'Công nghệ', 'Luật']),
                start_date=emp.start_date + timedelta(days=randint(365, 1825)),
                end_date=emp.start_date + timedelta(days=randint(1826, 2555)),
                certificate_number=f"CC{randint(1000, 9999)}/2024"
            )
            trainings.append(training)
    
    return trainings

def create_sample_achievements(employees):
    """Tạo dữ liệu thành tích mẫu"""
    achievements = []
    achievement_types = ['Lao động tiên tiến', 'Chiến sỹ thi đua cơ sở', 'Bằng khen']
    
    for emp in employees[:60]:  # Tạo cho 60 nhân viên
        achievement = Achievement(
            employee_id=emp.id,
            achievement_type=choice(achievement_types),
            achievement_name=f"Danh hiệu {choice(['xuất sắc', 'tiên tiến'])} năm 2023",
            level=choice(['Cấp cơ quan', 'Cấp Bộ', 'Cấp Tỉnh']),
            date=datetime(2023, randint(1, 12), randint(1, 28)),
            decision_number=f"QĐ-{randint(100, 999)}/2023",
            issuing_authority='Ban Giám đốc',
            description='Hoàn thành xuất sắc nhiệm vụ'
        )
        achievements.append(achievement)
    
    return achievements

def create_sample_contracts(employees):
    """Tạo dữ liệu hợp đồng mẫu"""
    contracts = []
    contract_types = ['Không xác định thời hạn', 'Có thời hạn 3 năm', 'Có thời hạn 1 năm']
    
    for emp in employees[:100]:  # Tạo cho 100 nhân viên
        contract = Contract(
            employee_id=emp.id,
            contract_number=f"HĐ-{emp.employee_code}-2024",
            contract_type=choice(contract_types),
            start_date=emp.start_date,
            end_date=emp.start_date + timedelta(days=1095) if 'Có thời hạn' in contract_types[0] else None,
            salary=emp.current_salary_coefficient * 1800000,  # Lương cơ sở 1.8 triệu
            position=emp.position,
            department=emp.department,
            status='active'
        )
        contracts.append(contract)
    
    return contracts

def init_sample_data():
    """Khởi tạo toàn bộ dữ liệu mẫu"""
    with app.app_context():
        # Kiểm tra xem đã có dữ liệu chưa
        if Employee.query.count() > 0:
            print("Database đã có dữ liệu. Bỏ qua việc tạo dữ liệu mẫu.")
            return
        
        print("Đang tạo dữ liệu mẫu...")
        
        # Tạo nhân viên
        employees = create_sample_employees()
        for emp in employees:
            db.session.add(emp)
        db.session.commit()
        print(f"✓ Đã tạo {len(employees)} nhân viên")
        
        # Lấy lại employees với ID
        employees = Employee.query.all()
        
        # Tạo lịch sử công tác
        work_histories = create_sample_work_history(employees)
        for wh in work_histories:
            db.session.add(wh)
        db.session.commit()
        print(f"✓ Đã tạo {len(work_histories)} lịch sử công tác")
        
        # Tạo đào tạo
        trainings = create_sample_trainings(employees)
        for tr in trainings:
            db.session.add(tr)
        db.session.commit()
        print(f"✓ Đã tạo {len(trainings)} khóa đào tạo")
        
        # Tạo thành tích
        achievements = create_sample_achievements(employees)
        for ach in achievements:
            db.session.add(ach)
        db.session.commit()
        print(f"✓ Đã tạo {len(achievements)} thành tích")
        
        # Tạo hợp đồng
        contracts = create_sample_contracts(employees)
        for con in contracts:
            db.session.add(con)
        db.session.commit()
        print(f"✓ Đã tạo {len(contracts)} hợp đồng")
        
        print("\n✅ Hoàn thành tạo dữ liệu mẫu!")
        print("Bạn có thể đăng nhập với tài khoản: admin / admin123")

if __name__ == '__main__':
    init_sample_data()
