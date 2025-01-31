import json
from flask import current_app as app, Blueprint, Response, make_response, request
from sqlalchemy.exc import DatabaseError

from .. import db
from ..models import PlayerMasteryData
from .utils import constants
from .mastery import get_all_mastery

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

    mastery_data = json.dumps(mastery_info[0])

    with app.app_context():
        try:
            player_mastery_data = PlayerMasteryData(
                riot_puuid=puuid,
                parent_id=puuid,

                initial_mastery=mastery_data,
                current_mastery=mastery_data,
            )
            db.session.add(player_mastery_data)
        except DatabaseError as e:
            app.logger.error(e)
            db.session.rollback()
            res.status_code = 404
            return res
        finally:
            db.session.commit()
    return res

#TODO: Implement starting a mastery journey
@player_bp.put("/journey/update")
def update_journey() -> Response:
    res = make_response()
    res.headers.update(constants.DEFAULT_RESPONSE_HEADERS)
    return res
