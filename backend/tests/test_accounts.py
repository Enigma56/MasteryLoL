import json
import logging

import pytest

from app.models import TableTest

print("Hello")

def test_account(client):
    res = client.get('/account/test')
    assert res.status_code == 200
    assert res.json == {"hello": "world"}

def test_account_query(db_session):
    result = db_session.get(TableTest, 1)
    assert result is not None

@pytest.mark.skip()
def test_account_query_normal(client):
    username = "its just a prank"
    tagline = "6969"

    res = client.get(f'/account/user?name={username}&tag={tagline}')
    data = json.loads(res.data)
    assert res.status_code == 200
    assert data is not None

@pytest.mark.skip()
def test_account_query_none(client):
    username = ""
    tagline = ""

    res = client.get(f'/account/user?name={username}&tag={tagline}')
    data = json.loads(res.data)
    assert res.status_code == 400
    assert "error" in data

@pytest.mark.skip()
def test_account_query_long(client):
    username = "its just a prankits"
    tagline = "696969"

    res = client.get(f'/account/user?name={username}&tag={tagline}')
    data = json.loads(res.data)
    assert res.status_code == 400
    assert "error" in data

@pytest.mark.skip()
def test_account_query_notfound(client):
    username = "its just a pra"
    tagline = "696"

    res = client.get(f'/account/user?name={username}&tag={tagline}')
    data = json.loads(res.data)
    assert res.status_code == 404
    assert "error" in data
