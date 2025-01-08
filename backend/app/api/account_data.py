import os
import requests
from typing import Tuple, Final, List
from flask import Blueprint, jsonify, make_response, Response, request, current_app as app
from sqlalchemy import select
from .utils import constants as const
from .. import db
from ..models import TableTest

API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5

account_bp = Blueprint("account", __name__, url_prefix="/account")

@account_bp.route("/test", methods=["GET"])
def tests() -> Response:
    with app.app_context():
        test_entry = TableTest(profile="Its just a prank", tag="6969")
        db.session.add(test_entry)
        db.session.commit()
    print("tests")
    return jsonify({"hello": "world"})

@account_bp.route("/test_pk", methods=["GET"])
def tests_get() -> Response:
    app.logger.debug(f"Attempting to get pk")
    pk = request.args.get("id")
    print(pk)
    with app.app_context():
        stmt = db.session.get(TableTest, pk)
        print(stmt)

    return jsonify({"pk": pk})


@account_bp.get("/user")
def get_account_information() -> tuple[Response, int, dict[str, str]]:
    name: str = request.args.get("name")
    tagline: str = request.args.get("tag")
    if len(name) > const.MAX_NAME_LENGTH or len(name) <= 0:
        app.logger.error("Name too long")
        return jsonify({"error": "Invalid name"}), 400, const.DEFAULT_HEADERS
    if len(tagline) > const.MAX_TAG_LENGTH or len(tagline) <= 0:
        app.logger.error("Tag too long")
        return jsonify({"error": "Invalid name"}), 400, const.DEFAULT_HEADERS

    app.logger.info(f"Getting account information for {name} with tagline: {tagline}")
    name = name.lower()

    status, account_info = get_riot_puuid(name, tagline)
    if status >= 400:
        app.logger.error(f"Error getting account information for {name} with tagline: {tagline}")
        return jsonify({"error": "Player not found!"}), status, {}

    puuid = account_info['puuid']
    status, summoner_info = get_summoner_information(puuid) # Pretty sure that if the first endpoint succeeds, this will
    if status >= 400:
        app.logger.error(f"Error getting summoner information for {name} with puuid: {puuid}")
        return jsonify({"error": "puuid is invalid for found player!"}), status, {}

    # Union of two sets
    account_info |= summoner_info
    res = make_response(account_info)
    res.set_cookie("riot_puuid", account_info['puuid'])
    print(account_info)
    return res, 200, const.DEFAULT_HEADERS

@account_bp.post("/user")
def post_acccount_information() -> tuple[Response, int, dict[str, str]]:
    name: str = request.args.get("name")
    tagline: str = request.args.get("tag")
    if len(name) > const.MAX_NAME_LENGTH or len(name) <= 0:
        app.logger.error("Name too long")
        return jsonify({"error": "Invalid name"}), 400, const.DEFAULT_HEADERS
    if len(tagline) > const.MAX_TAG_LENGTH or len(tagline) <= 0:
        app.logger.error("Tag too long")
        return jsonify({"error": "Invalid name"}), 400, const.DEFAULT_HEADERS

    app.logger.info(f"Getting account information for {name} with tagline: {tagline}")
    name = name.lower()

    status, account_info = get_riot_puuid(name, tagline)
    if status >= 400:
        app.logger.error(f"Error getting account information for {name} with tagline: {tagline}")
        return jsonify({"error": "Player not found!"}), status, {}

    puuid = account_info['puuid']
    status, summoner_info = get_summoner_information(
        puuid)  # Pretty sure that if the first endpoint succeeds, this will
    if status >= 400:
        app.logger.error(f"Error getting summoner information for {name} with puuid: {puuid}")
        return jsonify({"error": "puuid is invalid for found player!"}), status, {}

    # Union of two sets
    account_info |= summoner_info
    res = make_response(account_info)
    res.set_cookie("riot_puuid", account_info['puuid'])
    print(account_info)
    return res, 200, const.DEFAULT_HEADERS

def get_riot_puuid(name: str, tagline: str) -> Tuple[int, dict[str, str]]:
    """
    Retrieves Riot Account information with the associated IGN and tagline
    """
    base_url: str = "https://americas.api.riotgames.com"
    endpoint: str = f"/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
    url: str = f"{base_url}{endpoint}"
    req = requests.get(
            url,
            timeout=ACCOUNT_TIMEOUT,
            headers={
                     "X-Riot-Token": f"{API_KEY}"
                    }
            )
    account_info = req.json()
    req.close()
    return req.status_code, account_info


def get_summoner_information(riot_puuid: str) -> Tuple[int, dict[str, str]]:
    """
    Retrieves summoner information from a provided Riot PUUID
    """
    base_url: str = "https://na1.api.riotgames.com"
    endpoint: str = f"/lol/summoner/v4/summoners/by-puuid/{riot_puuid}"
    url: str = f"{base_url}{endpoint}"
    req = requests.get(
            url,
            timeout=ACCOUNT_TIMEOUT,
            headers={
                     "X-Riot-Token": f"{API_KEY}"
                     }
            )
    summoner_info = req.json()

    return req.status_code, summoner_info
