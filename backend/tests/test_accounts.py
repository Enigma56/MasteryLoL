# import unittest
# from api.account_data import get_account_information
#
#
# class TestAccount(unittest.TestCase):
#     def setUp(self) -> None:
#         self.name = "Its Just A Prank"
#         self.tag = '6969'
#
#         self.long_name = "Its Just A PrankIts Just A Prank"
#         self.long_tag = '696969'
#
#     def test_get_account_information(self):
#         info, status, _ = get_account_information(self.name, self.tag)
#         self.assertEqual(status, 200)
#         self.assertIsNotNone(info)
#
#     def test_get_account_info_long(self):
#         info, status, _ = get_account_information(self.long_name, self.long_tag)
#         self.assertEqual(status, 400)
#         # self.assertIsNotNone(info)

def test_account(client):
    res = client.get('/account/test')
    assert res.status_code == 200
    assert res.json == {"hello": "world"}