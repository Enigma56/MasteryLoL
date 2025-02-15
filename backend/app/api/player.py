import datetime
import time
import json
from flask import current_app as app, Blueprint, Response, make_response, request

from .. import db
from .utils.db_helpers import create_mastery_record, update_mastery_record, get_record_from
from .utils import constants
from .mastery import get_all_mastery
from ..models import PlayerMasteryData

player_bp = Blueprint('player', __name__, url_prefix='/player')

@player_bp.post("/journey/start")
def start_journey() -> Response:
    res = make_response()
    res.headers.update(constants.DEFAULT_RESPONSE_HEADERS)

    puuid: str = request.cookies.get('riot_puuid')

    mastery_info, status = get_all_mastery(puuid)
    if status >= 400:
        res.status_code = status
        return res

    mastery_data = json.dumps(mastery_info)
    with app.app_context():
        create_mastery_record(db.session, puuid, mastery_data)

    return res

@player_bp.patch("/journey/update")
def patch_journey_information() -> Response:
    puuid = request.cookies.get("riot_puuid")
    res = make_response()

    mastery_info, status = get_all_mastery(puuid)
    if status >= 400:
        res.status_code = status
        return res

    mastery_data = json.dumps(mastery_info)
    response = update_mastery_data(puuid, mastery_data)
    if response is None:
        res.status_code = 500
        return res

    res.status_code = 200
    return res


@player_bp.get("/journey/last_updated")
def get_journey_last_updated() -> Response:
    res = make_response()
    res.headers.update(constants.DEFAULT_RESPONSE_HEADERS)
    puuid: str = request.cookies.get("riot_puuid")

    with app.app_context():
        mastery_record = get_record_from(PlayerMasteryData, db.session, puuid)
        # TODO: Get Match Records
        if mastery_record is None: # Or match_records is none
            res.status_code = 404
            return res

    res.response = json.dumps({"last_updated": mastery_record.get("last_updated")})
    res.status_code = 200
    return res


def update_mastery_data(puuid: str, mastery_data: str) -> any:
    with app.app_context():
        record = get_record_from(PlayerMasteryData, db.session, puuid)
        if record is None:
            return None
        else:
            update_mastery_record(db.session, puuid, mastery_data)
            return mastery_data


def update_match_data():
    pass

