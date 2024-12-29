import os
from flask import Flask
from dotenv import load_dotenv

from . import db as db_helpers
from .models import db


def create_app(test_config=None):
    """
    Create and configure the flask app
    """
    load_dotenv()
    environment = os.getenv("ENV")

    if environment == "dev":
        print("DEV")
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            DEBUG=True,
            TESTING=True
        )

        # Register blueprints
        from ..api.account_data import account
        # print(account)
        app.register_blueprint(account)

        dbURL = f"sqlite:///{app.root_path}/dev.db"
        print(dbURL)
        app.config["SQLALCHEMY_DATABASE_URI"] = dbURL
        app.config["SQLALCHEMY_BINDS"] = {"url": dbURL}
        app.config["SQLALCHEMY_ECHO"] = True

        db.init_app(app)

        with app.app_context():
            from . import models  # Redundant call to ensure models get imported
            try:
                db.create_all()
                print(db.metadata.tables)
            except Exception as e:
                print(e)

        return app

    elif environment == "prod":
        print("PROD")
    else:
        raise Exception(f"Unsupported environment: {environment}. Check to see if ENV variable is set to DEV or PROD")

    # NOTE: Make sure to get rid of debug and testin configs before PROD
