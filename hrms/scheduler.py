from datetime import datetime, time, date
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

from .db import SessionLocal
from .models import Person
from .salary import list_due_in_window
from .retirement import calculate_retirement_date


def notify(title: str, message: str):
    # Tối giản: in ra console; có thể nâng cấp thành popup trong UI nếu cần
    print(f"[NOTICE] {title}: {message}")


def schedule_jobs():
    sched = BackgroundScheduler()

    # Cảnh báo nâng lương vào ngày 15 của 2/5/8/11
    def run_salary_alert():
        today = date.today()
        if today.day != 15 or today.month not in (2, 5, 8, 11):
            return
        from .app import quarter_window
        start, end = quarter_window(today)
        db = SessionLocal()
        try:
            items = list_due_in_window(db, start, end)
            if items:
                notify("Nâng lương định kỳ", f"Có {len(items)} nhân sự đến hạn trong quý này")
        finally:
            db.close()

    # Cảnh báo nghỉ hưu: 6 tháng và 3 tháng
    def run_retirement_alert():
        db = SessionLocal()
        try:
            today = date.today()
            six = date(today.year + (today.month + 6 - 1) // 12, ((today.month + 6 - 1) % 12) + 1, today.day)
            three = date(today.year + (today.month + 3 - 1) // 12, ((today.month + 3 - 1) % 12) + 1, today.day)
            due6 = 0
            due3 = 0
            for p in db.query(Person).all():
                rd = calculate_retirement_date(p)
                if not rd:
                    continue
                if rd == six:
                    due6 += 1
                if rd == three:
                    due3 += 1
            if due6:
                notify("Nghỉ hưu (6 tháng)", f"Có {due6} nhân sự sắp nghỉ hưu sau 6 tháng")
            if due3:
                notify("Nghỉ hưu (3 tháng)", f"Có {due3} nhân sự sắp nghỉ hưu sau 3 tháng")
        finally:
            db.close()

    # Chạy hàng ngày lúc 09:00
    sched.add_job(run_salary_alert, 'cron', hour=9, minute=0)
    sched.add_job(run_retirement_alert, 'cron', hour=9, minute=5)

    sched.start()
    return sched
