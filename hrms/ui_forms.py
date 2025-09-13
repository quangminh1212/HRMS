from typing import List, Dict, Any, Optional

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox, QPushButton, QHBoxLayout
from PySide6.QtCore import QDate

# fields: List[{
#   name: str, label: str, type: 'text'|'date'|'select', default: str|date, options: List[str] (for select)
# }]

def prompt_context(parent, title: str, fields: List[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    form = QFormLayout(dlg)

    widgets: Dict[str, Any] = {}

    for f in fields:
        ftype = f.get('type', 'text')
        name = f['name']
        label = f.get('label', name)
        if ftype == 'date':
            w = QDateEdit()
            w.setCalendarPopup(True)
            d = f.get('default')
            if isinstance(d, str) and d:
                # expect YYYY-MM-DD
                try:
                    y, m, da = [int(x) for x in d.split('-')]
                    w.setDate(QDate(y, m, da))
                except Exception:
                    w.setDate(QDate.currentDate())
            else:
                w.setDate(QDate.currentDate())
        elif ftype == 'select':
            w = QComboBox()
            opts = f.get('options') or []
            for o in opts:
                w.addItem(str(o))
            default = str(f.get('default', ''))
            if default and default in [str(o) for o in opts]:
                w.setCurrentText(default)
        else:
            w = QLineEdit()
            if f.get('default') is not None:
                w.setText(str(f.get('default')))
        widgets[name] = w
        form.addRow(label, w)

    btn_ok = QPushButton("Xuất")
    btn_cancel = QPushButton("Hủy")
    row = QHBoxLayout(); row.addWidget(btn_ok); row.addWidget(btn_cancel)
    form.addRow(row)

    def on_ok():
        ctx: Dict[str, str] = {}
        for f in fields:
            name = f['name']
            ftype = f.get('type', 'text')
            w = widgets[name]
            if ftype == 'date':
                d: QDate = w.date()
                ctx[name] = f"{d.year():04d}-{d.month():02d}-{d.day():02d}"
            elif ftype == 'select':
                ctx[name] = w.currentText()
            else:
                ctx[name] = w.text()
        dlg.done(1)
        dlg.ctx = ctx  # type: ignore

    def on_cancel():
        dlg.done(0)

    btn_ok.clicked.connect(on_ok)
    btn_cancel.clicked.connect(on_cancel)

    result = dlg.exec()
    if result == 1:
        return getattr(dlg, 'ctx', None)
    return None
