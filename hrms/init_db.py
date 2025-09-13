from .db import Base, engine
from .models import *  # noqa: F401,F403


def init_db():
    Base.metadata.create_all(bind=engine)
