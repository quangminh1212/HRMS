from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QListWidget, QPushButton
from PySide6.QtCore import Qt

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
