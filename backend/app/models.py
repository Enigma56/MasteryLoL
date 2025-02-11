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

    #id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    riot_puuid: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(db.DateTime, nullable=False, default=func.now())
    last_updated: Mapped[int] = mapped_column(db.Integer, default=func.now())  # Current UTC in seconds

    # Store Mastery data in JSON format
    initial_mastery: Mapped[dict] = mapped_column(db.JSON, nullable=False)
    current_mastery: Mapped[dict] = mapped_column(db.JSON, nullable=False)

    parent_id: Mapped[str] = mapped_column(db.String, db.ForeignKey("riot_accounts.riot_puuid"))
    account: Mapped["RiotAccounts"] = db.relationship(back_populates="mastery_data")

    # initial_level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # champion_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # champion_level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # champion_points: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return (
            f"ChampionMastery(id={self.id}, "
            f"riot_puuid='{self.riot_puuid}', "
            f"created_at={self.created_at!r}, "
            f"initial_level={self.initial_level})")

class RiotAccounts(db.Model):
    __tablename__ = "riot_accounts"

    riot_puuid: Mapped[str] = mapped_column(primary_key=True, unique=True)
    game_name: Mapped[str] = mapped_column(db.String(17), nullable=False)
    tag_line: Mapped[str] = mapped_column(db.String(6), nullable=False)
    profile_icon: Mapped[int] = mapped_column(db.Integer)
    initial_summoner_level: Mapped[int] = mapped_column(db.Integer)
    current_summoner_level: Mapped[int] = mapped_column(db.Integer)

    # Handle account creation date and when data was last retrieved
    created_at: Mapped[DateTime] = mapped_column(db.DateTime, default=func.now())  # Convert account creation date in UTC to seconds
    last_updated: Mapped[DateTime] = mapped_column(db.DateTime, default=func.now()) # Current UTC in seconds

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

    map_id: Mapped[int] = mapped_column(db.Integer)
    queue_id: Mapped[int] = mapped_column(db.Integer)
    team_id: Mapped[int] = mapped_column(db.Integer)
    game_creation: Mapped[int] = mapped_column(db.Integer)
    game_mode: Mapped[str] = mapped_column(db.String)
    game_ended_in_early_surrender: Mapped[bool] = mapped_column(db.Boolean)
    game_ended_in_surrender: Mapped[bool] = mapped_column(db.Boolean)
    team_early_surrendered: Mapped[bool] = mapped_column(db.Boolean)
    game_duration: Mapped[int] = mapped_column(db.Integer)
    win: Mapped[bool] = mapped_column(db.Boolean)
    lane: Mapped[str] = mapped_column(db.String(20))
    role: Mapped[str] = mapped_column(db.String(20))
    time_played: Mapped[int] = mapped_column(db.Integer)
    # team_position: Mapped[str] = mapped_column(db.String(20))
    # subteam_placement: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Objective-related stats
    objectives_stolen: Mapped[int] = mapped_column(db.Integer)
    objectives_stolen_assists: Mapped[int] = mapped_column(db.Integer)
    nexus_kills: Mapped[int] = mapped_column(db.Integer)
    nexus_takedowns: Mapped[int] = mapped_column(db.Integer)
    nexus_lost: Mapped[int] = mapped_column(db.Integer)
    inhibitor_kills: Mapped[int] = mapped_column(db.Integer)
    inhibitor_takedowns: Mapped[int] = mapped_column(db.Integer)
    inhibitors_lost: Mapped[int] = mapped_column(db.Integer)
    damage_dealt_to_buildings: Mapped[int] = mapped_column(db.Integer)
    damage_dealt_to_objectives: Mapped[int] = mapped_column(db.Integer)
    damage_dealt_to_turrets: Mapped[int] = mapped_column(db.Integer)
    turret_kills: Mapped[int] = mapped_column(db.Integer)
    turret_takedowns: Mapped[int] = mapped_column(db.Integer)
    turrets_lost: Mapped[int] = mapped_column(db.Integer)
    first_blood_assist: Mapped[bool] = mapped_column(db.Boolean)
    first_blood_kill: Mapped[bool] = mapped_column(db.Boolean)
    first_tower_assist: Mapped[bool] = mapped_column(db.Boolean)
    first_tower_kill: Mapped[bool] = mapped_column(db.Boolean)

    baron_kills: Mapped[int] = mapped_column(db.Integer)
    dragon_kills: Mapped[int] = mapped_column(db.Integer)
    detector_wards_placed: Mapped[int] = mapped_column(db.Integer)
    # bounty_level: Mapped[int] = mapped_column(db.Integer)
    # eligible_for_progression: Mapped[bool] = mapped_column(db.Boolean)
    # individual_position: Mapped[str] = mapped_column(db.String(20))

    # NOTE: Champion-related stats
    champ_experience: Mapped[int] = mapped_column(db.Integer)
    champ_level: Mapped[int] = mapped_column(db.Integer)
    champion_id: Mapped[int] = mapped_column(db.Integer)
    champion_name: Mapped[str] = mapped_column(db.String(50))
    # summoner_level: Mapped[int] = mapped_column(db.Integer)
    # summoner_name: Mapped[str] = mapped_column(db.String(50))
    # champion_transform: Mapped[int] = mapped_column(db.Integer)


    summoner1_casts: Mapped[int] = mapped_column(db.Integer)
    summoner1_id: Mapped[int] = mapped_column(db.Integer)
    summoner2_casts: Mapped[int] = mapped_column(db.Integer)
    summoner2_id: Mapped[int] = mapped_column(db.Integer)
    summoner_id: Mapped[str] = mapped_column(db.String(63))
    spell1_casts: Mapped[int] = mapped_column(db.Integer)
    spell2_casts: Mapped[int] = mapped_column(db.Integer)
    spell3_casts: Mapped[int] = mapped_column(db.Integer)
    spell4_casts: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Item-related
    gold_earned: Mapped[int] = mapped_column(db.Integer)
    gold_spent: Mapped[int] = mapped_column(db.Integer)
    consumables_purchased: Mapped[int] = mapped_column(db.Integer)
    item0: Mapped[int] = mapped_column(db.Integer)
    item1: Mapped[int] = mapped_column(db.Integer)
    item2: Mapped[int] = mapped_column(db.Integer)
    item3: Mapped[int] = mapped_column(db.Integer)
    item4: Mapped[int] = mapped_column(db.Integer)
    item5: Mapped[int] = mapped_column(db.Integer)
    item6: Mapped[int] = mapped_column(db.Integer)  # NOTE: The Ward purchased
    # items_purchased: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Kill-related stats
    deaths: Mapped[int] = mapped_column(db.Integer)
    assists: Mapped[int] = mapped_column(db.Integer)
    kills: Mapped[int] = mapped_column(db.Integer)
    double_kills: Mapped[int] = mapped_column(db.Integer)
    triple_kills: Mapped[int] = mapped_column(db.Integer)
    quadra_kills: Mapped[int] = mapped_column(db.Integer)
    penta_kills: Mapped[int] = mapped_column(db.Integer)
    killing_sprees: Mapped[int] = mapped_column(db.Integer)
    largest_killing_spree: Mapped[int] = mapped_column(db.Integer)
    largest_multi_kill: Mapped[int] = mapped_column(db.Integer)
    neutral_minions_killed: Mapped[int] = mapped_column(db.Integer)
    # unreal_kills: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Damage-related stats
    largest_critical_strike: Mapped[int] = mapped_column(db.Integer)
    longest_time_spent_living: Mapped[int] = mapped_column(db.Integer)
    magic_damage_dealt: Mapped[int] = mapped_column(db.Integer)
    magic_damage_dealt_to_champions: Mapped[int] = mapped_column(db.Integer)
    magic_damage_taken: Mapped[int] = mapped_column(db.Integer)
    physical_damage_dealt: Mapped[int] = mapped_column(db.Integer)
    physical_damage_dealt_to_champions: Mapped[int] = mapped_column(db.Integer)
    physical_damage_taken: Mapped[int] = mapped_column(db.Integer)
    damage_self_mitigated: Mapped[int] = mapped_column(db.Integer)
    total_damage_dealt: Mapped[int] = mapped_column(db.Integer)
    total_damage_dealt_to_champions: Mapped[int] = mapped_column(db.Integer)
    total_damage_shielded_on_teammates: Mapped[int] = mapped_column(db.Integer)
    total_damage_taken: Mapped[int] = mapped_column(db.Integer)
    true_damage_dealt: Mapped[int] = mapped_column(db.Integer)
    true_damage_dealt_to_champions: Mapped[int] = mapped_column(db.Integer)
    true_damage_taken: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Misc Stats
    time_ccing_others: Mapped[int] = mapped_column(db.Integer)
    total_ally_jungle_minions_killed: Mapped[int] = mapped_column(db.Integer)
    total_enemy_jungle_minions_killed: Mapped[int] = mapped_column(db.Integer)
    total_heal: Mapped[int] = mapped_column(db.Integer)
    total_heals_on_teammates: Mapped[int] = mapped_column(db.Integer)
    total_minions_killed: Mapped[int] = mapped_column(db.Integer)
    total_time_cc_dealt: Mapped[int] = mapped_column(db.Integer)
    total_time_spent_dead: Mapped[int] = mapped_column(db.Integer)
    total_units_healed: Mapped[int] = mapped_column(db.Integer)

    # NOTE: Ward-related
    wards_placed: Mapped[int] = mapped_column(db.Integer)
    wards_killed: Mapped[int] = mapped_column(db.Integer)
    vision_score: Mapped[int] = mapped_column(db.Integer)
    vision_wards_bought_in_game: Mapped[int] = mapped_column(db.Integer)
    sight_wards_bought_in_game: Mapped[int] = mapped_column(db.Integer)
    # hold_pings: Mapped[int] = mapped_column(db.Integer)
    # get_back_pings: Mapped[int] = mapped_column(db.Integer)
    # all_in_pings: Mapped[int] = mapped_column(db.Integer)
    # on_my_way_pings: Mapped[int] = mapped_column(db.Integer)
    # need_vision_pings: Mapped[int] = mapped_column(db.Integer)
    # assist_me_pings: Mapped[int] = mapped_column(db.Integer)
    # enemy_missing_pings: Mapped[int] = mapped_column(db.Integer)
    # enemy_vision_pings: Mapped[int] = mapped_column(db.Integer)
    # vision_cleared_pings: Mapped[int] = mapped_column(db.Integer)
    # command_pings: Mapped[int] = mapped_column(db.Integer)

    # placement: Mapped[int] = mapped_column(db.Integer)
    # player_augment1: Mapped[int] = mapped_column(db.Integer)
    # player_augment2: Mapped[int] = mapped_column(db.Integer)
    # player_augment3: Mapped[int] = mapped_column(db.Integer)
    # player_augment4: Mapped[int] = mapped_column(db.Integer)
    # player_subteam_id: Mapped[int] = mapped_column(db.Integer)
    # push_pings: Mapped[int] = mapped_column(db.Integer)
    # profile_icon: Mapped[int] = mapped_column(db.Integer)
    # puuid: Mapped[str] = mapped_column(db.String(78))
    # riot_id_game_name: Mapped[str] = mapped_column(db.String(50))
    # riot_id_name: Mapped[str] = mapped_column(db.String(50))
    # riot_id_tagline: Mapped[str] = mapped_column(db.String(20))

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
