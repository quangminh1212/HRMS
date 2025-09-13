from datetime import datetime, time, date
from typing import Optional
from queue import Queue

from apscheduler.schedulers.background import BackgroundScheduler

from .db import SessionLocal
from .models import Person
from .salary import list_due_in_window
from .retirement import calculate_retirement_date
from .mailer import send_alert, send_email_with_attachment_retry

# Hàng đợi thông báo để UI lấy và hiển thị popup
NOTIFY_QUEUE: Queue[tuple[str, str]] = Queue()


def notify(title: str, message: str):
    # Đưa thông báo vào hàng đợi và in log console
    try:
        NOTIFY_QUEUE.put_nowait((title, message))
    except Exception:
        pass
    print(f"[NOTICE] {title}: {message}")


def schedule_jobs():
    sched = BackgroundScheduler()

    # Gửi nâng lương theo đơn vị + ZIP tổng hợp nếu bật
    def run_salary_alert_by_unit(start, end):
        from pathlib import Path
        from .salary import export_due_to_excel
        from .mailer import send_email_with_attachment, get_recipients_for_unit, create_zip
        from .settings_service import get_setting
        from .models import Unit
        try:
            dbu = SessionLocal()
            Path('exports').mkdir(exist_ok=True)
            q = ((end.month - 1)//3) + 1
            files = []
            units = dbu.query(Unit).order_by(Unit.name).all()
            for u in units:
                recips = get_recipients_for_unit(u.name)
                if not recips:
                    continue
                arr = list_due_in_window(dbu, start, end, unit_id=u.id)
                if not arr:
                    continue
                out = Path('exports')/f"nang_luong_quy_{end.year}_Q{q}_{u.name.replace(' ', '_')}.xlsx"
                export_due_to_excel(arr, str(out), template_name=None, username='Scheduler')
                ok = send_email_with_attachment(f"[HRMS] Nâng lương Q{q}/{end.year} - {u.name}", f"Đính kèm danh sách cho {u.name}", [str(out)], to=recips)
                files.append(str(out))
                try:
                    # mask recipients
                    masked = []
                    for r in recips:
                        r = str(r or '').strip()
                        if '@' in r:
                            masked.append('***@' + r.split('@',1)[1])
                        elif r:
                            masked.append('***')
                    from .models import EmailLog
                    dbu.add(EmailLog(type='salary_due', unit_name=u.name, recipients=", ".join(masked)[:1000], subject=f"Nâng lương Q{q}/{end.year} - {u.name}", body=f"Gửi danh sách cho {u.name}", attachments=str(out), status='sent' if ok else 'failed'))
                    dbu.commit()
                except Exception:
                    pass
            # ZIP summary if enabled
            try:
                flag = (get_setting('SEND_SUMMARY_ZIP','0') or '0').strip().lower() in ('1','true','yes')
                if flag and files:
                    zip_path = Path('exports')/f"nang_luong_quy_{end.year}_Q{q}_by_unit.zip"
                    if create_zip(files, str(zip_path)):
                        send_email_with_attachment(f"[HRMS] Nâng lương Q{q}/{end.year} (ZIP tổng hợp)", f"ZIP tổng hợp danh sách nâng lương theo đơn vị Q{q}/{end.year}", [str(zip_path)])
            except Exception:
                pass
        finally:
            try:
                dbu.close()
            except Exception:
                pass

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
                msg = f"Có {len(items)} nhân sự đến hạn trong quý này"
                notify("Nâng lương định kỳ", msg)
                try:
                    send_alert("[HRMS] Nâng lương định kỳ", msg)
                except Exception:
                    pass
                # Xuất Excel và gửi email đính kèm
                try:
                    from pathlib import Path
                    from .salary import export_due_to_excel
from .mailer import send_email_with_attachment_retry as send_email_with_attachment
                    Path("exports").mkdir(exist_ok=True)
                    q = ((end.month - 1)//3) + 1
                    out = Path("exports") / f"nang_luong_quy_{end.year}_Q{q}.xlsx"
                    export_due_to_excel(items, str(out), template_name=None, username="Scheduler")
                    body = msg + f"\nĐính kèm file: {out.name}"
                    send_email_with_attachment("[HRMS] Danh sách đến hạn nâng lương", body, [str(out)])
                except Exception:
                    pass
                # Gửi theo đơn vị nếu có mapping
                run_salary_alert_by_unit(start, end)
        finally:
            db.close()

    # Cảnh báo nghỉ hưu: 6 tháng và 3 tháng
    def run_retirement_alert():
        db = SessionLocal()
        try:
            today = date.today()
            six = date(today.year + (today.month + 6 - 1) // 12, ((today.month + 6 - 1) % 12) + 1, today.day)
            three = date(today.year + (today.month + 3 - 1) // 12, ((today.month + 3 - 1) % 12) + 1, today.day)
            list6 = []
            list3 = []
            for p in db.query(Person).all():
                rd = calculate_retirement_date(p)
                if not rd:
                    continue
                if rd == six:
                    list6.append(p)
                if rd == three:
                    list3.append(p)
            if list6:
                msg = f"Có {len(list6)} nhân sự sắp nghỉ hưu sau 6 tháng"
                notify("Nghỉ hưu (6 tháng)", msg)
                try:
                    send_alert("[HRMS] Nghỉ hưu (6 tháng)", msg)
                except Exception:
                    pass
            if list3:
                msg = f"Có {len(list3)} nhân sự sắp nghỉ hưu sau 3 tháng"
                notify("Nghỉ hưu (3 tháng)", msg)
                try:
                    send_alert("[HRMS] Nghỉ hưu (3 tháng)", msg)
                except Exception:
                    pass
            # Nếu có danh sách, export Excel và gửi kèm
            if list6 or list3:
                try:
                    from pathlib import Path
                    from .reporting import export_retirement_alerts_to_excel
                    from .mailer import send_email_with_attachment
                    Path('exports').mkdir(exist_ok=True)
                    out = Path('exports')/f"nghi_huu_thong_bao_{today.isoformat()}.xlsx"
                    export_retirement_alerts_to_excel(db, list6, list3, str(out))
                    send_email_with_attachment('[HRMS] Danh sách nghỉ hưu (6/3 tháng)', 'Đính kèm danh sách nghỉ hưu (6/3 tháng)', [str(out)])
                except Exception:
                    pass
        finally:
            db.close()

    # BHXH hàng tháng: ngày 1 hàng tháng lúc 09:15
    def run_insurance_monthly():
        from datetime import date
        from calendar import monthrange
        from pathlib import Path
        from .insurance import export_insurance_to_excel
from .mailer import send_email_with_attachment_retry as send_email_with_attachment, get_recipients_for_unit
        today = date.today()
        # khoảng tháng trước
        prev_month = (today.month - 2) % 12 + 1
        prev_year = today.year - 1 if today.month == 1 else today.year
        start = date(prev_year, prev_month, 1)
        last_day = monthrange(prev_year, prev_month)[1]
        end = date(prev_year, prev_month, last_day)
        db = SessionLocal()
        try:
            Path('exports').mkdir(exist_ok=True)
            # tổng hợp chung
            out = Path('exports')/f"bhxh_{prev_year}_{prev_month:02d}.xlsx"
            export_insurance_to_excel(db, start, end, str(out), username='Scheduler')
            send_email_with_attachment('[HRMS] Báo cáo BHXH tháng', f'Đính kèm BHXH {prev_month:02d}/{prev_year}', [str(out)])
            # theo đơn vị
            from .models import Unit
            units = db.query(Unit).all()
            for u in units:
                recips = get_recipients_for_unit(u.name)
                if not recips:
                    continue
                outu = Path('exports')/f"bhxh_{prev_year}_{prev_month:02d}_{u.name.replace(' ', '_')}.xlsx"
                export_insurance_to_excel(db, start, end, str(outu), username='Scheduler', unit_id=u.id)
                send_email_with_attachment('[HRMS] BHXH tháng theo đơn vị', f'Đính kèm BHXH {prev_month:02d}/{prev_year} - {u.name}', [str(outu)], to=recips)
        except Exception:
            pass
        finally:
            db.close()

    # Hợp đồng hết hạn trong N ngày tới
    def run_contracts_expiring():
        from datetime import timedelta, date
        from pathlib import Path
        from .contracts import export_contracts_expiring_to_excel
        from .mailer import send_email_with_attachment, get_recipients_for_unit
        from .settings_service import get_setting
        today = date.today()
        days = int(get_setting('CONTRACT_ALERT_DAYS', '30') or '30')
        end = today + timedelta(days=days)
        db = SessionLocal()
        try:
            Path('exports').mkdir(exist_ok=True)
            # tổng hợp chung
            out = Path('exports')/f"contracts_expiring_{today.isoformat()}_{days}d.xlsx"
            export_contracts_expiring_to_excel(db, today, end, str(out))
            send_email_with_attachment('[HRMS] Hợp đồng sắp hết hạn', f'Đính kèm danh sách HĐ sắp hết hạn trong {days} ngày tới', [str(out)])
            # theo đơn vị
            from .models import Unit
            units = db.query(Unit).all()
            for u in units:
                recips = get_recipients_for_unit(u.name)
                if not recips:
                    continue
                outu = Path('exports')/f"contracts_expiring_{today.isoformat()}_{days}d_{u.name.replace(' ', '_')}.xlsx"
                export_contracts_expiring_to_excel(db, today, end, str(outu), unit_id=u.id)
                send_email_with_attachment('[HRMS] HĐ sắp hết hạn theo đơn vị', f'Đính kèm HĐ sắp hết hạn trong {days} ngày tới - {u.name}', [str(outu)], to=recips)
        except Exception:
            pass
        finally:
            db.close()

    # BHXH hàng tháng: ngày 1 hàng tháng lúc 09:15
    def run_insurance_monthly():
        from datetime import date
        from calendar import monthrange
        from pathlib import Path
        from .insurance import export_insurance_to_excel
from .mailer import send_email_with_attachment_retry as send_email_with_attachment, get_recipients_for_unit, create_zip
        today = date.today()
        prev_month = (today.month - 2) % 12 + 1
        prev_year = today.year - 1 if today.month == 1 else today.year
        start = date(prev_year, prev_month, 1)
        last_day = monthrange(prev_year, prev_month)[1]
        end = date(prev_year, prev_month, last_day)
        db = SessionLocal()
        try:
            Path('exports').mkdir(exist_ok=True)
            out = Path('exports')/f"bhxh_{prev_year}_{prev_month:02d}.xlsx"
            export_insurance_to_excel(db, start, end, str(out), username='Scheduler')
# Gửi tổng hợp
            ok = send_email_with_attachment('[HRMS] Báo cáo BHXH tháng', f'Đính kèm BHXH {prev_month:02d}/{prev_year}', [str(out)])
            try:
                # Log email tổng hợp
                from .db import SessionLocal
                from .models import EmailLog
                s = SessionLocal();
                s.add(EmailLog(type='bhxh_monthly', unit_name=None, recipients='', subject='[HRMS] Báo cáo BHXH tháng', body=f'BHXH {prev_month:02d}/{prev_year}', attachments=str(out), status='sent' if ok else 'failed'))
                s.commit(); s.close()
            except Exception: pass
            # Theo đơn vị + ZIP tổng hợp nếu bật
            from .models import Unit
            units = db.query(Unit).all()
            files = []
            for u in units:
                recips = get_recipients_for_unit(u.name)
                if not recips:
                    continue
                outu = Path('exports')/f"bhxh_{prev_year}_{prev_month:02d}_{u.name.replace(' ', '_')}.xlsx"
                export_insurance_to_excel(db, start, end, str(outu), username='Scheduler', unit_id=u.id)
                files.append(str(outu))
                ok_u = send_email_with_attachment('[HRMS] BHXH tháng theo đơn vị', f'Đính kèm BHXH {prev_month:02d}/{prev_year} - {u.name}', [str(outu)], to=recips)
                try:
                    # Ghi EmailLog chi tiết
                    masked = []
                    for r in recips:
                        r = str(r or '').strip()
                        if '@' in r:
                            masked.append('***@' + r.split('@',1)[1])
                        elif r:
                            masked.append('***')
                    from .db import SessionLocal
                    from .models import EmailLog
                    s2 = SessionLocal(); s2.add(EmailLog(type='bhxh_monthly', unit_name=u.name, recipients=", ".join(masked)[:1000], subject='BHXH tháng theo đơn vị', body=f"BHXH {prev_month:02d}/{prev_year} - {u.name}", attachments=str(outu), status='sent' if ok_u else 'failed')); s2.commit(); s2.close()
                except Exception:
                    pass
            try:
                from .settings_service import get_setting
                flag = (get_setting('SEND_SUMMARY_ZIP','0') or '0').strip().lower() in ('1','true','yes')
                if flag and files:
                    zip_path = Path('exports')/f"bhxh_{prev_year}_{prev_month:02d}_by_unit.zip"
                    if create_zip(files, str(zip_path)):
                        send_email_with_attachment('[HRMS] BHXH tháng (ZIP tổng hợp)', f'ZIP tổng hợp BHXH {prev_month:02d}/{prev_year}', [str(zip_path)])
            except Exception:
                pass
        except Exception:
            pass
        finally:
            db.close()

    # Hợp đồng hết hạn trong N ngày tới
    def run_contracts_expiring():
        from datetime import timedelta, date
        from pathlib import Path
        from .contracts import export_contracts_expiring_to_excel
from .mailer import send_email_with_attachment_retry as send_email_with_attachment, get_recipients_for_unit, create_zip
        from .settings_service import get_setting
        today = date.today()
        days = int(get_setting('CONTRACT_ALERT_DAYS','30') or '30')
        end = today + timedelta(days=days)
        db = SessionLocal()
        try:
            Path('exports').mkdir(exist_ok=True)
            out = Path('exports')/f"contracts_expiring_{today.isoformat()}_{days}d.xlsx"
            export_contracts_expiring_to_excel(db, today, end, str(out))
            ok = send_email_with_attachment('[HRMS] HĐ sắp hết hạn', f'Đính kèm HĐ sắp hết hạn trong {days} ngày tới', [str(out)])
            try:
                from .db import SessionLocal
                from .models import EmailLog
                s = SessionLocal(); s.add(EmailLog(type='contracts_expiring', unit_name=None, recipients='', subject='[HRMS] HĐ sắp hết hạn', body=f'{days} ngày', attachments=str(out), status='sent' if ok else 'failed')); s.commit(); s.close()
            except Exception: pass
            # Theo đơn vị + ZIP tổng hợp nếu bật
            from .models import Unit
            units = db.query(Unit).all()
            files = []
            for u in units:
                recips = get_recipients_for_unit(u.name)
                if not recips:
                    continue
                outu = Path('exports')/f"contracts_expiring_{today.isoformat()}_{days}d_{u.name.replace(' ', '_')}.xlsx"
                export_contracts_expiring_to_excel(db, today, end, str(outu), unit_id=u.id)
                files.append(str(outu))
                ok_u = send_email_with_attachment('[HRMS] HĐ sắp hết hạn theo đơn vị', f'Đính kèm HĐ sắp hết hạn trong {days} ngày tới - {u.name}', [str(outu)], to=recips)
                try:
                    masked = []
                    for r in recips:
                        r = str(r or '').strip()
                        if '@' in r:
                            masked.append('***@' + r.split('@',1)[1])
                        elif r:
                            masked.append('***')
                    from .db import SessionLocal
                    from .models import EmailLog
                    s2 = SessionLocal(); s2.add(EmailLog(type='contracts_expiring', unit_name=u.name, recipients=", ".join(masked)[:1000], subject='HĐ sắp hết hạn theo đơn vị', body=f"{days} ngày - {u.name}", attachments=str(outu), status='sent' if ok_u else 'failed')); s2.commit(); s2.close()
                except Exception:
                    pass
            try:
                flag = (get_setting('SEND_SUMMARY_ZIP','0') or '0').strip().lower() in ('1','true','yes')
                if flag and files:
                    zip_path = Path('exports')/f"contracts_expiring_{today.isoformat()}_{days}d_by_unit.zip"
                    if create_zip(files, str(zip_path)):
                        send_email_with_attachment('[HRMS] HĐ sắp hết hạn (ZIP tổng hợp)', 'ZIP tổng hợp HĐ sắp hết hạn các đơn vị', [str(zip_path)])
            except Exception:
                pass
        except Exception:
            pass
        finally:
            db.close()

    # Chạy hàng ngày lúc 09:00
    sched.add_job(run_salary_alert, 'cron', hour=9, minute=0)
    sched.add_job(run_retirement_alert, 'cron', hour=9, minute=5)
    sched.add_job(run_insurance_monthly, 'cron', day=1, hour=9, minute=15)
    sched.add_job(run_contracts_expiring, 'cron', hour=9, minute=20)

    # Dọn dẹp thư mục exports hằng ngày
    def cleanup_exports():
        try:
            from pathlib import Path
            import time, os
            from .settings_service import get_setting
            ttl_days = int(get_setting('EXPORT_TTL_DAYS','30') or '30')
            cutoff = time.time() - ttl_days * 86400
            p = Path('exports')
            if not p.exists():
                return
            removed = 0
            for f in p.iterdir():
                try:
                    if f.is_file():
                        st = f.stat()
                        if st.st_mtime < cutoff:
                            os.remove(f)
                            removed += 1
                except Exception:
                    pass
            if removed:
                print(f"[CLEANUP] Removed {removed} export file(s) older than {ttl_days} days")
        except Exception as ex:
            print(f"[CLEANUP] error: {ex}")

    sched.add_job(cleanup_exports, 'cron', hour=3, minute=0)

    sched.start()
    return sched
