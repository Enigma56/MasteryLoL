from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed


class ParamError(Exception):
    pass

def register_custom_error_handlers(app):
    # API Handlers
    @app.errorhandler(BadRequest)
    def handle_bad_request(err):
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(NotFound)
    def handle_not_found_error(err):
        return jsonify({"error": str(err)}), 404

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(err):
        return jsonify({"error": str(err)}), 405

    # Custom Handlers
    @app.errorhandler(ParamError)
    def handle_param_error(err):
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(err):
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(err):
        return jsonify({"error": str(err)}), 500