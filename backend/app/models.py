from typing import List
import datetime


from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from . import db

# NOTE: Integer-type primary keys automatically increment
class TableTest(db.Model):
    __tablename__ = "test"

    id: Mapped[int] = db.Column('id', db.Integer, primary_key=True)
    name: Mapped[str] = db.Column('name', db.String)
    tag: Mapped[str] = db.Column('tag', db.String)

    def __repr__(self) -> str:
        return (
            f"TestTable(id={self.id}, game_name={self.name}, tag={self.tag})"
        )

class PlayerMasteryData(db.Model):
    __tablename__ = "player_mastery_data"

    riot_puuid: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    created_at: Mapped[int] = mapped_column(nullable=False, default=int(datetime.datetime.now(datetime.UTC).timestamp()))
    last_updated: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp()))

    # Store Mastery data in JSON format
    initial_mastery: Mapped[dict] = mapped_column(db.JSON, nullable=False)
    current_mastery: Mapped[dict] = mapped_column(db.JSON, nullable=False)

    parent_id: Mapped[str] = mapped_column(db.String, db.ForeignKey("riot_accounts.riot_puuid"))
    account: Mapped["RiotAccounts"] = db.relationship(back_populates="mastery_data", single_parent=True)

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return (
            f"ChampionMastery(id={self.id}, "
            f"riot_puuid='{self.riot_puuid}', "
            f"created_at={self.created_at}, "
            f"initial_level={self.initial_level})")

class RiotAccounts(db.Model):
    __tablename__ = "riot_accounts"

    riot_puuid: Mapped[str] = mapped_column(primary_key=True, unique=True)
    game_name: Mapped[str] = mapped_column(db.String(17), nullable=False)
    tag_line: Mapped[str] = mapped_column(db.String(6), nullable=False)
    profile_icon: Mapped[int]
    initial_summoner_level: Mapped[int]
    current_summoner_level: Mapped[int]

    # Handle account creation date and when data was last retrieved
    created_at: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp()))  # Convert account creation date in UTC to seconds
    last_updated: Mapped[int] = mapped_column(default=int(datetime.datetime.now(datetime.UTC).timestamp())) # Current UTC in seconds

    mastery_data: Mapped["PlayerMasteryData"] = db.relationship(back_populates="account")
    matches: Mapped[List["MatchStats"]] = db.relationship()

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return (f"Account(riot_puuid:{self.riot_puuid}, "
                f"game_name:{self.game_name}), "
                f"tag_line:{self.tag_line}, "
                f"summoner_level:{self.summoner_level}, "
                f"profile_icon:{self.profile_icon})")

# Stats for an individual player in a match
class MatchStats(db.Model):
    __tablename__ = "match_stats"

    # NOTE: Game metadata
    match_id: Mapped[str] = mapped_column(db.String(14), primary_key=True)
    riot_puuid: Mapped[str] = mapped_column(db.String, db.ForeignKey('riot_accounts.riot_puuid'), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(db.DateTime, default=func.now())
    match_stats: Mapped[dict] = mapped_column(db.JSON, nullable=False)

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return (
            f"MatchPlayerStats("
            f"match_id='{self.match_id}', "
            f"riot_puuid='{self.riot_puuid}', "
            f"champion_name='{self.champion_name}', "
            f"kills={self.kills}, "
            f"deaths={self.deaths}, "
            f"assists={self.assists}, "
            f"win={self.win})"
        )
