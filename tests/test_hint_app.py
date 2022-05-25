import unittest

from hume.app.hint.models import (
    HumeUser,
    BrokerCredentials
)


class TestModels(unittest.TestCase):

    def test_hume_user(self):
        hume_user = HumeUser.decode("username", "password")
        self.assertEqual(hume_user.username, "username")
        self.assertEqual(hume_user.password, "password")

    def test_broker_credentials(self):
        broker_credentials = BrokerCredentials.decode("username", "password")
        self.assertEqual(broker_credentials.username, "username")
        self.assertEqual(broker_credentials.password, "password")


class TestAppLCM(unittest.TestCase):
    pass
    # def test_app_lcm(self):
    #     app = HintApp()
