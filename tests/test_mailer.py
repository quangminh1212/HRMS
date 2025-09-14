import os
import sys
import json
import uuid
import importlib
from pathlib import Path


def _reload_modules():
    for m in list(sys.modules.keys()):
        if m.startswith('hrms.') or m == 'hrms':
            sys.modules.pop(m, None)


def _setup_db(db_name: str):
    os.environ['DATABASE_URL'] = f'sqlite:///data/{db_name}'
    # ensure data dir exists
    Path('data').mkdir(exist_ok=True)
    _reload_modules()
    import hrms.db as db
    import hrms.models as models
    # create tables
    models.Base.metadata.create_all(bind=db.engine)
    return db, models


def test_get_recipients_for_unit_db_preferred():
    db_name = f'test_mailer_{uuid.uuid4().hex}.db'
    db, models = _setup_db(db_name)
    s = db.SessionLocal()
    try:
        # settings fallback says different values
        s.add(models.Setting(key='UNIT_EMAILS', value=json.dumps({'Phòng A': ['fallback@example.com']})))
        # create unit and recipients (with invalid and duplicate)
        u = models.Unit(name='Phòng A')
        s.add(u); s.commit(); s.refresh(u)
        recs = [
            models.UnitEmailRecipient(unit_id=u.id, email='user1@example.com', active=True),
            models.UnitEmailRecipient(unit_id=u.id, email='USER1@example.com', active=True),  # dup diff case
            models.UnitEmailRecipient(unit_id=u.id, email='invalid', active=True),  # invalid
            models.UnitEmailRecipient(unit_id=u.id, email='user2@example.com', active=False),  # inactive
            models.UnitEmailRecipient(unit_id=u.id, email='user3@example.com', active=True),
        ]
        s.add_all(recs); s.commit()
    finally:
        s.close()
    import hrms.mailer as mailer
    emails = mailer.get_recipients_for_unit('Phòng A')
    # Should prefer DB, filter invalid/inactive/duplicates
    assert 'user1@example.com' in emails
    assert 'user3@example.com' in emails
    assert 'fallback@example.com' not in emails
    assert 'invalid' not in emails
    # no duplicates
    assert len(emails) == len(set([e.lower() for e in emails]))


def test_get_recipients_for_unit_fallback_settings():
    db_name = f'test_mailer_{uuid.uuid4().hex}.db'
    db, models = _setup_db(db_name)
    s = db.SessionLocal()
    try:
        # No UnitEmailRecipient for this unit -> fallback to settings
        s.add(models.Setting(key='UNIT_EMAILS', value=json.dumps({'Unit X': ['a@example.com', 'A@EXAMPLE.com', 'bad', 'b@example.com']})))
        s.add(models.Unit(name='Unit X'))
        s.commit()
    finally:
        s.close()
    import hrms.mailer as mailer
    emails = mailer.get_recipients_for_unit('Unit X')
    assert 'a@example.com' in emails
    assert 'b@example.com' in emails
    assert 'bad' not in emails
    # dedup
    assert len(emails) == len(set([e.lower() for e in emails]))


def test_send_email_with_attachment_retry(monkeypatch):
    # Patch underlying send to simulate failures then success
    calls = {'count': 0}

    def fake_send(subject, body, attachments, to=None, suppress_log=False):
        calls['count'] += 1
        # fail twice then succeed
        return calls['count'] >= 3

    _reload_modules()
    import hrms.mailer as mailer
    monkeypatch.setattr(mailer, 'send_email_with_attachment', fake_send)
    ok = mailer.send_email_with_attachment_retry('s', 'b', [])
    assert ok is True
    assert calls['count'] == 3

    # Now always fail
    calls['count'] = 0

    def always_fail(subject, body, attachments, to=None, suppress_log=False):
        calls['count'] += 1
        return False

    monkeypatch.setattr(mailer, 'send_email_with_attachment', always_fail)
    ok2 = mailer.send_email_with_attachment_retry('s', 'b', [], retries=2, delay=0)
    assert ok2 is False
    assert calls['count'] == 3
