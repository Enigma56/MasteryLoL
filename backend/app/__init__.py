import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

from . import db as db_helpers
# from .models import db

Base = declarative_base()
db = SQLAlchemy(model_class=Base)

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
            SQLALCHEMY_ECHO=False,
        )

        if not testing:
            db_url = f"sqlite:///{app.root_path}/dev.db"
            print(db_url)
        else:
            db_url = f"sqlite:////Users/charlielyster/Developer/Personal/MasteryLoL/backend/tests/testing.db"

        app.config.update(
            SQLALCHEMY_DATABASE_URI=db_url,
        )

        db.init_app(app)

        if not testing:
            with app.app_context():
                from .models import TestTable, RiotAccounts, PlayerMasteryData, MatchStats # Redundant call to ensure models get imported
                try:
                    db.create_all()
                except Exception as e:
                    print(e)

        # Register blueprints
        from .api import mastery as m
        from .api import account_data as acc
        app.register_blueprint(acc.account_bp)
        app.register_blueprint(m.mastery_bp)

        @app.route('/', methods=['GET'])
        def test():
            return {"hello": "world"}, 200

        return app

    elif environment == "prod":
        print("PROD")
    else:
        raise Exception(f"Unsupported environment: {environment}. Check to see if ENV variable is set to DEV or PROD")

