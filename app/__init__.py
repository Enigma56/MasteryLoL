from flask import Flask
from dotenv import load_dotenv


def create_app(test_config=None):
    """
    Create and configure the flask app
    """
    load_dotenv()

    # NOTE: Make sure to get rid of debug and testin configs before PROD
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True,
        TESTING=True
       )

    from . import bp_mastery
    app.register_blueprint(bp_mastery.bp)

    # NOTE: Sessions automatically created.
    # Sessions only need to be removed after request.
    @app.teardown_request
    def request_teardown(s):
        pass
    return app
