from typing import Tuple, Final, List
import os
import requests

from flask import Blueprint, jsonify, Response, request, current_app as app
from .utils import constants as const

API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5

account = Blueprint("account", __name__, url_prefix="/account")

@account.get("/test")
def tests() -> Response:
    print("tests")
    return jsonify({"hello": "world"})


@account.route("/user", methods=["POST", "GET"])
def get_account_information() -> tuple[Response, int, dict[str, str]]:
    name: str = request.args.get("name")
    tagline: str = request.args.get("tag")
    if len(name) > const.MAX_NAME_LENGTH:
        app.logger.error("Name too long")
        return jsonify({"error": "Name too long"}), 400, const.DEFAULT_HEADERS
    if len(tagline) > const.MAX_TAG_LENGTH:
        app.logger.error("Tag too long")
        return jsonify({"error": "Tag too long"}), 400, const.DEFAULT_HEADERS

    app.logger.info(f"Getting account information for {name} with tagline: {tagline}")
    name = name.lower()
    
    if request.method == "POST":
        status, account_info = get_riot_puuid(name, tagline)
        if status >= 400:
            app.logger.error(f"Error getting account information for {name} with tagline: {tagline}")
            return jsonify({"err": "Player not found!"}), status, {}

        puuid = account_info['puuid']
        status, summoner_info = get_summoner_information(puuid)
        if status >= 400:
            app.logger.error(f"Error getting summoner information for {name} with puuid: {puuid}")
            return jsonify({"err": "puuid is invalid for found player!"}), status, {}

        # Union of two sets
        account_info |= summoner_info
        return jsonify(account_info), 200, const.DEFAULT_HEADERS
    else:
        pass

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
