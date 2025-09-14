from datetime import datetime, timedelta

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from hrms.db import Base
from hrms.models import EmailLog
from hrms.reporting import compute_email_summary


def setup_db(tmp_path):
    db_path = tmp_path / "test_summary.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def seed(Session):
    s = Session()
    now = datetime.utcnow()
    rows = [
        EmailLog(type='a', unit_name='U1', recipients='a@x', subject='S1', body='B', attachments='', status='sent', error=None, created_at=now, user_id=1),
        EmailLog(type='a', unit_name='U2', recipients='b@x', subject='S2', body='B', attachments='', status='failed', error='e', created_at=now, user_id=1),
        EmailLog(type='b', unit_name='U1', recipients='c@x', subject='S3', body='B', attachments='', status='sent', error=None, created_at=now, user_id=2),
    ]
    s.add_all(rows); s.commit()


def test_compute_email_summary(tmp_path):
    engine, TestingSession = setup_db(tmp_path)
    try:
        seed(TestingSession)
        s = TestingSession()
        base = s.query(EmailLog)
        summary = compute_email_summary(s, base)
        by_status = dict(summary['by_status'])
        by_type = dict(summary['by_type'])
        assert by_status.get('sent', 0) == 2
        assert by_status.get('failed', 0) == 1
        assert by_type.get('a', 0) == 2
        assert by_type.get('b', 0) == 1
    finally:
        s.close(); engine.dispose()
