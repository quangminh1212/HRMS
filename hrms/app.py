from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QListWidget, QMessageBox, QHBoxLayout, QComboBox, QDialog, QFormLayout
)
from PySide6.QtCore import Qt, QTimer
import sys
from pathlib import Path

from docx import Document

from .db import SessionLocal
from .models import Person, User
from .init_db import init_db
from .seed import seed_basic_data
from .security import verify_password
from .salary import list_due_in_window, export_due_to_excel
from .audit import log_action
from .scheduler import NOTIFY_QUEUE


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
            user_info = {"id": user.id, "username": user.username, "role": user.role, "unit_id": user.unit_id}
        finally:
            db.close()
        self.main = MainWindow(current_user=user_info)
        self.main.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, current_user: dict):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle(f"HRMS - Tra cứu nhân sự ({current_user.get('username')})")
        layout = QVBoxLayout()

        # Hàng filter
        filter_bar = QHBoxLayout()
        self.filter_unit = QComboBox()
        self.filter_unit.addItem("-- Đơn vị --", None)
        self.filter_position = QComboBox()
        self.filter_position.addItem("-- Chức vụ --", None)
        self.filter_status = QComboBox()
        self.filter_status.addItems(["-- Trạng thái --", "Đang công tác", "Nghỉ thai sản", "Đi học", "Thôi việc"])  # có thể mở rộng
        self.btn_filter_refresh = QPushButton("Lọc")
        self.btn_filter_refresh.clicked.connect(lambda: self.on_search(self.search.text()))
        self.btn_manage_users = QPushButton("Quản lý người dùng")
        self.btn_manage_users.clicked.connect(self.manage_users)
        filter_bar.addWidget(self.filter_unit)
        filter_bar.addWidget(self.filter_position)
        filter_bar.addWidget(self.filter_status)
        filter_bar.addWidget(self.btn_filter_refresh)
        filter_bar.addWidget(self.btn_manage_users)

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
        self.btn_ins_add = QPushButton("Thêm sự kiện BHXH")
        self.btn_ins_add.clicked.connect(self.add_insurance)
        self.btn_ins_export = QPushButton("Xuất Excel BHXH")
        self.btn_ins_export.clicked.connect(self.export_insurance)
        self.btn_contract_add = QPushButton("Thêm HĐ")
        self.btn_contract_add.clicked.connect(self.add_contract)
        self.btn_contract_export = QPushButton("Xuất HĐ")
        self.btn_contract_export.clicked.connect(self.export_contract)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_due)
        btn_layout.addWidget(self.btn_appointment)
        btn_layout.addWidget(self.btn_work)
        btn_layout.addWidget(self.btn_export_work)
        btn_layout.addWidget(self.btn_contract_add)
        btn_layout.addWidget(self.btn_contract_export)
        btn_layout.addWidget(self.btn_report)
        btn_layout.addWidget(self.btn_import)
        btn_layout.addWidget(self.btn_ins_add)
        btn_layout.addWidget(self.btn_ins_export)
        layout.addWidget(QLabel("Tra cứu nhân sự"))
        layout.addWidget(self.search)
        layout.addWidget(self.list)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setLayout(layout)

        # RBAC: áp dụng quyền theo role
        self.apply_role_permissions()

        # Tải danh mục filter
        self.load_filters()

        # Thiết lập timer để lấy thông báo từ scheduler và popup
        self.timer = QTimer(self)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.drain_notifications)
        self.timer.start()

        self.refresh()

    def refresh(self):
        self.on_search("")

    def on_search(self, text: str):
        db = SessionLocal()
        try:
            q = db.query(Person)
            # Lọc theo tên
            if text:
                like = f"%{text}%"
                q = q.filter(Person.full_name.ilike(like))
            # Lọc theo đơn vị/chức vụ/trạng thái
            unit_id = self.filter_unit.currentData()
            if unit_id:
                q = q.filter(Person.unit_id == unit_id)
            pos_id = self.filter_position.currentData()
            if pos_id:
                q = q.filter(Person.position_id == pos_id)
            st = self.filter_status.currentText()
            if st and not st.startswith("--"):
                q = q.filter(Person.status.ilike(f"%{st}%"))
            people = q.order_by(Person.full_name).all()
            self.list.clear()
            for p in people:
                self.list.addItem(f"{p.full_name} - {p.code}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def load_filters(self):
        db = SessionLocal()
        try:
            self.filter_unit.blockSignals(True)
            self.filter_position.blockSignals(True)
            # Units
            from .models import Unit, Position
            self.filter_unit.clear()
            self.filter_unit.addItem("-- Đơn vị --", None)
            role = (self.current_user.get('role') or '').lower()
            only_unit_id = self.current_user.get('unit_id') if role not in ('admin','hr') else None
            units_q = db.query(Unit).order_by(Unit.name)
            if only_unit_id:
                units_q = units_q.filter(Unit.id == only_unit_id)
            for u in units_q.all():
                self.filter_unit.addItem(u.name, u.id)
            # Positions
            self.filter_position.clear()
            self.filter_position.addItem("-- Chức vụ --", None)
            for p in db.query(Position).order_by(Position.name).all():
                self.filter_position.addItem(p.name, p.id)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            self.filter_unit.blockSignals(False)
            self.filter_position.blockSignals(False)
            db.close()

    def apply_role_permissions(self):
        role = (self.current_user.get('role') or '').lower()
        is_admin = role in ('admin', 'hr')
        # Người dùng thường: chỉ xem và xuất trích ngang, xem nâng lương/báo cáo
        self.btn_import.setEnabled(is_admin)
        self.btn_work.setEnabled(is_admin)
        self.btn_export_work.setEnabled(is_admin)
        self.btn_ins_add.setEnabled(is_admin)
        self.btn_ins_export.setEnabled(is_admin)
        self.btn_manage_users.setEnabled(is_admin)
        is_mgr = role in ('admin','hr','unit_manager')
        self.btn_work.setEnabled(is_mgr)
        self.btn_contract_add.setEnabled(is_mgr)
        self.btn_contract_export.setEnabled(is_mgr)

    def drain_notifications(self):
        # Lấy thông báo từ scheduler và hiển thị popup
        try:
            while not NOTIFY_QUEUE.empty():
                title, message = NOTIFY_QUEUE.get_nowait()
                QMessageBox.information(self, title, message)
        except Exception:
            pass

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
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'export_profile', 'Person', person.id, f"file={file_path}")
            except Exception:
                pass
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
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'export_salary_due', 'Salary', None, f"file={xlsx}")
            except Exception:
                pass
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
            # Audit
            try:
                details = f"target={target}; ok={ok_eligible}; reasons={';'.join(reasons)}"
                log_action(db, self.current_user.get('id'), 'check_appointment', 'Appointment', None, details)
            except Exception:
                pass
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
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'add_work_process', 'WorkProcess', wp.id, f"unit={unit};pos={pos}")
            except Exception:
                pass
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
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'export_work_process', 'Person', person.id, f"file={file_path}")
            except Exception:
                pass
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
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'export_quick_report', 'Report', None, f"file={file_path}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def manage_users(self):
        # Chỉ admin/hr mới được
        if (self.current_user.get('role') or '').lower() not in ('admin','hr'):
            QMessageBox.warning(self, "Không có quyền", "Bạn không có quyền quản lý người dùng")
            return
        # Dialog tạo nhanh người dùng
        dlg = QDialog(self)
        dlg.setWindowTitle("Thêm người dùng")
        f = QFormLayout(dlg)
        user_edit = QLineEdit()
        pw_edit = QLineEdit(); pw_edit.setEchoMode(QLineEdit.Password)
        role_box = QComboBox(); role_box.addItems(["user","hr","admin"])
        unit_box = QComboBox(); unit_box.addItem("-- Đơn vị --", None)
        # nạp đơn vị
        db = SessionLocal()
        from .models import Unit, User
        for u in db.query(Unit).order_by(Unit.name).all():
            unit_box.addItem(u.name, u.id)
        f.addRow("Username", user_edit)
        f.addRow("Password", pw_edit)
        f.addRow("Role", role_box)
        f.addRow("Đơn vị", unit_box)
        btn_ok = QPushButton("Tạo")
        btn_cancel = QPushButton("Hủy")
        row = QHBoxLayout(); row.addWidget(btn_ok); row.addWidget(btn_cancel)
        f.addRow(row)

        def do_create():
            username = user_edit.text().strip()
            pw = pw_edit.text()
            role = role_box.currentText()
            unit_id = unit_box.currentData()
            if not username or not pw:
                QMessageBox.warning(dlg, "Thiếu thông tin", "Nhập username và password")
                return
            # Tạo user
            from .security import hash_password
            if db.query(User).filter(User.username == username).first():
                QMessageBox.warning(dlg, "Tồn tại", "Username đã tồn tại")
                return
            u = User(username=username, password_hash=hash_password(pw), role=role, unit_id=unit_id)
            db.add(u); db.commit();
            try:
                log_action(db, self.current_user.get('id'), 'create_user', 'User', u.id, f"role={role};unit_id={unit_id}")
            except Exception:
                pass
            QMessageBox.information(dlg, "Thành công", "Đã tạo người dùng")
            dlg.accept()

        btn_ok.clicked.connect(do_create)
        btn_cancel.clicked.connect(dlg.reject)
        dlg.exec()
        db.close()

    def import_excel(self):
        from PySide6.QtWidgets import QFileDialog
        from .importer import import_persons_from_excel
        db = SessionLocal()
        try:
            xlsx_path, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel", "", "Excel Files (*.xlsx)")
            if not xlsx_path:
                return
            # RBAC: chỉ admin/hr mới được import
            if (self.current_user.get('role') or '').lower() not in ('admin','hr'):
                QMessageBox.warning(self, "Không có quyền", "Bạn không có quyền import")
                return
            result = import_persons_from_excel(db, xlsx_path)
            if not result.get("ok"):
                QMessageBox.critical(self, "Import lỗi", result.get("error", "Lỗi không rõ"))
                return
            # Audit
            try:
                details = f"file={xlsx_path}; created={result['created']}; updated={result['updated']}"
                log_action(db, self.current_user.get('id'), 'import_persons', 'Person', None, details)
            except Exception:
                pass
            QMessageBox.information(self, "Import thành công", f"Tạo mới: {result['created']}, Cập nhật: {result['updated']}")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def _check_unit_permission(self, person) -> bool:
        role = (self.current_user.get('role') or '').lower()
        if role in ('admin','hr'):
            return True
        if role == 'unit_manager' and person and person.unit_id == self.current_user.get('unit_id'):
            return True
        return False

    def add_insurance(self):
        from PySide6.QtWidgets import QInputDialog
        from datetime import date
        from .insurance import add_insurance_event
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            etype, ok = QInputDialog.getText(self, "Loại sự kiện BHXH", "Nhập loại sự kiện:")
            if not ok or not etype:
                return
            if not self._check_unit_permission(person):
                QMessageBox.warning(self, "Không có quyền", "Chỉ quản lý đơn vị mới được thêm cho người thuộc đơn vị mình")
                return
            add_insurance_event(db, person, etype, date.today())
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'add_insurance_event', 'InsuranceEvent', None, f"type={etype}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", "Đã thêm sự kiện BHXH")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def export_insurance(self):
        from datetime import date
        from .insurance import export_insurance_to_excel
        start = date(date.today().year, 1, 1)
        end = date(date.today().year, 12, 31)
        db = SessionLocal()
        try:
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"bhxh_{start.year}.xlsx"
            export_insurance_to_excel(db, start, end, str(file_path))
            # Audit
            try:
                log_action(db, self.current_user.get('id'), 'export_insurance', 'InsuranceEvent', None, f"file={file_path}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def add_contract(self):
        from PySide6.QtWidgets import QInputDialog
        from datetime import date
        from .contracts import add_contract as _add_contract
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            if not self._check_unit_permission(person):
                QMessageBox.warning(self, "Không có quyền", "Chỉ quản lý đơn vị mới được thêm cho người thuộc đơn vị mình")
                return
            ctype, ok = QInputDialog.getText(self, "Loại HĐ", "Nhập loại hợp đồng:")
            if not ok or not ctype:
                return
            c = _add_contract(db, person, ctype, date.today())
            try:
                log_action(db, self.current_user.get('id'), 'add_contract', 'Contract', c.id, f"type={ctype}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", "Đã thêm hợp đồng")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def export_contract(self):
        from .contracts import export_contracts_for_person
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"contracts_{person.code}.xlsx"
            export_contracts_for_person(db, person, str(file_path))
            try:
                log_action(db, self.current_user.get('id'), 'export_contracts', 'Person', person.id, f"file={file_path}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {file_path}")
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
