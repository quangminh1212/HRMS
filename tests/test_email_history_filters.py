from datetime import datetime, timedelta

from sqlalchemy import create_engine, event, func
from sqlalchemy.orm import sessionmaker

from hrms.db import Base
from hrms.models import EmailLog


def setup_sqlite(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    @event.listens_for(engine, "connect")
    def _sqlite_regexp(dbapi_connection, connection_record):
        import re as _re
        def regexp(pattern, string):
            try:
                if string is None:
                    return 0
                return 1 if _re.search(pattern, str(string)) else 0
            except Exception:
                return 0
        dbapi_connection.create_function("REGEXP", 2, regexp)
        dbapi_connection.create_function("regexp", 2, regexp)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def seed_email_logs(Session):
    s = Session()
    now = datetime.utcnow()
    rows = [
        EmailLog(type='generic', unit_name='Unit A', recipients='a@x,y@z', subject='Hello World', body='Body', attachments='', status='sent', error=None, created_at=now - timedelta(days=1), user_id=1),
        EmailLog(type='generic', unit_name='Unit B', recipients='b@x', subject='Error: Mail bounced', body='Body', attachments='exports/a.txt', status='failed', error='bounced', created_at=now - timedelta(days=2), user_id=2),
        EmailLog(type='generic', unit_name='Unit A', recipients='c@x', subject='Report Q3', body='Body', attachments='exports/a.txt, exports/b.txt', status='sent', error=None, created_at=now - timedelta(days=10), user_id=1),
        EmailLog(type='generic', unit_name='Unit C', recipients='d@x', subject='Retry Subject', body='Body', attachments=None, status='failed', error='timeout', created_at=now - timedelta(days=31), user_id=3),
    ]
    s.add_all(rows)
    s.commit()


def test_recipients_filters(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        seed_email_logs(TestingSession)
        s = TestingSession()
        # contains b@x -> second row
        q = s.query(EmailLog).filter(func.instr(EmailLog.recipients, 'b@x') > 0)
        assert q.count() == 1
        # not contains b@x -> others
        q2 = s.query(EmailLog).filter(func.instr(EmailLog.recipients, 'b@x') == 0)
        assert q2.count() == 3
    finally:
        s.close()
        engine.dispose()


def test_stats_attachment_counts(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        seed_email_logs(TestingSession)
        s = TestingSession()
        # count attachments approx by splitting commas
        rows = s.query(EmailLog.attachments).all()
        count = 0
        for (att,) in rows:
            for part in (att or '').split(','):
                if part.strip():
                    count += 1
        assert count >= 3  # we seeded two files in one row and one in another
    finally:
        s.close()
        engine.dispose()

import os
import tempfile
import json
import re
from datetime import datetime, timedelta

import pytest

from hrms.db import Base, create_engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from hrms.models import EmailLog


def setup_sqlite(tmp_path):
    # isolate sqlite file
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    # register REGEXP on this engine
    @event.listens_for(engine, "connect")
    def _sqlite_regexp(dbapi_connection, connection_record):
        import re as _re
        def regexp(pattern, string):
            try:
                if string is None:
                    return 0
                return 1 if _re.search(pattern, str(string)) else 0
            except Exception:
                return 0
        try:
            dbapi_connection.create_function("regexp", 2, regexp)
            dbapi_connection.create_function("REGEXP", 2, regexp)
        except Exception:
            pass
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def seed_email_logs(Session):
    s = Session()
    now = datetime.utcnow()
    rows = [
        EmailLog(type='generic', unit_name='Unit A', recipients='a@x', subject='Hello World', body='Body', attachments='', status='sent', error=None, created_at=now - timedelta(days=1), user_id=1),
        EmailLog(type='generic', unit_name='Unit B', recipients='b@x', subject='Error: Mail bounced', body='Body', attachments='exports/a.txt', status='failed', error='bounced', created_at=now - timedelta(days=2), user_id=2),
        EmailLog(type='generic', unit_name='Unit A', recipients='c@x', subject='Report Q3', body='Body', attachments='exports/a.txt, exports/b.txt', status='sent', error=None, created_at=now - timedelta(days=10), user_id=1),
        EmailLog(type='generic', unit_name='Unit C', recipients='d@x', subject='Retry Subject', body='Body', attachments=None, status='failed', error='timeout', created_at=now - timedelta(days=31), user_id=3),
    ]
    s.add_all(rows)
    s.commit()


def test_subject_regex_and_negative(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        s = TestingSession()
        seed_email_logs(TestingSession)
        # regex match 'Error:'
        q = s.query(EmailLog).filter(EmailLog.subject.op('REGEXP')('^Error:'))
        assert q.count() == 1
        # not contains 'Report'
        q2 = s.query(EmailLog).filter(~EmailLog.subject.ilike('%Report%'))
        assert q2.count() == 3
    finally:
        s.close()
        engine.dispose()


def test_has_attachments_and_error_filters(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        s = TestingSession()
        seed_email_logs(TestingSession)
        # has attachments
        q = s.query(EmailLog).filter(EmailLog.attachments != None).filter(EmailLog.attachments != '')
        assert q.count() == 2
        # error contains
        q2 = s.query(EmailLog).filter(EmailLog.error.ilike('%bounce%'))
        assert q2.count() == 1
        # error not contains
        q3 = s.query(EmailLog).filter(~EmailLog.error.ilike('%time%'))
        # one row has error None, ~ilike(None) is NULL-safe if we OR with error is NULL
        q3 = s.query(EmailLog).filter((EmailLog.error == None) | (~EmailLog.error.ilike('%time%')))
        assert q3.count() >= 2
    finally:
        s.close()
        engine.dispose()


def test_my_only_and_sort(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        s = TestingSession()
        seed_email_logs(TestingSession)
        # my_only user_id=1
        q = s.query(EmailLog).filter(EmailLog.user_id == 1)
        assert q.count() == 2
        # sort asc by created_at
        rows = s.query(EmailLog).order_by(EmailLog.created_at.asc()).all()
        assert rows[0].created_at <= rows[-1].created_at
    finally:
        s.close()
        engine.dispose()