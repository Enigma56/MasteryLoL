import os
import requests
import json

from typing import Final, Optional
from flask import request, Response, make_response, Blueprint, jsonify
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from werkzeug.exceptions import BadRequest

from .utils import get_query_params
from .utils.constants import DEFAULT_RESPONSE_HEADERS
from .utils.db_helpers import create_match_record, get_record_from, get_match_records

from .. import db

match_bp = Blueprint('match', __name__, url_prefix='/match')

BASE_URL: str = "https://americas.api.riotgames.com"
API_KEY: str | None = os.environ.get("API_KEY")
MASTERY_TIMEOUT: Final[int] = 5


@match_bp.get("/get")
def get_matches_by_puuid():
    res = make_response()
    res.headers.update(DEFAULT_RESPONSE_HEADERS)

    puuid = request.cookies.get("riot_puuid")
    # count = request.args.get("count")

    session = db.session
    try:
        matches = get_match_records(session, puuid, 5)
    except SQLAlchemyError as e:
        raise SQLAlchemyError(e)

    json_matches = json.dumps([match.to_dict() for match in matches])
    res.response = json_matches
    return res


# NOTE: Helper Methods

def add_recent_matches():
    """
    Respond with data from 20 most recent match_ids from player account
    """
    puuid = request.cookies.get("riot_puuid")

    match_ids = get_match_ids()
    add_matches(puuid, match_ids)


def add_matches(puuid: str, match_ids: list[str]):
    for match_id in match_ids:
        res = get_match_by_id(match_id)
        if code := res.status_code >= 400:
            raise BadRequest(f"Riot Server - failed to get match stats with code {code}")

        match_stats_json = res.get_json()
        participant_index = match_stats_json["metadata"]["participants"].index(puuid)
        participant_info = match_stats_json["info"]["participants"][participant_index]
        match_stats_json["info"]["participants"] = [participant_info]

        session = db.session
        try:
            create_match_record(session, puuid, match_id, match_stats_json)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            raise SQLAlchemyError(e)


def get_match_by_id(match_id: str) -> Response:
    endpoint: str = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    req = requests.get(
        endpoint,
        timeout=MASTERY_TIMEOUT,
        headers={"Content-Type": "application/json",
                 "X-RIOT-TOKEN": f"{API_KEY}"
                 }
    )

    res = make_response(req.json())
    return res

def get_match_ids(query_params: str = ""):
    puuid = request.cookies.get("riot_puuid")
    endpoint: str = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids{query_params}"
    res = requests.get(
        endpoint,
        timeout=MASTERY_TIMEOUT,
        headers={"Content-Type": "application/json",
                 "X-RIOT-TOKEN": f"{API_KEY}"
                 }
    )

    return res.json()
