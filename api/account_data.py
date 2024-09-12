from typing import Tuple, Final
import os
import requests


API_KEY: str | None = os.environ.get("API_KEY")
ACCOUNT_TIMEOUT: Final[int] = 5


def get_riot_puuid(name: str, tagline: str) -> Tuple[int, str]:
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
    return req.status_code, account_info["puuid"]


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
