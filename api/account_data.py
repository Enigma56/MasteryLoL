from typing import Tuple
import os
import requests


def get_account(name: str, tagline: str) -> Tuple[int, dict[str, str]]:
    """
    Retrieves Riot Account information with the associated IGN and tagline
    """
    api_key: str | None = os.environ.get("API_KEY")
    url: str = f"""https://americas.api.riotgames.com/riot/account/v1/
                               accounts/by-riot-id/{name}/{tagline}"""
    req = requests.get(
            url,
            timeout=10,
            headers={"Content-Type": "application/json",
                                     "X-Riot-Token": f"{api_key}"})
    account_info = req.json()
    # print(account_info)
    req.close()
    return req.status_code, account_info
