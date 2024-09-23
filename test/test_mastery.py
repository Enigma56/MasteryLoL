import unittest
import api.mastery as mastery
from api.account_data import get_riot_puuid


class TestMastery(unittest.TestCase):
    def setUp(self) -> None:
        _, account_info = get_riot_puuid("Its Just A Prank", "6969")
        self.puuid = account_info['puuid']

    def test_all_mastery_by_puuid(self):
        status_code, mastery_info = mastery.get_all_mastery_by_puuid(self.puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)

    def test_top_mastery_by_puuid(self):
        status_code, mastery_info = mastery.get_top_mastery_by_puuid(self.puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)

    def test_sum_mastery_by_puuid(self):
        status_code, mastery_info = mastery.get_sum_mastery_by_puuid(self.puuid)
        self.assertLess(status_code, 400)
        self.assertIsNotNone(mastery_info)
