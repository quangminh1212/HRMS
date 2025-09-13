from pathlib import Path
from datetime import date

from .templates import render_docx_template

TEMPLATES_DIR = Path('templates')


def export_salary_review_cover(context: dict, output_path: str) -> None:
    tpl = TEMPLATES_DIR / 'cong_van_ra_soat_nang_luong.docx'
    render_docx_template(str(tpl), context, output_path)


def export_salary_notification(context: dict, output_path: str) -> None:
    tpl = TEMPLATES_DIR / 'thong_bao_nang_luong.docx'
    render_docx_template(str(tpl), context, output_path)


def export_salary_decision(context: dict, output_path: str) -> None:
    tpl = TEMPLATES_DIR / 'quyet_dinh_nang_luong.docx'
    render_docx_template(str(tpl), context, output_path)


def export_retirement_notification(context: dict, output_path: str) -> None:
    tpl = TEMPLATES_DIR / 'thong_bao_nghi_huu.docx'
    render_docx_template(str(tpl), context, output_path)


def export_retirement_decision(context: dict, output_path: str) -> None:
    tpl = TEMPLATES_DIR / 'quyet_dinh_nghi_huu.docx'
    render_docx_template(str(tpl), context, output_path)