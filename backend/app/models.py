import datetime

from typing import List
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.sqlite import JSON

from . import db


class Base(db.Model):
    __abstract__ = True

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# NOTE: Integer-type primary keys automatically increment
class TableTest(Base):
    __tablename__ = "test"

    id: Mapped[int] = db.Column('id', Integer, primary_key=True)
    name: Mapped[str] = db.Column('name', String)
    tag: Mapped[str] = db.Column('tag', String)

    def __repr__(self) -> str:
        return (
            f"TestTable(id={self.id}, game_name={self.name}, tag={self.tag})"
        )


class PlayerMasteryData(Base):
    __tablename__ = "player_mastery_data"

    riot_puuid: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    parent_id: Mapped[str] = mapped_column(ForeignKey("riot_accounts.riot_puuid"))

    created_at: Mapped[int] = mapped_column(nullable=False, default=int(datetime.datetime.now(datetime.UTC).timestamp()))
    last_updated: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp()))

    initial_mastery = mapped_column(JSON, nullable=False)
    initial_points: Mapped[int] = mapped_column(nullable=False)

    current_mastery = mapped_column(JSON, nullable=False)
    current_points: Mapped[int] = mapped_column(nullable=False)

    account: Mapped["RiotAccounts"] = db.relationship(back_populates="mastery_data", single_parent=True)

    def __repr__(self) -> str:
        return (
            f"ChampionMastery(id={self.id}, "
            f"riot_puuid='{self.riot_puuid}', "
            f"created_at={self.created_at}, "
            f"initial_level={self.initial_level})")


class RiotAccounts(Base):
    __tablename__ = "riot_accounts"

    riot_puuid: Mapped[str] = mapped_column(primary_key=True, unique=True)
    game_name: Mapped[str] = mapped_column(String(17), nullable=False)
    tag_line: Mapped[str] = mapped_column(String(6), nullable=False)
    profile_icon: Mapped[int]
    initial_summoner_level: Mapped[int]
    current_summoner_level: Mapped[int]

    # Handle account creation date and when data was last retrieved
    created_at: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp()))  # Convert account creation date in UTC to seconds
    last_updated: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp())) # Current UTC in seconds

    mastery_data: Mapped["PlayerMasteryData"] = db.relationship(back_populates="account")
    matches: Mapped[List["MatchStats"]] = db.relationship()

    def __repr__(self):
        return (f"Account(riot_puuid:{self.riot_puuid}, "
                f"game_name:{self.game_name}), "
                f"tag_line:{self.tag_line}, "
                f"summoner_level:{self.current_summoner_level}, "
                f"profile_icon:{self.profile_icon})")


class MatchStats(Base):
    __tablename__ = "match_stats"

    # NOTE: Game metadata
    match_id: Mapped[str] = mapped_column(String(14), primary_key=True)
    riot_puuid: Mapped[str] = mapped_column(ForeignKey('riot_accounts.riot_puuid'), primary_key=True)

    created_at: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp()))
    match_stats = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        return (
            f"MatchPlayerStats("
            f"match_id='{self.match_id}', "
            f"riot_puuid='{self.riot_puuid}'"
        )
