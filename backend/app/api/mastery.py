import os
import requests
import json

from typing import Final, Tuple, List
from flask import Blueprint, Response, request, make_response
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import Unauthorized, BadRequest

from .utils import constants as consts, create_mastery_record
from .. import db

API_KEY: str | None = os.environ.get("API_KEY")
BASE_URL: Final[str] = "https://na1.api.riotgames.com/lol/champion-mastery/v4"
MASTERY_TIMEOUT: Final[int] = 5

mastery_bp = Blueprint("mastery", __name__, url_prefix="/mastery")

# TODO: Add records to DB

@mastery_bp.route("/all", methods=["GET"])
def mastery_all() -> Response:
    """
    Handle mastery list and refresh DB
    """
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    riot_puuid = request.cookies.get("riot_puuid")
    if not riot_puuid:
        raise Unauthorized("No puuid cookie is set")

    mastery_info, status = get_all_mastery(riot_puuid)
    if status >= 400:
        raise BadRequest("Invalid puuid")

    res.response = json.dumps(mastery_info)
    res.status_code = 200
    return res

@mastery_bp.route("/top", methods=["GET"])
def mastery_top() -> Response:
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    riot_puuid = request.cookies.get("riot_puuid")
    if not riot_puuid:
        raise Unauthorized("No puuid cookie is set")

    mastery_info, status = get_top_mastery(riot_puuid)
    if status >= 400:
        raise BadRequest("Riot Servers - Could not process your request")

    res.response = json.dumps(mastery_info)[1]
    res.status_code = 200
    return res

@mastery_bp.route("/sum", methods=["GET"])
def mastery_sum():
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    riot_puuid = request.cookies.get("riot_puuid")
    if not riot_puuid:
        raise Unauthorized("No puuid cookie is set")

    mastery_info, status = get_sum_mastery(riot_puuid)
    if status >= 400:
        raise BadRequest("Riot Servers - Could not process your request")

    res.response = json.dumps(mastery_info)
    res.status_code = 200
    return res

def get_all_mastery(riot_puuid: str) -> Tuple[JSON, int]:
    endpoint: str = f"/champion-masteries/by-puuid/{riot_puuid}"
    url: str = f"{BASE_URL}{endpoint}"
    req = requests.get(
            url,
            timeout=MASTERY_TIMEOUT,
            headers={
                     "X-RIOT-TOKEN": f"{API_KEY}"
                    }
            )
    mastery_info = req.json()
    return  mastery_info, req.status_code


def get_top_mastery(riot_puuid: str) -> Tuple[JSON, int]:
    endpoint: str = f"/champion-masteries/by-puuid/{riot_puuid}/top"
    url: str = f"{BASE_URL}{endpoint}"
    req = requests.get(
            url,
            timeout=MASTERY_TIMEOUT,
            headers={"Content-Type": "application/json",
                     "X-RIOT-TOKEN": f"{API_KEY}"
                     }
            )
    mastery_info = req.json()
    return mastery_info, req.status_code

def get_sum_mastery(riot_puuid: str) -> Tuple[JSON, int]:
    """
    Get a player's total champion mastery score, which is the sum of
    individual champion mastery levels.
    """
    endpoint: str = f"/scores/by-puuid/{riot_puuid}"
    url: str = f"{BASE_URL}{endpoint}"
    req = requests.get(
            url,
            timeout=MASTERY_TIMEOUT,
            headers={"Content-Type": "application/json",
                     "X-RIOT-TOKEN": f"{API_KEY}"
                     }
            )
    mastery_info = req.json()
    return mastery_info, req.status_code
