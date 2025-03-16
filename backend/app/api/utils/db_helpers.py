import json

from sqlalchemy import select, JSON
from sqlalchemy.orm import Session

from app.models import RiotAccounts, PlayerMasteryData, MatchStats

Table = RiotAccounts | PlayerMasteryData | MatchStats


def get_record_from(table: Table, db_session: Session, riot_puuid: str) -> dict | None:
    record = db_session.get(table, riot_puuid)
    return record.to_dict() if record else None


def create_mastery_record(db_session: Session, puuid: str, mastery_info: JSON, points: int):
    record = PlayerMasteryData(
        parent_id=puuid,
        riot_puuid=puuid,

        initial_mastery=mastery_info,
        initial_points=points,

        current_mastery=mastery_info,
        current_points=points
    )
    db_session.add(record)


def create_match_record(db_session: Session, puuid: str, match_id, match_stats: JSON):
    record = MatchStats(
        match_id=match_id,
        riot_puuid=puuid,
        match_stats=match_stats
    )
    db_session.add(record)


def update_mastery_record(db_session: Session, puuid: str, mastery_info: JSON):
    record = db_session.get(PlayerMasteryData, puuid)
    points = get_total_points(db_session, puuid)

    record.current_mastery = mastery_info
    record.current_points = points

    db_session.flush()


def get_match_records(db_session: Session, puuid: str) -> any:
    stmt = select(MatchStats).where(MatchStats.riot_puuid == puuid)
    records = db_session.execute(stmt).scalars().all()
    return records

def get_total_points(db_session: Session, puuid: str) -> int:
    record = db_session.get(PlayerMasteryData, puuid)
    mastery_data = record.current_mastery

    points = sum([champ['championPoints'] for champ in mastery_data])
    return points


# # TODO: Load the environment variables in app/__init__.py
# def create_db_url(turso_db_url, turso_auth_token) -> str:
#     TURSO_DATABASE_URL = turso_db_url
#     TURSO_AUTH_TOKEN = turso_auth_token
#     dbURL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=True"
#
#     return dbURL