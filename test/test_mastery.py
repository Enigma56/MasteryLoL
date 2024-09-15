import unittest
import api.mastery as mastery
from api.account_data import get_riot_puuid


class TestMastery(unittest.TestCase):
    def test_all_mastery_by_puuid(self):
        _, puuid = get_riot_puuid("Its Just A Prank", "6969")
        status_code, mastery_info = mastery.get_all_mastery_by_puuid(puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)

    def test_top_mastery_by_puuid(self):
        _, puuid = get_riot_puuid("Its Just A Prank", "6969")
        status_code, mastery_info = mastery.get_top_mastery_by_puuid(puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)

    def test_sum_mastery_by_puuid(self):
        _, puuid = get_riot_puuid("Its Just A Prank", "6969")
        status_code, mastery_info = mastery.get_sum_mastery_by_puuid(puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)
