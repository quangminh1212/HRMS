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
from .templates import render_docx_template
from .ui_forms import prompt_context
from .person_detail import PersonDetailDialog


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
        self.filter_rank = QComboBox(); self.filter_rank.addItem("-- Ngạch --", None)
        self.filter_step = QComboBox(); self.filter_step.addItem("-- Bậc --", None)
        self.filter_status = QComboBox()
        self.filter_status.addItems(["-- Trạng thái --", "Đang công tác", "Nghỉ thai sản", "Đi học", "Thôi việc"])  # có thể mở rộng
        self.btn_filter_refresh = QPushButton("Lọc")
        self.btn_filter_refresh.clicked.connect(lambda: self.on_search(self.search.text()))
        self.btn_manage_users = QPushButton("Quản lý người dùng")
        self.btn_manage_users.clicked.connect(self.manage_users)
        self.btn_settings = QPushButton("Cấu hình")
        self.btn_settings.clicked.connect(self.open_settings)
        filter_bar.addWidget(self.filter_unit)
        filter_bar.addWidget(self.filter_position)
        filter_bar.addWidget(self.filter_rank)
        filter_bar.addWidget(self.filter_step)
        filter_bar.addWidget(self.filter_status)
        filter_bar.addWidget(self.btn_filter_refresh)
        filter_bar.addWidget(self.btn_manage_users)
        filter_bar.addWidget(self.btn_settings)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Nhập tên cần tìm...")
        self.search.textChanged.connect(self.on_search)
        self.list = QListWidget()
        # Phân trang
        pager_layout = QHBoxLayout()
        self.page_size_box = QComboBox(); self.page_size_box.addItems(["50","100","200"]); self.page_size_box.setCurrentText("50")
        self.btn_prev = QPushButton("◀ Trước")
        self.btn_next = QPushButton("Sau ▶")
        self.page_label = QLabel("Trang 1/1")
        pager_layout.addWidget(QLabel("Kích thước trang"))
        pager_layout.addWidget(self.page_size_box)
        pager_layout.addWidget(self.btn_prev)
        pager_layout.addWidget(self.btn_next)
        pager_layout.addWidget(self.page_label)
        self.current_page = 0
        self.total_count = 0
        self.btn_prev.clicked.connect(self.go_prev_page)
        self.btn_next.clicked.connect(self.go_next_page)
        self.page_size_box.currentTextChanged.connect(lambda _: self.reset_to_first_page())
        btn_layout = QHBoxLayout()
        self.btn_export = QPushButton("Xuất trích ngang")
        self.btn_export.clicked.connect(self.export_selected)
        self.btn_detail = QPushButton("Chi tiết")
        self.btn_detail.clicked.connect(self.open_detail)
        self.btn_due = QPushButton("Nâng lương quý này")
        self.btn_due.clicked.connect(self.show_due)
        self.btn_email_salary_due = QPushButton("Gửi email nâng lương (quý)")
        self.btn_email_salary_due.clicked.connect(self.send_quarter_salary_email)
        self.btn_appointment = QPushButton("Kiểm tra bổ nhiệm")
        self.btn_appointment.clicked.connect(self.check_appointment)
        self.btn_work = QPushButton("Thêm quá trình công tác")
        self.btn_work.clicked.connect(self.add_work_process)
        self.btn_export_work = QPushButton("Xuất quá trình công tác")
        self.btn_export_work.clicked.connect(self.export_work_process)
        self.btn_report = QPushButton("Báo cáo nhanh")
        self.btn_report.clicked.connect(self.quick_report)
        self.btn_email_report = QPushButton("Gửi báo cáo nhanh (email)")
        self.btn_email_report.clicked.connect(self.send_quick_report_email)
        self.btn_letter_salary_cover = QPushButton("CV rà soát nâng lương")
        self.btn_letter_salary_cover.clicked.connect(self.export_salary_cover)
        self.btn_letter_retirement = QPushButton("Văn bản nghỉ hưu")
        self.btn_letter_retirement.clicked.connect(self.export_retirement_letters)
        self.btn_letter_salary_person = QPushButton("Văn bản nâng lương")
        self.btn_letter_salary_person.clicked.connect(self.export_salary_letters)
        self.btn_pdf_toggle = QComboBox(); self.btn_pdf_toggle.addItems(["DOCX","PDF"])  # chế độ xuất
        # Template Excel chooser
        self.excel_template_box = QComboBox(); self.load_excel_templates(); self.load_default_excel_template()
        # Combobox loại export để lưu mặc định theo loại
        self.excel_template_type_box = QComboBox(); self._init_excel_template_types()
        self.btn_save_tpl = QPushButton("Lưu mặc định"); self.btn_save_tpl.clicked.connect(self.save_default_excel_template)
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
        self.btn_salary_export_filtered = QPushButton("Xuất lương (lọc)")
        self.btn_salary_export_filtered.clicked.connect(self.export_salary_histories_filtered)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_detail)
        btn_layout.addWidget(self.btn_due)
        btn_layout.addWidget(self.btn_email_salary_due)
        btn_layout.addWidget(self.btn_appointment)
        btn_layout.addWidget(self.btn_work)
        btn_layout.addWidget(self.btn_export_work)
        btn_layout.addWidget(self.btn_contract_add)
        btn_layout.addWidget(self.btn_contract_export)
        btn_layout.addWidget(self.btn_report)
        btn_layout.addWidget(self.btn_email_report)
        btn_layout.addWidget(self.btn_letter_salary_cover)
        btn_layout.addWidget(self.btn_letter_retirement)
        btn_layout.addWidget(self.btn_letter_salary_person)
        btn_layout.addWidget(self.btn_pdf_toggle)
        btn_layout.addWidget(self.excel_template_box)
        btn_layout.addWidget(self.excel_template_type_box)
        btn_layout.addWidget(self.btn_save_tpl)
        btn_layout.addWidget(self.btn_import)
        btn_layout.addWidget(self.btn_ins_add)
        btn_layout.addWidget(self.btn_ins_export)
        btn_layout.addWidget(self.btn_salary_export_filtered)
        layout.addWidget(QLabel("Tra cứu nhân sự"))
        layout.addWidget(self.search)
        layout.addWidget(self.list)
        layout.addLayout(pager_layout)
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

    def reset_to_first_page(self):
        self.current_page = 0
        self.on_search(self.search.text())

    def go_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.on_search(self.search.text())

    def go_next_page(self):
        page_size = int(self.page_size_box.currentText()) if self.page_size_box.currentText().isdigit() else 50
        max_page = max(0, (self.total_count - 1) // page_size)
        if self.current_page < max_page:
            self.current_page += 1
            self.on_search(self.search.text())

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
            # Lọc theo ngạch/bậc dựa trên lịch sử lương mới nhất (tối ưu hóa ở DB)
            rank_id = self.filter_rank.currentData()
            step_val = self.filter_step.currentData()
            if rank_id or step_val:
                from .models import SalaryHistory
                from sqlalchemy import func
                sub = db.query(
                    SalaryHistory.person_id.label('pid'),
                    func.max(SalaryHistory.effective_date).label('max_date')
                ).group_by(SalaryHistory.person_id).subquery()
                latest = db.query(
                    SalaryHistory.person_id.label('pid'),
                    SalaryHistory.rank_id.label('rank_id'),
                    SalaryHistory.step.label('step')
                ).join(
                    sub,
                    (SalaryHistory.person_id == sub.c.pid) & (SalaryHistory.effective_date == sub.c.max_date)
                ).subquery()
                q = q.join(latest, Person.id == latest.c.pid)
                if rank_id:
                    q = q.filter(latest.c.rank_id == rank_id)
                if step_val:
                    q = q.filter(latest.c.step == step_val)
            st = self.filter_status.currentText()
            if st and not st.startswith("--"):
                q = q.filter(Person.status.ilike(f"%{st}%"))
            # Đếm tổng số kết quả trước khi phân trang
            self.total_count = q.count()
            page_size = int(self.page_size_box.currentText()) if self.page_size_box.currentText().isdigit() else 50
            offset = self.current_page * page_size
            # Nếu offset vượt quá tổng, đưa về trang cuối
            if offset >= max(0, self.total_count):
                self.current_page = max(0, (self.total_count - 1) // page_size) if self.total_count > 0 else 0
                offset = self.current_page * page_size
            people = q.order_by(Person.full_name).limit(page_size).offset(offset).all()
            # Cập nhật danh sách
            self.list.clear()
            for p in people:
                self.list.addItem(f"{p.full_name} - {p.code}")
            # Cập nhật pager label và nút
            total_pages = max(1, (self.total_count - 1) // page_size + 1) if self.total_count > 0 else 1
            self.page_label.setText(f"Trang {self.current_page+1}/{total_pages} ({self.total_count} kết quả)")
            self.btn_prev.setEnabled(self.current_page > 0)
            self.btn_next.setEnabled(self.current_page < total_pages - 1)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def get_selected_excel_template(self) -> str | None:
        # Trả về tên file template (không gồm đường dẫn) hoặc None
        data = self.excel_template_box.currentData()
        return data if isinstance(data, str) or data is None else None

    def _init_excel_template_types(self):
        # Khởi tạo danh sách loại export
        self.excel_template_type_box.clear()
        self.excel_template_type_box.addItem("(Chung)", "GLOBAL")
        self.excel_template_type_box.addItem("Nâng lương đến hạn", "salary_due")
        self.excel_template_type_box.addItem("Lịch sử lương (cá nhân)", "salary_history")
        self.excel_template_type_box.addItem("Lịch sử lương (lọc)", "salary_histories")
        self.excel_template_type_box.addItem("Hợp đồng", "contracts")
        self.excel_template_type_box.addItem("BHXH", "bhxh")

    def get_template_for(self, export_type: str) -> str | None:
        # Ưu tiên mặc định theo loại -> mặc định chung -> lựa chọn hiện tại
        try:
            from .settings_service import get_setting
            username = (self.current_user.get('username') or '').strip()
            if username:
                key_type = f"DEFAULT_XLSX_TEMPLATE:{username}:{export_type}"
                val = get_setting(key_type, None)
                if val:
                    return val
                key_global = f"DEFAULT_XLSX_TEMPLATE:{username}:GLOBAL"
                val2 = get_setting(key_global, None)
                if val2:
                    return val2
        except Exception:
            pass
        return self.get_selected_excel_template()

    def load_excel_templates(self):
        # Nạp danh sách template Excel từ templates/xlsx
        try:
            self.excel_template_box.clear()
            self.excel_template_box.addItem("(Mặc định)", None)
            tpl_dir = Path('templates') / 'xlsx'
            if tpl_dir.exists():
                for p in sorted([x for x in tpl_dir.iterdir() if x.suffix.lower() == '.xlsx']):
                    self.excel_template_box.addItem(p.name, p.name)
        except Exception:
            # Bỏ qua lỗi nạp template
            self.excel_template_box.clear()
            self.excel_template_box.addItem("(Mặc định)", None)

    def load_default_excel_template(self) -> None:
        # Nạp template mặc định (chung) đã lưu theo user hiện tại
        try:
            from .settings_service import get_setting
            username = (self.current_user.get('username') or '').strip()
            if not username:
                return
            key = f"DEFAULT_XLSX_TEMPLATE:{username}:GLOBAL"
            val = get_setting(key, None)
            if not val:
                return
            # Tìm item có data == val
            for i in range(self.excel_template_box.count()):
                if self.excel_template_box.itemData(i) == val:
                    self.excel_template_box.setCurrentIndex(i)
                    break
        except Exception:
            pass

    def save_default_excel_template(self) -> None:
        # Lưu template hiện chọn làm mặc định cho user (theo loại export hoặc GLOBAL)
        try:
            from .settings_service import set_setting
            tpl = self.get_selected_excel_template()
            username = (self.current_user.get('username') or '').strip()
            if not username:
                QMessageBox.warning(self, "Lỗi", "Không xác định được người dùng")
                return
            etype = self.excel_template_type_box.currentData() or 'GLOBAL'
            key = f"DEFAULT_XLSX_TEMPLATE:{username}:{etype}"
            set_setting(key, tpl or '')
            QMessageBox.information(self, "Đã lưu", "Đã lưu template Excel mặc định cho loại export")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

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
            # Ranks
            from .models import SalaryRank, SalaryStep
            self.filter_rank.clear(); self.filter_rank.addItem("-- Ngạch --", None)
            for r in db.query(SalaryRank).order_by(SalaryRank.code).all():
                self.filter_rank.addItem(f"{r.code}-{r.name}", r.id)
            self.filter_step.clear(); self.filter_step.addItem("-- Bậc --", None)
            for s in range(1, 15):
                self.filter_step.addItem(str(s), s)
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
        self.btn_detail.setEnabled(True)
        self.btn_export_work.setEnabled(is_admin)
        self.btn_ins_add.setEnabled(is_admin)
        self.btn_ins_export.setEnabled(is_admin)
        self.btn_manage_users.setEnabled(is_admin)
        self.btn_settings.setEnabled(is_admin)
        # Gửi email nâng lương (quý) chỉ cho admin/hr
        self.btn_email_salary_due.setEnabled(is_admin)
        # Nút email nghỉ hưu: chỉ admin/hr
        if not hasattr(self, 'btn_email_retirement'):
            self.btn_email_retirement = QPushButton("Gửi email nghỉ hưu (6/3 tháng)")
            self.btn_email_retirement.clicked.connect(self.send_retirement_email)
            # chèn vào layout nút, đặt sau email báo cáo nhanh
            # chú ý: layout đã tạo sẵn, thêm vào cuối để tránh phá vỡ UI
            self.layout().itemAt(3).addWidget(self.btn_email_retirement) if hasattr(self, 'layout') else None
        self.btn_email_retirement.setEnabled(is_admin)
        is_mgr = role in ('admin','hr','unit_manager')
        self.btn_work.setEnabled(is_mgr)
        self.btn_contract_add.setEnabled(is_mgr)
        self.btn_contract_export.setEnabled(is_mgr)
        # Xuất lịch sử lương theo danh sách lọc: chỉ admin/hr và quản lý đơn vị (sẽ lọc theo đơn vị)
        self.btn_salary_export_filtered.setEnabled(is_mgr)
        # Gửi báo cáo nhanh (email): chỉ admin/hr
        self.btn_email_report.setEnabled(role in ('admin','hr'))

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
            # Nếu có template, render template; nếu không, fallback bảng mặc định
            tpl = Path("templates") / "trich_ngang_template.docx"
            context = {
                "full_name": person.full_name or "",
                "code": person.code or "",
                "dob": person.dob.isoformat() if person.dob else "",
                "gender": person.gender or "",
                "ethnicity": person.ethnicity or "",
                "religion": person.religion or "",
                "hometown": person.hometown or "",
                "position": person.position.name if person.position else "",
                "unit": person.unit.name if person.unit else "",
                "party_joined_date": person.party_joined_date.isoformat() if person.party_joined_date else "",
                "llct_level": person.llct_level or "",
                "professional_level": person.professional_level or "",
                "status": person.status or "",
                "phone": person.phone or "",
                "email": person.email or "",
            }
            if tpl.exists():
                render_docx_template(str(tpl), context, str(file_path))
            else:
                doc = Document()
                doc.add_heading("Trích ngang nhân sự", level=1)
                rows = [
                    ("Họ và tên", context["full_name"]),
                    ("Mã", context["code"]),
                    ("Ngày sinh", context["dob"]),
                    ("Giới tính", context["gender"]),
                    ("Dân tộc", context["ethnicity"]),
                    ("Tôn giáo", context["religion"]),
                    ("Quê quán", context["hometown"]),
                    ("Chức danh", context["position"]),
                    ("Đơn vị", context["unit"]),
                    ("Ngày vào Đảng", context["party_joined_date"]),
                    ("LLCT", context["llct_level"]),
                    ("Trình độ chuyên môn", context["professional_level"]),
                    ("Tình trạng công tác", context["status"]),
                    ("Điện thoại", context["phone"]),
                    ("Email", context["email"]),
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
            export_due_to_excel(items, str(xlsx), template_name=self.get_template_for('salary_due'), username=self.current_user.get('username'))
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

    def open_detail(self):
        # Mở dialog chi tiết cho nhân sự đang chọn
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            dlg = PersonDetailDialog(person.id, self)
            dlg.exec()
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

    def export_salary_cover(self):
        # Xuất công văn rà soát nâng lương theo quý hiện tại
        from datetime import date
        from .docx_exports import export_salary_review_cover
        q = (date.today().month - 1)//3 + 1
        defaults = {
            'org_name': 'Cơ quan ABC',
            'quarter': str(q),
            'year': str(date.today().year),
            'date': date.today().isoformat(),
        }
        # Hỏi người dùng thông tin văn bản
        form_fields = [
            {'name': 'org_name', 'label': 'Đơn vị/Cơ quan', 'type': 'text', 'default': defaults['org_name']},
            {'name': 'quarter', 'label': 'Quý', 'type': 'select', 'default': defaults['quarter'], 'options': ['1','2','3','4']},
            {'name': 'year', 'label': 'Năm', 'type': 'text', 'default': defaults['year']},
            {'name': 'date', 'label': 'Ngày văn bản', 'type': 'date', 'default': defaults['date']},
        ]
        ctx = prompt_context(self, 'Thông tin công văn rà soát', form_fields)
        if not ctx:
            QMessageBox.information(self, "Đã hủy", "Đã hủy xuất công văn")
            return
        Path('exports').mkdir(exist_ok=True)
        out = Path('exports')/f"cong_van_ra_soat_quy_{ctx['year']}_Q{ctx['quarter']}.docx"
        try:
            export_salary_review_cover(ctx, str(out))
            # Optional PDF
            if self.btn_pdf_toggle.currentText() == 'PDF':
                from .templates import try_export_docx_to_pdf
                pdf_path = str(out).replace('.docx','.pdf')
                if try_export_docx_to_pdf(str(out), pdf_path):
                    out = Path(pdf_path)
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'export_salary_cover', 'Letter', None, f"file={out}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def export_retirement_letters(self):
        # Xuất văn bản nghỉ hưu cho nhân sự đã chọn (TB và QĐ)
        from datetime import date
        from .docx_exports import export_retirement_notification, export_retirement_decision
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            default_retire = (person.dob.replace(year=person.dob.year + (60 if (person.gender or 'Nam').lower().startswith('n') else 55)).isoformat() if person.dob else '')
            defaults = {
                'full_name': person.full_name or '',
                'code': person.code or '',
                'retirement_date': default_retire,
                'date': date.today().isoformat(),
            }
            fields = [
                {'name': 'full_name', 'label': 'Họ và tên', 'type': 'text', 'default': defaults['full_name']},
                {'name': 'code', 'label': 'Mã nhân sự', 'type': 'text', 'default': defaults['code']},
                {'name': 'retirement_date', 'label': 'Ngày nghỉ hưu', 'type': 'date', 'default': defaults['retirement_date']},
                {'name': 'date', 'label': 'Ngày văn bản', 'type': 'date', 'default': defaults['date']},
            ]
            ctx = prompt_context(self, 'Thông tin văn bản nghỉ hưu', fields)
            if not ctx:
                QMessageBox.information(self, "Đã hủy", "Đã hủy xuất văn bản")
                return
            Path('exports').mkdir(exist_ok=True)
            out1 = Path('exports')/f"thong_bao_nghi_huu_{person.code}.docx"
            out2 = Path('exports')/f"quyet_dinh_nghi_huu_{person.code}.docx"
            export_retirement_notification(ctx, str(out1))
            export_retirement_decision(ctx, str(out2))
            if self.btn_pdf_toggle.currentText() == 'PDF':
                from .templates import try_export_docx_to_pdf
                p1 = str(out1).replace('.docx','.pdf')
                p2 = str(out2).replace('.docx','.pdf')
                if try_export_docx_to_pdf(str(out1), p1):
                    out1 = Path(p1)
                if try_export_docx_to_pdf(str(out2), p2):
                    out2 = Path(p2)
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'export_retirement_letters', 'Letter', person.id, f"files={out1},{out2}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {out1}\n{out2}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def export_salary_letters(self):
        # Xuất Thông báo & Quyết định nâng lương cho nhân sự đã chọn nếu có đề xuất
        from datetime import date
        from .salary import compute_next_for_person
        from .docx_exports import export_salary_notification, export_salary_decision
        db, person = self.current_person()
        try:
            if not person:
                QMessageBox.information(self, "Chưa chọn", "Chọn một nhân sự trước")
                return
            info = compute_next_for_person(db, person, date.today())
            if not info:
                QMessageBox.information(self, "Không có đề xuất", "Nhân sự chưa đến hạn nâng lương")
                return
            effective = info.get('due_date')
            step = info.get('next_step') if info.get('type') == 'step' else ''
            coef = info.get('next_coef') if info.get('type') == 'step' else f"{info.get('allowance_percent','')}%"
            defaults = {
                'full_name': person.full_name or '',
                'code': person.code or '',
                'unit': person.unit.name if person.unit else '',
                'effective_date': effective.isoformat() if effective else date.today().isoformat(),
                'step': str(step) if step != '' else '',
                'coefficient': str(coef) if coef is not None else '',
            }
            fields = [
                {'name': 'full_name', 'label': 'Họ và tên', 'type': 'text', 'default': defaults['full_name']},
                {'name': 'code', 'label': 'Mã nhân sự', 'type': 'text', 'default': defaults['code']},
                {'name': 'unit', 'label': 'Đơn vị', 'type': 'text', 'default': defaults['unit']},
                {'name': 'effective_date', 'label': 'Ngày hiệu lực', 'type': 'date', 'default': defaults['effective_date']},
                {'name': 'step', 'label': 'Bậc', 'type': 'text', 'default': defaults['step']},
                {'name': 'coefficient', 'label': 'Hệ số/% vượt khung', 'type': 'text', 'default': defaults['coefficient']},
            ]
            ctx = prompt_context(self, 'Thông tin văn bản nâng lương', fields)
            if not ctx:
                QMessageBox.information(self, "Đã hủy", "Đã hủy xuất văn bản")
                return
            Path('exports').mkdir(exist_ok=True)
            out1 = Path('exports')/f"thong_bao_nang_luong_{person.code}.docx"
            out2 = Path('exports')/f"quyet_dinh_nang_luong_{person.code}.docx"
            export_salary_notification(ctx, str(out1))
            export_salary_decision(ctx, str(out2))
            if self.btn_pdf_toggle.currentText() == 'PDF':
                from .templates import try_export_docx_to_pdf
                p1 = str(out1).replace('.docx','.pdf')
                p2 = str(out2).replace('.docx','.pdf')
                if try_export_docx_to_pdf(str(out1), p1):
                    out1 = Path(p1)
                if try_export_docx_to_pdf(str(out2), p2):
                    out2 = Path(p2)
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'export_salary_letters', 'Letter', person.id, f"files={out1},{out2}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {out1}\n{out2}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            if db:
                db.close()

    def send_quarter_salary_email(self):
        # Gửi email danh sách nâng lương quý hiện tại kèm file Excel
        role = (self.current_user.get('role') or '').lower()
        if role not in ('admin','hr'):
            QMessageBox.warning(self, "Không có quyền", "Chỉ admin/HR mới gửi email")
            return
        from datetime import date
        from pathlib import Path
        from .salary import list_due_in_window, export_due_to_excel
        from .mailer import send_email_with_attachment
        start, end = quarter_window(date.today())
        db = SessionLocal()
        try:
            items = list_due_in_window(db, start, end)
            if not items:
                QMessageBox.information(self, "Kết quả", "Không có nhân sự đến hạn trong quý này")
                return
            Path("exports").mkdir(exist_ok=True)
            q = ((end.month - 1)//3) + 1
            out = Path("exports") / f"nang_luong_quy_{end.year}_Q{q}.xlsx"
            export_due_to_excel(items, str(out), template_name=self.get_template_for('salary_due'), username=self.current_user.get('username'))
            subject = f"[HRMS] Danh sách đến hạn nâng lương - Q{q}/{end.year}"
            body = f"Có {len(items)} nhân sự đến hạn trong quý này. Tệp đính kèm: {out.name}"
            ok = send_email_with_attachment(subject, body, [str(out)])
            # Audit
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'email_salary_due', 'Salary', None, f"file={out};sent={ok};count={len(items)}")
            except Exception:
                pass
            if ok:
                QMessageBox.information(self, "Thành công", f"Đã gửi email kèm tệp: {out}")
            else:
                QMessageBox.warning(self, "Chưa gửi", "Không gửi được email. Kiểm tra cấu hình SMTP/ALERT_EMAILS")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def send_retirement_email(self):
        # Gửi email danh sách nghỉ hưu (6/3 tháng) kèm Excel 2 sheet
        role = (self.current_user.get('role') or '').lower()
        if role not in ('admin','hr'):
            QMessageBox.warning(self, "Không có quyền", "Chỉ admin/HR mới gửi")
            return
        from datetime import date
        from pathlib import Path
        from .reporting import export_retirement_alerts_to_excel
        from .retirement import calculate_retirement_date
        from .mailer import send_email_with_attachment
        db = SessionLocal()
        try:
            today = date.today()
            six = date(today.year + (today.month + 6 - 1) // 12, ((today.month + 6 - 1) % 12) + 1, today.day)
            three = date(today.year + (today.month + 3 - 1) // 12, ((today.month + 3 - 1) % 12) + 1, today.day)
            persons = db.query(Person).all()
            list6 = [p for p in persons if calculate_retirement_date(p) == six]
            list3 = [p for p in persons if calculate_retirement_date(p) == three]
            if not list6 and not list3:
                QMessageBox.information(self, "Kết quả", "Chưa có người trùng mốc 6/3 tháng kể từ hôm nay")
                return
            Path('exports').mkdir(exist_ok=True)
            out = Path('exports')/f"nghi_huu_thong_bao_{today.isoformat()}.xlsx"
            export_retirement_alerts_to_excel(db, list6, list3, str(out))
            subject = f"[HRMS] Danh sách nghỉ hưu (6/3 tháng) {today.isoformat()}"
            body = "Đính kèm danh sách nghỉ hưu dự kiến theo mốc 6 và 3 tháng."
            ok = send_email_with_attachment(subject, body, [str(out)])
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'email_retirement_alerts', 'Retirement', None, f"file={out};sent={ok};six={len(list6)};three={len(list3)}")
            except Exception:
                pass
            if ok:
                QMessageBox.information(self, "Thành công", f"Đã gửi email: {out}")
            else:
                QMessageBox.warning(self, "Chưa gửi", "Không gửi được email. Kiểm tra cấu hình SMTP/ALERT_EMAILS")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
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
            db.close()

    def send_quick_report_email(self):
        # Gửi báo cáo nhanh qua email (đính kèm file Excel)
        role = (self.current_user.get('role') or '').lower()
        if role not in ('admin','hr'):
            QMessageBox.warning(self, "Không có quyền", "Chỉ admin/HR mới gửi")
            return
        from datetime import date
        from pathlib import Path
        from .reporting import compute_annual_summary, compute_demographics, export_report_to_excel
        from .mailer import send_email_with_attachment
        year = date.today().year
        db = SessionLocal()
        try:
            summary = compute_annual_summary(db, year)
            demo = compute_demographics(db, date.today())
            Path("exports").mkdir(exist_ok=True)
            file_path = Path("exports") / f"bao_cao_nhanh_{year}.xlsx"
            export_report_to_excel(summary, demo, str(file_path))
            subject = f"[HRMS] Báo cáo nhanh {year}"
            body = "Đính kèm báo cáo nhanh tổng hợp và cơ cấu nhân sự."
            ok = send_email_with_attachment(subject, body, [str(file_path)])
            try:
                log_action(SessionLocal(), self.current_user.get('id'), 'email_quick_report', 'Report', None, f"file={file_path};sent={ok}")
            except Exception:
                pass
            if ok:
                QMessageBox.information(self, "Thành công", f"Đã gửi email: {file_path}")
            else:
                QMessageBox.warning(self, "Chưa gửi", "Không gửi được email. Kiểm tra cấu hình SMTP/ALERT_EMAILS")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def export_salary_histories_filtered(self):
        # Xuất lịch sử lương cho danh sách đang hiển thị (lọc)
        from datetime import datetime
        from .salary import export_salary_histories_for_people
        db = SessionLocal()
        try:
            role = (self.current_user.get('role') or '').lower()
            # Lấy danh sách code từ list widget (đang hiển thị theo bộ lọc)
            codes = []
            for i in range(self.list.count()):
                item = self.list.item(i)
                if not item:
                    continue
                code = item.text().split(" - ")[-1]
                codes.append(code)
            if not codes:
                QMessageBox.information(self, "Không có dữ liệu", "Không có nhân sự trong danh sách để xuất")
                return
            from .models import Person
            q = db.query(Person).filter(Person.code.in_(codes))
            # RBAC: nếu quản lý đơn vị, chỉ cho phép xuất người cùng đơn vị
            if role == 'unit_manager':
                only_unit_id = self.current_user.get('unit_id')
                if only_unit_id:
                    q = q.filter(Person.unit_id == only_unit_id)
            people = q.order_by(Person.full_name).all()
            if not people:
                QMessageBox.information(self, "Không có dữ liệu", "Không có nhân sự phù hợp quyền để xuất")
                return
            Path("exports").mkdir(exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            out = Path("exports")/f"salary_histories_{ts}.xlsx"
            export_salary_histories_for_people(db, people, str(out), template_name=self.get_template_for('salary_histories'), username=self.current_user.get('username'))
            try:
                log_action(db, self.current_user.get('id'), 'export_salary_histories', 'Person', None, f"count={len(people)};file={out}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()

    def open_settings(self):
        # Trang cấu hình tối giản: SMTP và alert emails
        role = (self.current_user.get('role') or '').lower()
        if role not in ('admin','hr'):
            QMessageBox.warning(self, "Không có quyền", "Chỉ admin/HR mới truy cập cấu hình")
            return
        from PySide6.QtWidgets import QDialog, QFormLayout
        from .settings_service import get_setting, set_setting
        dlg = QDialog(self); dlg.setWindowTitle("Cấu hình hệ thống")
        f = QFormLayout(dlg)
        smtp_host = QLineEdit(get_setting('SMTP_HOST','') or '')
        smtp_port = QLineEdit(get_setting('SMTP_PORT','587') or '587')
        smtp_user = QLineEdit(get_setting('SMTP_USER','') or '')
        smtp_pass = QLineEdit(get_setting('SMTP_PASSWORD','') or ''); smtp_pass.setEchoMode(QLineEdit.Password)
        alert_emails = QLineEdit(get_setting('ALERT_EMAILS','') or '')
        org_name = QLineEdit(get_setting('ORG_NAME','') or '')
        date_fmt = QLineEdit(get_setting('XLSX_DATE_FORMAT','DD/MM/YYYY') or 'DD/MM/YYYY')
        coef_fmt = QLineEdit(get_setting('XLSX_NUMBER_FORMAT_COEF','0.00') or '0.00')
        freeze_global = QLineEdit(get_setting('XLSX_FREEZE_COL:GLOBAL','A') or 'A')
        freeze_bhxh = QLineEdit(get_setting('XLSX_FREEZE_COL:bhxh','') or '')
        freeze_contracts = QLineEdit(get_setting('XLSX_FREEZE_COL:contracts','') or '')
        freeze_salary_due = QLineEdit(get_setting('XLSX_FREEZE_COL:salary_due','') or '')
        freeze_salary_history = QLineEdit(get_setting('XLSX_FREEZE_COL:salary_history','') or '')
        freeze_salary_histories = QLineEdit(get_setting('XLSX_FREEZE_COL:salary_histories','') or '')
        f.addRow("SMTP_HOST", smtp_host)
        f.addRow("SMTP_PORT", smtp_port)
        f.addRow("SMTP_USER", smtp_user)
        f.addRow("SMTP_PASSWORD", smtp_pass)
        f.addRow("ALERT_EMAILS", alert_emails)
        f.addRow("ORG_NAME", org_name)
        f.addRow("XLSX_DATE_FORMAT", date_fmt)
        f.addRow("XLSX_NUMBER_FORMAT_COEF", coef_fmt)
        f.addRow("XLSX_FREEZE_COL:GLOBAL", freeze_global)
        f.addRow("XLSX_FREEZE_COL:bhxh", freeze_bhxh)
        f.addRow("XLSX_FREEZE_COL:contracts", freeze_contracts)
        f.addRow("XLSX_FREEZE_COL:salary_due", freeze_salary_due)
        f.addRow("XLSX_FREEZE_COL:salary_history", freeze_salary_history)
        f.addRow("XLSX_FREEZE_COL:salary_histories", freeze_salary_histories)
        btn_ok = QPushButton("Lưu"); btn_cancel = QPushButton("Đóng")
        row = QHBoxLayout(); row.addWidget(btn_ok); row.addWidget(btn_cancel)
        f.addRow(row)
        def save():
            set_setting('SMTP_HOST', smtp_host.text())
            set_setting('SMTP_PORT', smtp_port.text())
            set_setting('SMTP_USER', smtp_user.text())
            set_setting('SMTP_PASSWORD', smtp_pass.text())
            set_setting('ALERT_EMAILS', alert_emails.text())
            set_setting('ORG_NAME', org_name.text())
            set_setting('XLSX_DATE_FORMAT', (date_fmt.text() or 'DD/MM/YYYY'))
            set_setting('XLSX_NUMBER_FORMAT_COEF', (coef_fmt.text() or '0.00'))
            set_setting('XLSX_FREEZE_COL:GLOBAL', (freeze_global.text() or 'A').upper())
            if freeze_bhxh.text(): set_setting('XLSX_FREEZE_COL:bhxh', freeze_bhxh.text().upper())
            if freeze_contracts.text(): set_setting('XLSX_FREEZE_COL:contracts', freeze_contracts.text().upper())
            if freeze_salary_due.text(): set_setting('XLSX_FREEZE_COL:salary_due', freeze_salary_due.text().upper())
            if freeze_salary_history.text(): set_setting('XLSX_FREEZE_COL:salary_history', freeze_salary_history.text().upper())
            if freeze_salary_histories.text(): set_setting('XLSX_FREEZE_COL:salary_histories', freeze_salary_histories.text().upper())
            QMessageBox.information(dlg, "Đã lưu", "Lưu cấu hình thành công")
        btn_ok.clicked.connect(save)
        btn_cancel.clicked.connect(dlg.reject)
        dlg.exec()

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
            export_insurance_to_excel(db, start, end, str(file_path), template_name=self.get_template_for('bhxh'), username=self.current_user.get('username'))
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
            export_contracts_for_person(db, person, str(file_path), template_name=self.get_template_for('contracts'), username=self.current_user.get('username'))
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
