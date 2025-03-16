import os
import logging

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import declarative_base

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
        CORS(app, supports_credentials=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            DEBUG=True,
            SQLALCHEMY_ECHO=False,
        )

        app.logger.setLevel(logging.DEBUG)

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
                from .models import TableTest, RiotAccounts, PlayerMasteryData, MatchStats
                try:
                    db.drop_all()
                    db.create_all()
                except Exception as e:
                    print(e)

        # Register blueprints
        from .api import mastery, account_data, match, player
        app.register_blueprint(account_data.account_bp)
        app.register_blueprint(mastery.mastery_bp)
        app.register_blueprint(match.match_bp)
        app.register_blueprint(player.journey_bp)

        from .api.utils import register_custom_error_handlers
        register_custom_error_handlers(app)

        @app.route('/', methods=['GET'])
        def test():
            routes = []
            for rule in app.url_map.iter_rules():
                if rule.endpoint != 'static':  # Ignore static routes
                    methods = ','.join(sorted(rule.methods))
                    routes.append({
                        'endpoint': rule.endpoint,
                        'methods': methods,
                        'rule': str(rule)
                    })
            return jsonify(routes)

        return app

    elif environment == "prod":
        print("PROD")
    else:
        raise Exception(f"Unsupported environment: {environment}. Check to see if ENV variable is set to DEV or PROD")

