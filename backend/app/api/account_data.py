import os
import requests
import json

from typing import Final
from flask import Blueprint, jsonify, make_response, Response, request, current_app as app
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed

from .. import db, models
from .utils import constants as consts, db_helpers, ParamError

API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5

account_bp = Blueprint("account", __name__, url_prefix="/account")

@account_bp.route("/user", methods=["GET", "POST"])
def get_account_information() -> Response:
    """
    Get account information from Riot API
    """
    res = make_response()
    res.headers.update(consts.DEFAULT_RESPONSE_HEADERS)

    name: str = request.args.get("name").lower()
    tagline: str = request.args.get("tag")

    if name is None or tagline is None:
        raise ParamError(f"name and tagline are both required to find a record")

    account_info, status = get_riot_puuid(name, tagline)
    if status >= 400:
        raise NotFound("Riot Servers - Account not found")

    puuid = account_info['puuid']
    record = db_helpers.get_record_from(models.RiotAccounts, db.session, puuid)
    if request.method == "GET":
        if record is None:
            raise NotFound("Interal - Account not found in db")

        res.response = json.dumps(record, default=str)
        return res

    elif request.method == "POST":
        if record is not None:
            raise BadRequest("Internal - Account already exists in db")

        app.logger.info(f"Getting account information for {name} with tagline: {tagline}")
        summoner_info, _ = get_summoner_information(puuid)
        account_info |= summoner_info  # Union of two sets

        try:
            account_entry = models.RiotAccounts(
                riot_puuid=puuid,
                game_name=account_info['gameName'],
                tag_line=account_info['tagLine'],
                profile_icon=0,
                initial_summoner_level=account_info['summonerLevel'],
                current_summoner_level=account_info['summonerLevel'])
            db.session.add(account_entry)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Error inserting user into db with err: {e}")

        res.status_code = 201
        res.set_cookie("riot_puuid", account_info['puuid'])
        res.response = json.dumps({
            "game_name": account_info["gameName"],
            "tag_line": account_info["tagLine"]},
            default=str)
        return res
    else:
        raise MethodNotAllowed(f"Method not allowed: {request.method}. Only GET and POST are allowed")


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

    return summoner_info, req.status_code


#NOTE: Test Endpoints
@account_bp.route("/test", methods=["GET"])
def tests() -> Response:
    with app.app_context():
        test_entry = models.TableTest(name="its just a prank", tag="6969")
        db.session.add(test_entry)
        db.session.commit()

    return jsonify({"hello": "world"})

@account_bp.route("/test_pk", methods=["GET"])
def tests_get() -> Response:
    app.logger.debug(f"Attempting to get pk")
    pk = request.args.get("id")
    print(pk)
    with app.app_context():
        stmt = db.session.get(models.TableTest, pk)
        print(stmt)

    return jsonify({"pk": pk})
