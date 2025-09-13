# HRMS (Python-only)

Mục tiêu: Xây dựng hệ thống quản trị nhân sự nội bộ (desktop app) viết THUẦN Python, đáp ứng các nghiệp vụ: tra cứu nhân sự, nâng lương định kỳ/trước hạn, nghỉ hưu, quy hoạch, bổ nhiệm, quá trình công tác, hợp đồng, báo cáo, bảo hiểm, cảnh báo & phân quyền.

Kiến trúc lựa chọn: Desktop app Python (PySide6) + SQLAlchemy + Alembic + SQLite (dev) / PostgreSQL (prod) + xuất Word/Excel (python-docx, openpyxl), scheduler (APScheduler).

Hướng dẫn nhanh
- Tạo venv: python -m venv .venv
- Cài lib: .venv\Scripts\python.exe -m pip install -r requirements.txt
- Chạy lần đầu (sau khi có mã nguồn): .venv\Scripts\python.exe -m hrms

Commit convention
- Tiếng Anh, 1 dòng, dạng imperative, ví dụ: "Initialize project structure"

