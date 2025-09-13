from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QListWidget, QMessageBox
from PySide6.QtCore import Qt
import sys

from .db import SessionLocal
from .models import Person
from .init_db import init_db
from .seed import seed_basic_data


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
        # Demo: chấp nhận mọi login (sẽ thay bằng xác thực thật)
        self.main = MainWindow()
        self.main.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRMS - Tra cứu nhân sự")
        layout = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Nhập tên cần tìm...")
        self.search.textChanged.connect(self.on_search)
        self.list = QListWidget()
        layout.addWidget(QLabel("Tra cứu nhân sự"))
        layout.addWidget(self.search)
        layout.addWidget(self.list)
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


def main():
    # Khởi tạo DB nếu chưa có và seed dữ liệu demo lần đầu
    init_db()
    seed_basic_data()

    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())
