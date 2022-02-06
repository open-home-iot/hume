# flake8: noqa: E402
import unittest
import sys
import os

import peewee

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from defs import CLI_PSQL_PASSWORD, CLI_PSQL_USER
from util.storage import DataStore, PersistentModel, SINGLETON


class TestModel(PersistentModel):
    name = peewee.CharField(unique=True)
    length = peewee.IntegerField()

    @staticmethod
    def local_key_field():
        return "name"


class TestModelSingleton(PersistentModel):
    some_key = peewee.CharField(unique=True)

    @staticmethod
    def local_key_field():
        return SINGLETON


class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore({
            CLI_PSQL_USER: "hume",
            CLI_PSQL_PASSWORD: "password"
        })
        self.data_store.start()

    def tearDown(self):
        print("running teardown")
        self.data_store.delete_all()
        self.data_store.stop()

    @classmethod
    def tearDownClass(cls):
        print("running tear down class")
        data_store = DataStore({
            CLI_PSQL_USER: "hume",
            CLI_PSQL_PASSWORD: "password"
        })
        data_store.start()
        data_store.register(TestModel)
        data_store.register(TestModelSingleton)
        data_store.delete_all()

    def test_define_model(self):
        """Verify model definitions work"""
        name = "percius"

        self.data_store.register(TestModel)
        entries = self.data_store.get_all(TestModel)

        # Verify 0 entries post definition
        self.assertEqual(len(entries), 0)

        self.data_store.set(TestModel(name=name, length=185))
        percius = self.data_store.get(TestModel, name)

        self.assertEqual(percius.name, name)
        self.assertEqual(percius.length, 185)

    def test_singleton(self):
        """Verify singletons are in fact singletons."""
        some_key = "blablabla"

        self.data_store.register(TestModelSingleton)
        entries = self.data_store.get_all(TestModelSingleton)

        self.assertEqual(entries, None)

        self.data_store.set(TestModelSingleton(some_key=some_key))
        singleton = self.data_store.get(TestModelSingleton, None)

        self.assertEqual(singleton.some_key, some_key)

        updated_key = "blebleble"
        self.data_store.set(TestModelSingleton(some_key=updated_key))
        singleton = self.data_store.get(TestModelSingleton, None)

        self.assertEqual(singleton.some_key, updated_key)

    def test_multiple_instances_in_table(self):
        """Verify multiple model instances can exist."""
        self.data_store.register(TestModel)
        self.data_store.set(TestModel(name="name1", length=185))
        self.data_store.set(TestModel(name="name2", length=185))
        self.data_store.set(TestModel(name="name3", length=185))

        [_1, _2, _3] = self.data_store.get_all(TestModel)

    def test_overwrite(self):
        """Verify a model instance can't be overwritten using 'set'."""
        self.data_store.register(TestModel)
        self.data_store.set(TestModel(name="name1", length=185))

