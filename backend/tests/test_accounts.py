import json

from app.models import TableTest

print("Hello")


class TestDummy:
    def test_db_post_account_dummy(self, client):
        res = client.get('/account/test')
        assert res.status_code == 200
        assert res.json == {"hello": "world"}

    def test_db_get_account(self, db_session):
        profile = db_session.get(TableTest, 1)
        assert profile.tag == "6969"
        assert profile.name == "its just a prank"

class TestAccounts:
    def test_get_account_precookie(self, client, credentials):
        res = client.get(f'/account/user?name={credentials["game_name"]}&tag={credentials["tagline"]}')
        assert res.status_code >= 400
    
    def test_db_post_account(self, client, credentials):
        res = client.post(f"/account/user?name={credentials["game_name"]}&tag={credentials["tagline"]}")
        assert res.status_code == 201

    def test_post_account_exists(self, client, credentials):
        res = client.post(f"/account/user?name={credentials["game_name"]}&tag={credentials["tagline"]}")
        assert res.status_code == 400

    def test_get_account_normal(self, client, credentials):
        res = client.get(f'/account/user?name={credentials["game_name"]}&tag={credentials["tagline"]}')
        data = json.loads(res.data)
        assert res.status_code == 200
        assert data is not None

    def test_get_account_empty(self, client):
        username = ""
        tagline = ""

        res = client.post(f'/account/user?name={username}&tag={tagline}')
        data = json.loads(res.data)
        assert res.status_code >= 400
        assert data == {}

    def test_get_account_long(self, client):
        username = "its just a prankits"
        tagline = "696969"

        res = client.post(f'/account/user?name={username}&tag={tagline}')
        data = json.loads(res.data)
        assert res.status_code >= 400
        assert data == {}

    def test_get_account_notfound(self, client):
        username = "its just a pra"
        tagline = "696"

        res = client.post(f'/account/user?name={username}&tag={tagline}')
        data = json.loads(res.data)
        assert res.status_code >= 400
        assert data == {}
