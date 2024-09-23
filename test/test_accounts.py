import unittest

from api.account_data import get_riot_puuid, get_summoner_information, get_account_information


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        _, account_info = get_account_information("Its Just A Prank", "6969")
        self.puuid = account_info

    @unittest.skip("Not needed")
    def test_get_puuid(self):
        status_code, puuid = get_riot_puuid("Its Just A Prank", "6969")
        self.assertLess(status_code, 400)
        self.assertIsNotNone(puuid)

    def test_get_summoner_information(self):
        status_code, info = get_summoner_information(self.puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(info)
