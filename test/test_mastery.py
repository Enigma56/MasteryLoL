import unittest
from api.mastery import get_mastery_by_puuid
from api.account_data import get_riot_puuid


class TestMastery(unittest.TestCase):
    def test_mastery_by_puuid(self):
        _, puuid = get_riot_puuid("Its Just A Prank", "6969")
        status_code, mastery = get_mastery_by_puuid(puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery)
