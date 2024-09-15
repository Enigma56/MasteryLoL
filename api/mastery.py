from typing import Final, Tuple
import os
import requests

API_KEY: str | None = os.environ.get("API_KEY")
BASE_URL: Final[str] = "https://na1.api.riotgames.com/lol/champion-mastery/v4"
MASTERY_TIMEOUT: Final[int] = 5


def get_all_mastery_by_puuid(riot_puuid: str) -> Tuple[int, dict[str, str]]:
    endpoint: str = f"/champion-masteries/by-puuid/{riot_puuid}"
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


def get_top_mastery_by_puuid(riot_puuid: str) -> Tuple[int, dict[str, str]]:
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


def get_sum_mastery_by_puuid(riot_puuid: str) -> Tuple[int, dict[str, str]]:
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
