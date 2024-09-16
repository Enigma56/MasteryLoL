from typing import Tuple, Final
import os
import requests


API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5


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
    # print(account_info)
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


def get_account_information(name: str, tagline: str) -> dict[str, str]:
    status, account_info = get_riot_puuid(name, tagline)
    if status >= 400:
        return {"err": "Player not found!"}

    puuid = account_info['puuid']
    status, summoner_info = get_summoner_information(puuid)
    if status >= 400:
        return {"err": "puuid is invalid for found player!"}

    account_info |= summoner_info
    return account_info
