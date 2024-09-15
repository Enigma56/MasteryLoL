from flask import Flask


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

    @app.route("/home")
    def home():
        return "This is home!"

    return app
