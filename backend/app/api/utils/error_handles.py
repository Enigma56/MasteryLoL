from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


class ParamException(Exception):
    pass

def register_custom_error_handlers(app):
    @app.errorhandler(ParamException)
    def handle_param_error(err):
        return jsonify({"error": err.message}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(err: ValueError):
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(Exception)
    def handle_generic_exception(err):
        return jsonify({"error": "A generic exception"}), 100


    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(err):
        return jsonify({"error": err.message}), 500