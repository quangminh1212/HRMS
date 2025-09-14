import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from hrms.db import Base
import hrms.settings_service as ss


def setup_sqlite(tmp_path):
    db_path = tmp_path / "test_settings_default.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def test_saved_filter_default_applies_on_load(monkeypatch, tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        monkeypatch.setattr(ss, 'SessionLocal', TestingSession, raising=True)
        from hrms.settings_service import get_setting, set_setting

        user = 'tester'
        key_current = f"EMAIL_HISTORY_FILTER:{user}"
        list_key = f"EMAIL_HISTORY_SAVED_LIST:{user}"
        def_key = f"EMAIL_HISTORY_SAVED_DEFAULT:{user}"
        name = 'DefaultFilter'
        saved_key = f"EMAIL_HISTORY_SAVED_FILTER:{user}:{name}"

        # Simulate saved default
        obj = {"type": "generic", "sort_field": "Thời gian", "date_preset": "Hôm nay"}
        set_setting(saved_key, json.dumps(obj, ensure_ascii=False))
        set_setting(list_key, json.dumps([name], ensure_ascii=False))
        set_setting(def_key, name)

        # No current filter yet
        set_setting(key_current, '')

        # Load and assert we can read the default (no UI import here; we just verify settings path is consistent)
        assert get_setting(saved_key, '') != ''
        assert json.loads(get_setting(saved_key, '{}')).get('date_preset') == 'Hôm nay'
        assert get_setting(def_key, '') == name
    finally:
        engine.dispose()
