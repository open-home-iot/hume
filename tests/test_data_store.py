import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from util.storage import DataStore  # noqa


class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()
