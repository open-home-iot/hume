import unittest

from util.storage import DataStore


class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()
