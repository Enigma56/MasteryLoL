from typing import Tuple
import os
import requests


def get_account(name: str, tagline: str) -> Tuple[int, dict[str, str]]:
    APIKEY: str | None = os.environ.get("API_KEY")
    url: str = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
    r = requests.get(url, headers={"Content-Type": "application/json", "X-Riot-Token": f"{APIKEY}"})
    account_info = r.json()
    # print(account_info)
    r.close()
    return r.status_code, account_info
