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
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

    #os.remove("/Users/charlielyster/Developer/Personal/MasteryLoL/backend/tests/testing.db")


@pytest.fixture(scope="session")
def db_session(app):
    with app.app_context():
        yield db.session

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()