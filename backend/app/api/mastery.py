from typing import Final, Tuple, List
import os
import requests
import json

from .utils import constants as const

from flask import Blueprint, Response, request, make_response

API_KEY: str | None = os.environ.get("API_KEY")
BASE_URL: Final[str] = "https://na1.api.riotgames.com/lol/champion-mastery/v4"
MASTERY_TIMEOUT: Final[int] = 5

mastery_bp = Blueprint("mastery", __name__, url_prefix="/mastery")

@mastery_bp.route("/all", methods=["GET"])
def mastery_all() -> Response:
    riot_puuid = request.cookies.get("riot_puuid")

    res = make_response()
    if not riot_puuid:
        res.status_code = 401
        res.headers.update(const.DEFAULT_HEADERS)
        return res

    mastery_info = get_all_mastery(riot_puuid)
    mastery_data = json.dumps(mastery_info)

    res.response = mastery_data
    res.headers.update(const.DEFAULT_HEADERS)
    res.status_code = 200
    return res

@mastery_bp.route("/top", methods=["GET"])
def mastery_top() -> Response:
    riot_puuid = request.cookies.get("riot_puuid")

    res = make_response()
    if not riot_puuid:
        res.status_code = 401
        res.headers.update(const.DEFAULT_HEADERS)
        return res

    mastery_info = get_top_mastery(riot_puuid)
    mastery_data = json.dumps(mastery_info)

    res.response = mastery_data
    res.headers.update(const.DEFAULT_HEADERS)
    res.status_code = 200
    return res

@mastery_bp.route("/sum", methods=["GET"])
def mastery_sum():
    riot_puuid = request.cookies.get("riot_puuid")

    res = make_response()
    if not riot_puuid:
        res.status_code = 401
        res.headers.update(const.DEFAULT_HEADERS)
        return res

    mastery_info = get_sum_mastery(riot_puuid)
    mastery_data = json.dumps(mastery_info)

    res.response = mastery_data
    res.headers.update(const.DEFAULT_HEADERS)
    res.status_code = 200
    return res

def get_all_mastery(riot_puuid: str) -> Tuple[List[dict[str, str]], int]:
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

def get_top_mastery(riot_puuid: str) -> Tuple[int, dict[str, str]]:
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
    return req.status_code, mastery_info

def get_sum_mastery(riot_puuid: str) -> Tuple[int, List[dict[str, str]]]:
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
    return req.status_code, mastery_info
