import unittest
from api.player import determine_owned_champions
from api.mastery import get_all_mastery_by_puuid
from api.account_data import get_account_information


class TestPlayer(unittest.TestCase):
    def test_owned_champions(self):
        account_info = get_account_information("Its Just A Prank", "6969")
        puuid = account_info['puuid']

        _, all_mastery = get_all_mastery_by_puuid(puuid)
        unowned_champs = determine_owned_champions(puuid, all_mastery)

        print(unowned_champs)
