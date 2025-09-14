import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from hrms.db import Base
import hrms.settings_service as ss


def setup_sqlite(tmp_path):
    db_path = tmp_path / "test_settings.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def test_saved_filters_crud(monkeypatch, tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        # Monkeypatch SessionLocal used by settings_service to isolated SQLite
        monkeypatch.setattr(ss, 'SessionLocal', TestingSession, raising=True)
        from hrms.settings_service import get_setting, set_setting

        user = 'tester'
        current_key = f"EMAIL_HISTORY_FILTER:{user}"
        list_key = f"EMAIL_HISTORY_SAVED_LIST:{user}"
        name = 'MyFilter'
        saved_key = f"EMAIL_HISTORY_SAVED_FILTER:{user}:{name}"

        # 1) Save current filter
        cur = {"type": "generic", "sort_field": "Thời gian", "sort_field2": "(Không)", "sort_asc": True}
        set_setting(current_key, json.dumps(cur, ensure_ascii=False))
        assert get_setting(current_key, None) is not None

        # 2) Save as named filter and update list
        set_setting(saved_key, get_setting(current_key, ''))
        raw = get_setting(list_key, '') or ''
        names = []
        if raw.strip():
            names = json.loads(raw)
        if name not in names:
            names.append(name)
        set_setting(list_key, json.dumps(names, ensure_ascii=False))

        assert name in json.loads(get_setting(list_key, '[]'))
        assert json.loads(get_setting(saved_key, '{}'))["type"] == "generic"

        # 3) Overwrite existing saved filter
        cur2 = {"type": "generic", "sort_field": "Subject", "sort_field2": "Số tệp", "sort_asc": False, "sort_asc2": False}
        set_setting(current_key, json.dumps(cur2, ensure_ascii=False))
        set_setting(saved_key, get_setting(current_key, ''))
        got = json.loads(get_setting(saved_key, '{}'))
        assert got["sort_field"] == "Subject"
        assert got.get("sort_asc2") is False

        # 4) Delete saved filter (simulate UI behavior: remove from list and blank value)
        raw = get_setting(list_key, '') or ''
        names = json.loads(raw) if raw.strip() else []
        names = [n for n in names if n != name]
        set_setting(list_key, json.dumps(names, ensure_ascii=False))
        set_setting(saved_key, '')

        assert name not in json.loads(get_setting(list_key, '[]'))
        assert (get_setting(saved_key, '') or '') == ''
    finally:
        engine.dispose()
