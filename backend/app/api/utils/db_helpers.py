import types

from sqlalchemy import select
from sqlalchemy.orm import Session
from flask import current_app as app

from app.models import RiotAccounts, PlayerMasteryData, MatchStats

CustomTable = RiotAccounts | PlayerMasteryData | MatchStats


def get_record_from(table: CustomTable, db_session: Session, riot_puuid: str) -> dict | None:
    try:
        record = db_session.get(table, riot_puuid)
        if record is None:
            return None
        else:
            return record.to_dict()
    except Exception as e:
        app.logger.error(f"SQLAlchemy error: {e}")
        return None

def create_mastery_record(db_session: Session, puuid: str, mastery_info: str):
    try:
        record = PlayerMasteryData(
            riot_puuid=puuid,
            initial_mastery=mastery_info,
            current_mastery=mastery_info,
            parent_id=puuid,
        )
        db_session.add(record)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"SQLAlchemy error: {e}")

def update_mastery_record(db_session: Session, puuid: str, mastery_info: str):
    try:
        record = db_session.get(PlayerMasteryData, puuid)
        record.current_mastery = {}
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"SQLAlchemy error: {e}")

# TODO: Implement getting records
def get_match_records(db_session: Session, puuid: str) -> any:
    stmt = select(MatchStats).where(MatchStats.riot_puuid == puuid)
    try:
        records = db_session.execute(stmt)
        print(records.scalars().all())
    except Exception as e:
        app.logger.error(f"SQLAlchemy error: {e}")

# TODO: Get most recent records