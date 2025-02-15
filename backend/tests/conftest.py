import pytest
from app import create_app, db


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////Users/charlielyster/Developer/Personal/MasteryLoL/backend/tests/testing.db',
    })

    with app.app_context():
        #from app.models import TableTest
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="session")
def db_session(app):
    with app.app_context():
        yield db.session


@pytest.fixture(scope="module")
def client(app):
    client = app.test_client()
    client.set_cookie("riot_puuid", "VbFNfWhMl53nxTkB59diHEGRp-SrnZYBviQzroixnCjhX_875Dv7UDEcuBZNOTiAbZ75SldP-XxoLw")
    return client

@pytest.fixture()
def credentials():
    return {"game_name": "Its Just A Prank", "tagline": "6969"}
