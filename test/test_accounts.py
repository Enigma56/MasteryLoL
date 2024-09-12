import unittest

from api.account_data import get_riot_puuid, get_summoner_information
# TODO: Consider using pytest for its fixtures instead


class TestAccount(unittest.TestCase):
    def test_get_puuid(self):
        status_code, puuid = get_riot_puuid("Its Just A Prank", "6969")
        self.assertLess(status_code, 400)
        self.assertIsNotNone(puuid)

    def test_get_summoner_information(self):
        _, puuid = get_riot_puuid("Its Just A Prank", "6969")
        status_code, info = get_summoner_information(puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(info)
