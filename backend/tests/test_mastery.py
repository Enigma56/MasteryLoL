import json
import logging
import pytest


def test_mastery_all(client):
    res = client.get("/mastery/all")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[0] is not None


def test_mastery_top(client):
    res = client.get("/mastery/top")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[1] is not None


def test_mastery_sum(client):
    res = client.get("/mastery/sum")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[1] is not None
