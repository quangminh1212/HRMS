from datetime import datetime, timedelta

from sqlalchemy import create_engine, event, func
from sqlalchemy.orm import sessionmaker

from hrms.db import Base
from hrms.models import EmailLog


def setup_sqlite(tmp_path):
    db_path = tmp_path / "test_extra.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    # register REGEXP in case needed later
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


ession = None

def seed_email_logs(Session):
    s = Session()
    now = datetime.utcnow()
    rows = [
        # no body, no attachments, no error, sent
        EmailLog(type='generic', unit_name='U1', recipients='a@x', subject='S1', body='', attachments='', status='sent', error=None, created_at=now - timedelta(days=1), user_id=1),
        # body, one attachment, empty error, sent
        EmailLog(type='generic', unit_name='U2', recipients='b@x', subject='S2', body='Body', attachments='exports/a.txt', status='sent', error='', created_at=now - timedelta(days=2), user_id=2),
        # body, two attachments, error, failed
        EmailLog(type='generic', unit_name='U1', recipients='c@x', subject='S3', body='X', attachments='exports/a.txt, exports/b.txt', status='failed', error='err', created_at=now - timedelta(days=3), user_id=3),
        # no body, no attachments, no error, failed
        EmailLog(type='generic', unit_name='U3', recipients='d@x', subject='S4', body=None, attachments=None, status='failed', error=None, created_at=now - timedelta(days=4), user_id=4),
    ]
    s.add_all(rows)
    s.commit()


def test_has_body_and_no_attachments_and_no_error_and_only_success(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        seed_email_logs(TestingSession)
        s = TestingSession()
        # has_body: body not null and not empty => rows 2,3
        q_has_body = s.query(EmailLog).filter(EmailLog.body != None).filter(EmailLog.body != '')
        assert q_has_body.count() == 2
        # no_attachments: attachments is null or empty => rows 1,4
        q_no_att = s.query(EmailLog).filter((EmailLog.attachments == None) | (EmailLog.attachments == ''))
        assert q_no_att.count() == 2
        # only_success: status sent => rows 1,2
        q_sent = s.query(EmailLog).filter(EmailLog.status == 'sent')
        assert q_sent.count() == 2
        # no_error: error is null or empty => rows 1,2,4
        q_no_err = s.query(EmailLog).filter((EmailLog.error == None) | (EmailLog.error == ''))
        assert q_no_err.count() == 3
    finally:
        s.close()
        engine.dispose()


def test_max_attachments_expression(tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        seed_email_logs(TestingSession)
        s = TestingSession()
        # compute att_count using SQLite expression
        att_count_expr = (func.length(EmailLog.attachments) - func.length(func.replace(EmailLog.attachments, ',', '')) + 1)
        att_count_expr = func.coalesce(att_count_expr, 0)
        # rows with attachments <= 1 (and not null/empty) should include row 2 only
        rows = s.query(EmailLog, att_count_expr.label('cnt')).filter(EmailLog.attachments != None).filter(EmailLog.attachments != '').filter(att_count_expr <= 1).all()
        assert len(rows) == 1
        assert rows[0][0].subject == 'S2'
    finally:
        s.close()
        engine.dispose()
