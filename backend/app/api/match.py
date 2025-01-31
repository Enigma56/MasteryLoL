import os
import requests
from typing import Final, Optional
from flask import current_app as app, request, Response, make_response, Blueprint
# from .utils import constants

match_bp = Blueprint('match', __name__, url_prefix='/match')

BASE_URL: str = "https://americas.api.riotgames.com"
API_KEY: str | None = os.environ.get("API_KEY")
MASTERY_TIMEOUT: Final[int] = 5

@match_bp.get("/ids")
def get_match_ids():
    puuid = request.cookies.get("puuid")
    p_count: Optional[str] = request.args.get("count")

    query_params: str = get_query_params(count=p_count)
    endpoint: str = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids{query_params}"
    req = requests.get(
        endpoint,
        timeout=MASTERY_TIMEOUT,
        headers={"Content-Type": "application/json",
                 "X-RIOT-TOKEN": f"{API_KEY}"
                 }
    )
    matches = req.json()
    return matches

def get_query_params(**kwargs) -> str:
    params = "?"
    for idx, (k,v) in enumerate(kwargs.items()):
        if idx == len(kwargs)-1:
            params += f"{k}={v}"
        else:
            params += f"{k}={v}&"

    return params
