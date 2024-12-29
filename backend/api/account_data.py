from typing import Tuple, Final, List
import os
import requests

from flask import Blueprint, jsonify, Response, request

API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5

account = Blueprint("account", __name__, url_prefix="/account")

@account.get("/test")
def test() -> Response:
    print("test")
    return jsonify({"status": "ok"})


@account.get("/user")
def get_account_information() -> Response:
    name = request.args.get("name")
    tagline = request.args.get("tag")
    print(f"Getting account information for {name} with tagline: {tagline}")
    name = name.lower()
    status, account_info = get_riot_puuid(name, tagline)
    if status >= 400:
        return jsonify({"err": "Player not found!"})

    puuid = account_info['puuid']
    status, summoner_info = get_summoner_information(puuid)
    if status >= 400:
        return jsonify({"err": "puuid is invalid for found player!"})

    # Union of two sets
    account_info |= summoner_info
    return jsonify(account_info)

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
            headers={"Content-Type": "application/json",
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
            headers={"Content-Type": "application/json",
                     "X-RIOT-Token": f"{API_KEY}"
                     }
            )
    summoner_info = req.json()

    return req.status_code, summoner_info
