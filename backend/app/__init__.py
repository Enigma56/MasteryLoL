import os
from flask import Flask
from dotenv import load_dotenv

from . import db as db_helpers
from .models import db


def create_app(testing=False):
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
            SQLALCHEMY_ECHO=True,
        )

        if not testing:
            db_url = f"sqlite:///{app.root_path}/dev.db"
            print(db_url)
        else:
            db_url = f"sqlite:////Users/charlielyster/Developer/Personal/MasteryLoL/backend/tests/testing.db"

        app.config.update(
            SQLALCHEMY_DATABASE_URI=db_url,
            SQLALCHEMY_BINDS={"url": db_url},
        )

        db.init_app(app)
        with app.app_context():
            from . import models  # Redundant call to ensure models get imported
            try:
                db.create_all()
                print(db.metadata.tables)
            except Exception as e:
                print(e)

        # Register blueprints
        from api.account_data import account
        app.register_blueprint(account)

        return app

    elif environment == "prod":
        print("PROD")
    else:
        raise Exception(f"Unsupported environment: {environment}. Check to see if ENV variable is set to DEV or PROD")

