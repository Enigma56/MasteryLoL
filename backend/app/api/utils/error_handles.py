from flask import current_app as app, jsonify
from sqlalchemy.exc import SQLAlchemyError


class ParamException(Exception):
    pass


@app.errorhandler(ParamException)
def handle_param_error(err):
    return jsonify({"error": err.message}), 400


@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(err):
    return jsonify({"error": err.message}), 500