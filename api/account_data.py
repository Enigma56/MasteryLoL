import requests
import os

def get_account(name: str, tagline: str) -> dict[str, str]: 
    API_KEY: str | None = os.environ.get("API_KEY")
    url: str = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}" 
    r = requests.get(url, headers={"Content-Type": "application/json", "X-Riot-Token": f"{API_KEY}"})
    dat = r.json()
    print(dat)
    return dat
