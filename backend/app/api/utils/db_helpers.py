from sqlalchemy import select, JSON
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from flask import current_app as app

from app.models import RiotAccounts, PlayerMasteryData, MatchStats

Table = RiotAccounts | PlayerMasteryData | MatchStats


def get_record_from(table: Table, db_session: Session, riot_puuid: str) -> dict | None:
    record = db_session.get(table, riot_puuid)
    return record.to_dict() if record else None


def create_mastery_record(db_session: Session, puuid: str, mastery_info: JSON):
    record = PlayerMasteryData(
        riot_puuid=puuid,
        initial_mastery=mastery_info,
        current_mastery=mastery_info,
        parent_id=puuid,
    )
    db_session.add(record)



def update_mastery_record(db_session: Session, puuid: str, mastery_info: JSON):
    record = db_session.get(PlayerMasteryData, puuid)
    record.current_mastery = mastery_info


# TODO: Implement getting records
def get_match_records(db_session: Session, puuid: str) -> any:
    stmt = select(MatchStats).where(MatchStats.riot_puuid == puuid)
    try:
        records = db_session.execute(stmt)
        print(records.scalars().all())
    except SQLAlchemyError as e:
        app.logger.error(f"SQLAlchemy error: {e}")

# TODO: Get most recent records

# # TODO: Load the environment variables in app/__init__.py
# def create_db_url(turso_db_url, turso_auth_token) -> str:
#     TURSO_DATABASE_URL = turso_db_url
#     TURSO_AUTH_TOKEN = turso_auth_token
#     dbURL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=True"
#
#     return dbURL