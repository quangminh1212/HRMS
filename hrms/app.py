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
        btn_layout.addWidget(self.btn_export)
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

    def export_selected(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.information(self, "Chưa chọn", "Vui lòng chọn một nhân sự trong danh sách")
            return
        code = item.text().split(" - ")[-1]
        db = SessionLocal()
        try:
            person = db.query(Person).filter_by(code=code).first()
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
            db.close()


def main():
    # Khởi tạo DB nếu chưa có và seed dữ liệu demo lần đầu
    init_db()
    seed_basic_data()

    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())
