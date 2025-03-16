import json
from flask import current_app as app, Blueprint, Response, make_response, request
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound

from .. import db
from ..models import PlayerMasteryData
from .utils import constants
from .utils.db_helpers import create_mastery_record, update_mastery_record, get_record_from
from .mastery import get_all_mastery

journey_bp = Blueprint('journey', __name__, url_prefix='/journey')

@journey_bp.post("/start")
def start_journey() -> Response:
    res = make_response()
    res.headers.update(constants.DEFAULT_RESPONSE_HEADERS)

    puuid: str = request.cookies.get('riot_puuid')

    mastery_info, status = get_all_mastery(puuid)
    if status >= 400:
        raise BadRequest("Riot Servers - could not retrieve all mastery")

    session = db.session
    try:
        create_mastery_record(session, puuid, mastery_info)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f"Internal error: {e}")

    res.status_code = 200
    res.response = json.dumps(mastery_info)
    return res

@journey_bp.patch("/update")
def patch_journey_information() -> Response:
    puuid = request.cookies.get("riot_puuid")
    res = make_response()

    mastery_info, status = get_all_mastery(puuid)
    if status >= 400:
        raise BadRequest("Riot Servers - could not retrieve all mastery")

    response = update_mastery_data(puuid, mastery_info)
    if response is None:
        res.status_code = 500
        return res

    res.status_code = 200
    return res


@journey_bp.get("/last_updated")
def get_journey_last_updated() -> Response:
    res = make_response()
    res.headers.update(constants.DEFAULT_RESPONSE_HEADERS)
    puuid: str = request.cookies.get("riot_puuid")

    mastery_record = get_record_from(PlayerMasteryData, db.session, puuid)
    # TODO: Get Match Records
    if mastery_record is None: # Or match_records is none
        raise NotFound("Interal - Record not found in db")

    res.response = json.dumps({"last_updated": mastery_record.get("last_updated")})
    res.status_code = 200
    return res


def update_mastery_data(puuid: str, mastery_data: JSON) -> any:
    record = get_record_from(PlayerMasteryData, db.session, puuid)
    if record is None:
        return None

    session = db.session
    try:
        update_mastery_record(session, puuid, mastery_data)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f"Internal error: {e}")

    return mastery_data


def update_match_data():
    pass

