import os
import requests
import json

from typing import Final
from flask import Blueprint, jsonify, make_response, Response, request, current_app as app
from sqlalchemy.exc import DatabaseError

from .utils import constants as consts, db_helpers
from .. import db
from ..models import TableTest, RiotAccounts

API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5
EMPTY_RESPONSE: Final[str] = json.dumps({})

account_bp = Blueprint("account", __name__, url_prefix="/account")

@account_bp.get("/user")
def get_account_information() -> Response:
    """
    Get account information from Riot API
    """
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    name: str = request.args.get("name").lower()
    tagline: str = request.args.get("tag")

    if name is None or tagline is None:
        raise ValueError(f"name are both required to find a record")

    account_info, status = get_riot_puuid(name, tagline)
    if status >= 400:
        app.logger.error(f"Error getting account information for {name} with tagline: {tagline}")
        res.status_code = status
        res.response = json.dumps({"error": f"Error getting account information for {name}"})
        return res

    riot_puuid = account_info['puuid']
    user_record = db_helpers.get_record_from(RiotAccounts, db.session, riot_puuid)
    if user_record is None:
        res.status_code = 404
        res.response = json.dumps({"error": f"Riot account with id:{riot_puuid} not found"})
        return res

    res.response = json.dumps(user_record, default=str)
    return res


@account_bp.post("/user")
def post_acccount_information() -> Response:
    """
    Create account in DB or retrieve existing record
    """
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    name: str = request.args.get("name").lower()
    tagline: str = request.args.get("tag")

    if name is None or tagline is None:
        raise ValueError(f"name are both required to find a record")

    account_info, status = get_riot_puuid(name, tagline)
    if status >= 400:
        app.logger.error(f"Error getting account information for {name} with tagline: {tagline}")
        res.status_code = status
        res.response = json.dumps({"error": f"Error getting account information for {name}"})
        return res

    puuid = account_info['puuid']

    record = db_helpers.get_record_from(RiotAccounts, db.session, puuid)
    if record is not None:
        app.logger.error("Riot account already exists")
        res.status_code = 400
        res.response = json.dumps({"error": f"Riot account already exists"})
        return res

    app.logger.info(f"Getting account information for {name} with tagline: {tagline}")
    _, summoner_info = get_summoner_information(puuid)
    account_info |= summoner_info # Union of two sets

    try:
        account_entry = RiotAccounts(
            riot_puuid=puuid,
            game_name=account_info['gameName'],
            tag_line=account_info['tagLine'],
            profile_icon=0,
            initial_summoner_level=account_info['summonerLevel'],
            current_summoner_level=account_info['summonerLevel'])
        db.session.add(account_entry)
        db.session.commit()
    except DatabaseError as e:
        app.logger.error(f"Error inserting user into db with err: {e}")
        db.session.rollback()

        res.status_code = 400
        res.response = json.dumps({"error": f"Error inserting user into db"})
        return res

    res.status_code=201
    res.set_cookie("riot_puuid", account_info['puuid'])
    res.response = json.dumps({"game_name": account_info["gameName"], "tag_line": account_info["tagLine"]}, default=str)
    return res



def get_riot_puuid(name: str, tagline: str):
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
    return account_info, req.status_code


# TODO: Rethink this method and how it works
def get_summoner_information(riot_puuid: str):
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


#NOTE: Test Endpoints
@account_bp.route("/test", methods=["GET"])
def tests() -> Response:
    with app.app_context():
        test_entry = TableTest(name="its just a prank", tag="6969")
        db.session.add(test_entry)
        db.session.commit()

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
