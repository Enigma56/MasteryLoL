from flask import Flask, g
import os


def create_app(test_config=None):
    """
    Create and configure the flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True
    )

    # Can load instance config at this point
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(app.instance_path)

    from . import bp_mastery
    app.register_blueprint(bp_mastery.bp)

    # These request-based functions do not need to be specific to the blueprint
    # because I only need one Blueprint for this project
    @app.before_request
    def before_any_request():
        # Open db request
        print("A request will be executed")
        g.db = "some db conn string"

    @app.teardown_request
    def request_teardown(s):
        print("A request has finished executing")

    return app
