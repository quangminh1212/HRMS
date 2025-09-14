import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from hrms.db import Base
import hrms.settings_service as ss


def setup_sqlite(tmp_path):
    db_path = tmp_path / "test_settings2.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    return engine, TestingSession


def test_saved_filters_rename_and_duplicate(monkeypatch, tmp_path):
    engine, TestingSession = setup_sqlite(tmp_path)
    try:
        monkeypatch.setattr(ss, 'SessionLocal', TestingSession, raising=True)
        from hrms.settings_service import get_setting, set_setting

        user = 'tester'
        list_key = f"EMAIL_HISTORY_SAVED_LIST:{user}"
        name = 'FilterA'
        saved_key = f"EMAIL_HISTORY_SAVED_FILTER:{user}:{name}"
        set_setting(saved_key, json.dumps({"k": 1}, ensure_ascii=False))
        set_setting(list_key, json.dumps([name], ensure_ascii=False))

        # rename
        new_name = 'FilterRenamed'
        new_key = f"EMAIL_HISTORY_SAVED_FILTER:{user}:{new_name}"
        # simulate logic: write new key, blank old, update list
        set_setting(new_key, get_setting(saved_key, ''))
        set_setting(saved_key, '')
        names = json.loads(get_setting(list_key, '[]'))
        names = [new_name if x == name else x for x in names]
        if new_name not in names:
            names.append(new_name)
        set_setting(list_key, json.dumps(names, ensure_ascii=False))
        assert get_setting(new_key, '') != ''
        assert get_setting(saved_key, '') == ''
        assert new_name in json.loads(get_setting(list_key, '[]'))

        # duplicate
        dup = 'FilterCopy'
        dup_key = f"EMAIL_HISTORY_SAVED_FILTER:{user}:{dup}"
        set_setting(dup_key, get_setting(new_key, ''))
        names2 = json.loads(get_setting(list_key, '[]'))
        if dup not in names2:
            names2.append(dup)
        set_setting(list_key, json.dumps(names2, ensure_ascii=False))
        assert get_setting(dup_key, '') != ''
        assert dup in json.loads(get_setting(list_key, '[]'))
    finally:
        engine.dispose()
