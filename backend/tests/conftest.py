import pytest
import os
from app import create_app

@pytest.fixture()
def app():
    app = create_app(testing=True)
    app.config.update({
        'TESTING': True,
    })

    yield app

    os.remove("/Users/charlielyster/Developer/Personal/MasteryLoL/backend/tests/testing.db")


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()