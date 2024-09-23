from flask import Flask
from dotenv import load_dotenv

from . import db as db_helpers
from .models import db


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

    dbURL = db_helpers.create_db_url()
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

    from . import bp_mastery
    app.register_blueprint(bp_mastery.bp)

    return app
