import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

dbURL = f"sqlite+{TURSO_DATABASE_URL}/?authToken{TURSO_AUTH_TOKEN}&secure=True"
engine = create_engine(dbURL, echo=True)
db_session = scoped_session(sessionmaker(engine))


def init_db():
    pass
