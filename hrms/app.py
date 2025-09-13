from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QListWidget, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import sys
from pathlib import Path

from docx import Document

from .db import SessionLocal
from .models import Person, User
from .init_db import init_db
from .seed import seed_basic_data
from .security import verify_password
from .salary import list_due_in_window, export_due_to_excel


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRMS - Đăng nhập")
        layout = QVBoxLayout()
        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        self.pw = QLineEdit()
        self.pw.setPlaceholderText("Password")
        self.pw.setEchoMode(QLineEdit.Password)
        self.btn = QPushButton("Login")
        self.btn.clicked.connect(self.do_login)
        layout.addWidget(self.user)
        layout.addWidget(self.pw)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def do_login(self):
        username = self.user.text().strip()
        password = self.pw.text()
        if not username or not password:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập username và password")
            return
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user or not verify_password(password, user.password_hash):
                QMessageBox.critical(self, "Đăng nhập thất bại", "Sai thông tin đăng nhập")
                return
        finally:
            db.close()
        self.main = MainWindow(current_user=username)
        self.main.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, current_user: str):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle(f"HRMS - Tra cứu nhân sự ({current_user})")
        layout = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Nhập tên cần tìm...")
        self.search.textChanged.connect(self.on_search)
        self.list = QListWidget()
        btn_layout = QHBoxLayout()
        self.btn_export = QPushButton("Xuất trích ngang")
        self.btn_export.clicked.connect(self.export_selected)
        self.btn_due = QPushButton("Nâng lương quý này")
        self.btn_due.clicked.connect(self.show_due)
        self.btn_appointment = QPushButton("Kiểm tra bổ nhiệm")
        self.btn_appointment.clicked.connect(self.check_appointment)
        self.btn_work = QPushButton("Thêm quá trình công tác")
        self.btn_work.clicked.connect(self.add_work_process)
        self.btn_export_work = QPushButton("Xuất quá trình công tác")
        self.btn_export_work.clicked.connect(self.export_work_process)
        self.btn_report = QPushButton("Báo cáo nhanh")
        self.btn_report.clicked.connect(self.quick_report)
        self.btn_import = QPushButton("Import Excel nhân sự")
        self.btn_import.clicked.connect(self.import_excel)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_due)
        btn_layout.addWidget(self.btn_appointment)
        btn_layout.addWidget(self.btn_work)
        btn_layout.addWidget(self.btn_export_work)
        btn_layout.addWidget(self.btn_report)
        btn_layout.addWidget(self.btn_import)
        layout.addWidget(QLabel("Tra cứu nhân sự"))
        layout.addWidget(self.search)
        layout.addWidget(self.list)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.on_search("")

    def on_search(self, text: str):
        db = SessionLocal()
        try:
            q = db.query(Person)
            if text:
                like = f"%{text}%"
                q = q.filter(Person.full_name.ilike(like))
            people = q.order_by(Person.full_name).all()
            self.list.clear()
            for p in people:
                self.list.addItem(f"{p.full_name} - {p.code}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def current_person(self):
        item = self.list.currentItem()
        if not item:
            return None, None
        code = item.text().split(" - ")[-1]
        db = SessionLocal()
        p = db.query(Person).filter_by(code=code).first()
        return db, p

    def export_selected(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.information(self, "Chưa chọn", "Vui lòng chọn một nhân sự trong danh sách")
            return
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.critical(self, "Lỗi", "Không tìm thấy nhân sự đã chọn")
                return
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"trich_ngang_{person.code}.docx"
            doc = Document()
            doc.add_heading("Trích ngang nhân sự", level=1)
            rows = [
                ("Họ và tên", person.full_name or ""),
                ("Mã", person.code or ""),
                ("Ngày sinh", person.dob.isoformat() if person.dob else ""),
                ("Giới tính", person.gender or ""),
                ("Dân tộc", person.ethnicity or ""),
                ("Tôn giáo", person.religion or ""),
                ("Quê quán", person.hometown or ""),
                ("Chức danh", person.position.name if person.position else ""),
                ("Đơn vị", person.unit.name if person.unit else ""),
                ("Ngày vào Đảng", person.party_joined_date.isoformat() if person.party_joined_date else ""),
                ("LLCT", person.llct_level or ""),
                ("Trình độ chuyên môn", person.professional_level or ""),
                ("Tình trạng công tác", person.status or ""),
                ("Điện thoại", person.phone or ""),
                ("Email", person.email or ""),
            ]
            table = doc.add_table(rows=1, cols=2)
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = "Trường"
            hdr_cells[1].text = "Giá trị"
            for k, v in rows:
                row_cells = table.add_row().cells
                row_cells[0].text = k
                row_cells[1].text = v
            doc.save(str(file_path))
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def show_due(self):
        from datetime import date
        start, end = quarter_window(date.today())
        db = SessionLocal()
        try:
            items = list_due_in_window(db, start, end)
            if not items:
                QMessageBox.information(self, "Kết quả", "Không có nhân sự đến hạn trong quý này")
                return
            Path("exports").mkdir(exist_ok=True)
            xlsx = Path("exports") / f"nang_luong_quy_{end.year}_Q{((end.month-1)//3)+1}.xlsx"
            export_due_to_excel(items, str(xlsx))
            QMessageBox.information(self, "Thành công", f"Đã xuất danh sách: {xlsx}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def check_appointment(self):
        from .appointment import check_appointment_eligibility
        from PySide6.QtWidgets import QInputDialog
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            target, ok = QInputDialog.getText(self, "Vị trí bổ nhiệm", "Nhập vị trí cần kiểm tra:")
            if not ok or not target:
                return
            ok_eligible, reasons = check_appointment_eligibility(db, person, target)
            if ok_eligible:
                QMessageBox.information(self, "Kết quả", f"Đủ điều kiện bổ nhiệm vị trí: {target}")
            else:
                QMessageBox.warning(self, "Chưa đạt", "\n".join(reasons) or "Chưa đủ điều kiện")
        finally:
            if db:
                db.close()

    def add_work_process(self):
        from PySide6.QtWidgets import QInputDialog
        from datetime import date
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            unit, ok = QInputDialog.getText(self, "Đơn vị", "Nhập đơn vị:")
            if not ok or not unit:
                return
            pos, ok = QInputDialog.getText(self, "Chức vụ", "Nhập chức vụ:")
            if not ok or not pos:
                return
            from .models import WorkProcess
            # đơn giản: lấy start_date = ngày hiện tại
            wp = WorkProcess(person_id=person.id, unit=unit, position=pos, start_date=date.today())
            db.add(wp)
            db.commit()
            QMessageBox.information(self, "Thành công", "Đã thêm quá trình công tác")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def export_work_process(self):
        from .models import WorkProcess
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            wps = db.query(WorkProcess).filter_by(person_id=person.id).order_by(WorkProcess.start_date).all()
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"work_process_{person.code}.docx"
            doc = Document()
            doc.add_heading(f"Quá trình công tác - {person.full_name}", level=1)
            t = doc.add_table(rows=1, cols=3)
            t.rows[0].cells[0].text = "Từ ngày"
            t.rows[0].cells[1].text = "Đơn vị"
            t.rows[0].cells[2].text = "Chức vụ"
            for w in wps:
                row = t.add_row().cells
                row[0].text = (w.start_date.isoformat() + (" -> " + w.end_date.isoformat() if w.end_date else ""))
                row[1].text = w.unit or ""
                row[2].text = w.position or ""
            doc.save(str(file_path))
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def quick_report(self):
        from datetime import date
        from .reporting import compute_annual_summary, compute_demographics, export_report_to_excel
        year = date.today().year
        db = SessionLocal()
        try:
            summary = compute_annual_summary(db, year)
            demo = compute_demographics(db, date.today())
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"bao_cao_nhanh_{year}.xlsx"
            export_report_to_excel(summary, demo, str(file_path))
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def import_excel(self):
        from PySide6.QtWidgets import QFileDialog
        from .importer import import_persons_from_excel
        db = SessionLocal()
        try:
            xlsx_path, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel", "", "Excel Files (*.xlsx)")
            if not xlsx_path:
                return
            result = import_persons_from_excel(db, xlsx_path)
            if not result.get("ok"):
                QMessageBox.critical(self, "Import lỗi", result.get("error", "Lỗi không rõ"))
                return
            QMessageBox.information(self, "Import thành công", f"Tạo mới: {result['created']}, Cập nhật: {result['updated']}")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()


def quarter_window(d):
    # cảnh báo vào ngày 15 của tháng 2/5/8/11, nhưng ở đây tạo cửa sổ quý
    q = (d.month - 1) // 3 + 1
    start_month = 3 * (q - 1) + 1
    from datetime import date as _date
    start = _date(d.year, start_month, 1)
    # end: ngày cuối tháng trong quý
    end_month = start_month + 2
    from calendar import monthrange
    last_day = monthrange(d.year, end_month)[1]
    end = _date(d.year, end_month, last_day)
    return start, end


def main():
    # Khởi tạo DB nếu chưa có và seed dữ liệu demo lần đầu
    init_db()
    seed_basic_data()

    # Khởi động scheduler cảnh báo in-app
    try:
        from .scheduler import schedule_jobs
        schedule_jobs()
    except Exception as e:
        print(f"[WARN] Scheduler not started: {e}")

    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())
