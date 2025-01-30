#TODO: Retrieve user from DB
from sqlalchemy.orm import Session
from flask import current_app as app

from app.models import RiotAccounts

def get_user_record(db_session: Session, riot_puuid: str) -> dict | None:
    try:
        record = db_session.get(RiotAccounts, riot_puuid)
        if record is None:
            return None
        else:
            return record.to_dict()
    except Exception as e:
        app.logger.error(f"SQLAlchemy error: {e}")
