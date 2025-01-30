import json
import logging
import pytest


def test_mastery_all(client):
    client.set_cookie("riot_puuid", "VbFNfWhMl53nxTkB59diHEGRp-SrnZYBviQzroixnCjhX_875Dv7UDEcuBZNOTiAbZ75SldP-XxoLw")
    res = client.get("/mastery/all")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[0] is not None


def test_mastery_top(client):
    client.set_cookie("riot_puuid", "VbFNfWhMl53nxTkB59diHEGRp-SrnZYBviQzroixnCjhX_875Dv7UDEcuBZNOTiAbZ75SldP-XxoLw")
    res = client.get("/mastery/top")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[1] is not None


def test_mastery_sum(client):
    client.set_cookie("riot_puuid", "VbFNfWhMl53nxTkB59diHEGRp-SrnZYBviQzroixnCjhX_875Dv7UDEcuBZNOTiAbZ75SldP-XxoLw")
    res = client.get("/mastery/sum")
    data = json.loads(res.data)
    logging.debug(data)
    assert res.status_code == 200
    assert data[1] is not None
