# flake8: noqa: E402
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from defs import *
from app.hint.models import (
    HumeUser,
    BrokerCredentials,
    HintAuthentication
)
from app.hint import HintApp
from util.storage import DataStore


class TestModels(unittest.TestCase):

    def test_hume_user(self):
        hume_user = HumeUser.decode("username", "password")
        self.assertEqual(hume_user.username, "username")
        self.assertEqual(hume_user.password, "password")

    def test_broker_credentials(self):
        broker_credentials = BrokerCredentials.decode("username", "password")
        self.assertEqual(broker_credentials.username, "username")
        self.assertEqual(broker_credentials.password, "password")

    def test_hint_auth(self):
        _ = HintAuthentication("...", "...")
        HintAuthentication.decode("..", "..")


class TestAppLCM(unittest.TestCase):

    def test_app_lcm(self):
        cli_args = {
            CLI_BROKER_IP_ADDRESS: "127.0.0.1",
            CLI_BROKER_PORT: 1337,
        }
        storage = DataStore()
        app = HintApp(cli_args, storage)

        app.pre_start()

        with self.assertRaises(TypeError):
            storage.get(HumeUser, "does-not-exist")

        with self.assertRaises(TypeError):
            storage.get(BrokerCredentials, "does-not-exist")

        with self.assertRaises(TypeError):
            storage.get(HintAuthentication, "does-not-exist")
