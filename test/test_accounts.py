import unittest

from api.account_data import get_account
# TODO: Consider using pytest for its fixtures instead


class TestAccount(unittest.TestCase):
    def test_get_account(self):
        status_code, _ = get_account("Its Just A Prank", "6969")
        self.assertLess(status_code, 400)
        # self.assertIsNotNone(account_info)
