from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QListWidget, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from pathlib import Path

from .db import SessionLocal
from .models import Person, SalaryHistory, WorkProcess, Planning, Contract, InsuranceEvent, SalaryRank


class PersonDetailDialog(QDialog):
    def __init__(self, person_id: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chi tiết nhân sự")
        self.resize(700, 500)
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.btn_export_salary = QPushButton("Xuất lương (Excel)")
        self.btn_export_salary.clicked.connect(self.export_salary_history)
        layout.addWidget(self.btn_export_salary, alignment=Qt.AlignRight)

        self.btn_close = QPushButton("Đóng")
        self.btn_close.clicked.connect(self.accept)
        layout.addWidget(self.btn_close, alignment=Qt.AlignRight)

        self.person_id = person_id
        self._build()

    def _build(self):
        db = SessionLocal()
        try:
            p = db.get(Person, self.person_id)
            # Overview
            ov = QListWidget()
            ov.addItem(f"Họ tên: {p.full_name}")
            ov.addItem(f"Mã: {p.code}")
            ov.addItem(f"Đơn vị: {p.unit.name if p.unit else ''}")
            ov.addItem(f"Chức vụ: {p.position.name if p.position else ''}")
            ov.addItem(f"Ngày sinh: {p.dob or ''}")
            ov.addItem(f"Giới tính: {p.gender or ''}")
            ov.addItem(f"Tình trạng: {p.status or ''}")
            self.tabs.addTab(ov, "Trích ngang")

            # Salary
            sal = QListWidget()
            hists = db.query(SalaryHistory).filter_by(person_id=p.id).order_by(SalaryHistory.effective_date.desc()).all()
            for h in hists:
                rank = db.get(SalaryRank, h.rank_id)
                sal.addItem(f"{h.effective_date} - {rank.code if rank else ''}/{h.step} - HS {h.coefficient}")
            self.tabs.addTab(sal, "Lương")

            # Work processes
            wp_list = QListWidget()
            wps = db.query(WorkProcess).filter_by(person_id=p.id).order_by(WorkProcess.start_date.desc()).all()
            for w in wps:
                wp_list.addItem(f"{w.start_date} -> {w.end_date or ''}: {w.unit} - {w.position}")
            self.tabs.addTab(wp_list, "Quá trình")

            # Planning
            pl_list = QListWidget()
            pls = db.query(Planning).filter_by(person_id=p.id).order_by(Planning.start_year.desc()).all()
            for pl in pls:
                pl_list.addItem(f"{pl.start_year}-{pl.end_year}: {pl.job_position}")
            self.tabs.addTab(pl_list, "Quy hoạch")

            # Contracts
            ct_list = QListWidget()
            cts = db.query(Contract).filter_by(person_id=p.id).order_by(Contract.start_date.desc()).all()
            for c in cts:
                ct_list.addItem(f"{c.start_date}->{c.end_date or ''}: {c.contract_type} ({c.note or ''})")
            self.tabs.addTab(ct_list, "Hợp đồng")

            # Insurance
            ins_list = QListWidget()
            ins = db.query(InsuranceEvent).filter_by(person_id=p.id).order_by(InsuranceEvent.event_date.desc()).all()
            for i in ins:
                ins_list.addItem(f"{i.event_date}: {i.event_type} ({i.details or ''})")
            self.tabs.addTab(ins_list, "BHXH")
        finally:
            db.close()

    def export_salary_history(self):
        from .salary import export_salary_history_for_person
        from .audit import log_action
        db = SessionLocal()
        try:
            p = db.get(Person, self.person_id)
            if not p:
                QMessageBox.critical(self, "Lỗi", "Không tìm thấy nhân sự")
                return
            # RBAC: chỉ admin/hr và quản lý đơn vị (chỉ người trong đơn vị)
            current_user = getattr(self.parent(), 'current_user', {}) if self.parent() else {}
            role = (current_user.get('role') or '').lower() if isinstance(current_user, dict) else ''
            if role not in ('admin','hr','unit_manager'):
                QMessageBox.warning(self, "Không có quyền", "Bạn không có quyền xuất lịch sử lương")
                return
            if role == 'unit_manager' and current_user.get('unit_id') and p.unit_id and p.unit_id != current_user.get('unit_id'):
                QMessageBox.warning(self, "Không có quyền", "Chỉ quản lý đơn vị được xuất nhân sự thuộc đơn vị mình")
                return

            # Lấy template Excel từ màn hình chính nếu có
            template_name = None
            try:
                parent = self.parent()
                if parent and hasattr(parent, 'get_selected_excel_template'):
                    template_name = parent.get_selected_excel_template()
            except Exception:
                template_name = None

            Path("exports").mkdir(exist_ok=True)
            out = Path("exports") / f"salary_history_{p.code}.xlsx"
            # Dùng template theo loại (fallback template_name nếu đã lấy trực tiếp)
            try:
                parent = self.parent()
                if parent and hasattr(parent, 'get_template_for'):
                    template_name = parent.get_template_for('salary_history')
            except Exception:
                pass
            export_salary_history_for_person(db, p, str(out), template_name=template_name, username=(current_user.get('username') if isinstance(current_user, dict) else None))
            # Audit
            try:
                uid = current_user.get('id') if isinstance(current_user, dict) else None
                log_action(db, uid, 'export_salary_history', 'Person', p.id, f"file={out}")
            except Exception:
                pass
            QMessageBox.information(self, "Thành công", f"Đã xuất: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))
        finally:
            db.close()
