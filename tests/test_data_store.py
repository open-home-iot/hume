# flake8: noqa: E402
from __future__ import annotations

import random
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from util.storage import DataStore, Model, ModelError, SINGLETON


class TestModel(Model):
    persistent = True
    key = "name"

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def decode(cls, name: str = None, age: str = None) -> TestModel:
        return cls(name, int(age))


class DataTypeModel(Model):
    persistent = True
    key = "string"

    def __init__(self,
                 string: str,
                 boolean: bool,
                 integer: int,
                 floating: float):
        self.string = string
        self.boolean = boolean
        self.integer = integer
        self.floating = floating

    @classmethod
    def decode(cls,
               string: str,
               boolean: bool,
               integer: int,
               floating: float) -> DataTypeModel:
        return cls(string, bool(int(boolean)), int(integer), float(floating))


class OptionalModel(Model):
    persistent = True
    key = "origin"

    def __init__(self,
                 origin: str,
                 species: str,
                 nickname: str = None,
                 exists: bool = None):
        self.origin = origin
        self.species = species
        self.nickname = nickname
        self.exists = exists

    @classmethod
    def decode(cls,
               origin: str = None,
               species: str = None,
               nickname: str = None,
               exists: str = None) -> OptionalModel:
        return cls(origin,
                   species,
                   nickname=nickname,
                   exists=bool(int(exists)))


class LocalModel(Model):
    key = "site"

    def __init__(self, site: str, workers: int):
        self.site = site
        self.workers = workers

    @classmethod
    def decode(cls) -> None:
        pass


class SingletonModel(Model):
    persistent = True
    key = SINGLETON

    def __init__(self, count: int, factor: int):
        self.count = count
        self.factor = factor

    @classmethod
    def decode(cls,
               count: str = None,
               factor: str = None) -> SingletonModel:
        return cls(int(count), int(factor))


class TestModels(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()

    def tearDown(self):
        self.data_store.delete_all()

    def test_basic_model(self):
        """Verify basic model registration and set/get works."""
        self.data_store.register(TestModel)

        model_instance = TestModel("Moens", 30)
        self.data_store.set(model_instance)
        gotten_model_instance = self.data_store.get(TestModel, "Moens")

        self.assertEqual(gotten_model_instance.name, model_instance.name)

    def test_model_instance_cannot_be_set_before_register(self):
        """
        Verify model instance cannot be set before the model is registered and
        allocated space for.
        """
        model_instance = TestModel("Moens", 30)
        with self.assertRaises(ModelError):
            self.data_store.set(model_instance)

    def test_model_instance_cannot_be_gotten_before_register(self):
        """
        Verify model instance cannot be gotten before the model is registered
        and allocated space for.
        """
        with self.assertRaises(ModelError):
            self.data_store.get(TestModel, "Moens")

    def test_model_instance_cannot_be_deleted_before_register(self):
        """
        Verify model instance cannot be deleted before the model is registered
        and allocated space for.
        """
        with self.assertRaises(ModelError):
            model_instance = TestModel("Moens", 2)
            self.data_store.delete(model_instance)

    def test_get_all_fails_prior_to_registration(self):
        """Verify get_all fails before a model is registered."""
        with self.assertRaises(ModelError):
            self.data_store.get_all(TestModel)

    def test_double_registration_raises_model_error(self):
        """Verify get_all fails before a model is registered."""
        with self.assertRaises(ModelError):
            self.data_store.register(TestModel)
            self.data_store.register(TestModel)

    def test_gotten_model_instance_does_not_change_original(self):
        """
        Verify that when a model instance is gotten changing its fields does
        not alter the original model instance.
        """
        self.data_store.register(TestModel)

        model_instance = TestModel("Moens", 30)
        self.data_store.set(model_instance)
        gotten_model_instance = self.data_store.get(TestModel, "Moens")

        self.assertEqual(model_instance.name, gotten_model_instance.name)
        gotten_model_instance.name = "new_name"
        # original instance name field is still set to 'name'
        self.assertEqual(model_instance.name, "Moens")

    def test_changing_object_post_set_does_not_alter_set_instance(self):
        """
        Verify changing an instance after setting it in the data store does
        not change the stored instance.
        """
        self.data_store.register(TestModel)
        model_instance = TestModel("Moens", 30)
        self.data_store.set(model_instance)

        # now change something and fetch the instance to verify it has not been
        # impacted
        model_instance.name = "Sarah"
        gotten_model_instance = self.data_store.get(TestModel, "Moens")
        self.assertEqual(gotten_model_instance.name, "Moens")

    def test_get_all(self):
        """Verify get_all gets all model instances."""
        self.data_store.register(TestModel)
        for i in range(0, 10):
            self.data_store.set(TestModel(str(i), i+10))

        model_instances = self.data_store.get_all(TestModel)
        self.assertEqual(len(model_instances), 10)


class TestSingeltonModels(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()

    def tearDown(self):
        self.data_store.delete_all()

    def test_singleton_model(self):
        """
        Verify register, set, and get of singleton works.
        """
        self.data_store.register(SingletonModel)
        singleton = SingletonModel(2, 3)
        self.data_store.set(singleton)
        gotten_singleton = self.data_store.get(SingletonModel, SINGLETON)

        self.assertEqual(gotten_singleton.count, 2)
        self.assertEqual(gotten_singleton.factor, 3)

    def test_second_singleton_set_overrides_old_instance(self):
        """
        Verify a second call to set for a singleton model will override the
        old instance.
        """
        self.data_store.register(SingletonModel)
        singleton = SingletonModel(2, 3)
        self.data_store.set(singleton)
        gotten_singleton = self.data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(gotten_singleton.count, 2)
        self.assertEqual(gotten_singleton.factor, 3)

        new_singleton = SingletonModel(5, 6)
        self.data_store.set(new_singleton)
        gotten_singleton = self.data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(gotten_singleton.count, 5)
        self.assertEqual(gotten_singleton.factor, 6)

    def test_changing_singleton_post_set_does_not_alter_set_instance(self):
        """
        Verify changing an instance after setting it in the data store does
        not change the stored instance.
        """
        self.data_store.register(SingletonModel)
        singleton = SingletonModel(1, 2)
        self.data_store.set(singleton)

        # now change something and fetch the instance to verify it has not been
        # impacted
        singleton.count = 40
        gotten_model_instance = self.data_store.get(
            SingletonModel, SINGLETON)
        self.assertEqual(gotten_model_instance.count, 1)


class TestPersistence(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStore()

    def tearDown(self):
        self.data_store.delete_all()

    def test_model_persistence(self):
        """Base test for model persistence."""
        names = ["0", "1", "2", "3", "4"]
        self.data_store.register(TestModel)
        for name in names:
            model_instance = TestModel(name, random.randint(0, 100))
            self.data_store.set(model_instance)

        new_data_store = DataStore()
        new_data_store.register(TestModel)

        for name in names:
            # will raise KeyError if not exists and fail the test case.
            _ = new_data_store.get(TestModel, name)

    def test_optional_model_persistence(self):
        """
        Verify a model with optional fields can choose to include or exclude
        those optional fields.
        """
        self.data_store.register(OptionalModel)
        # No optional field set
        self.data_store.set(OptionalModel("Sweden", "Finch", exists=False))

        model_instance = self.data_store.get(OptionalModel, "Sweden")
        self.assertEqual(model_instance.origin, "Sweden")
        self.assertEqual(model_instance.species, "Finch")
        self.assertEqual(model_instance.nickname, None)
        self.assertEqual(model_instance.exists, False)

        new_data_store = DataStore()
        new_data_store.register(OptionalModel)

        model_instance = new_data_store.get(OptionalModel, "Sweden")
        self.assertEqual(model_instance.origin, "Sweden")
        self.assertEqual(model_instance.species, "Finch")
        self.assertEqual(model_instance.nickname, None)
        self.assertEqual(model_instance.exists, False)

    def test_singleton_persistence(self):
        """
        Verify a stored is gotten when its model is registered with the data
        store.
        """
        self.data_store.register(SingletonModel)
        self.data_store.set(SingletonModel(1, 2))

        new_data_store = DataStore()
        new_data_store.register(SingletonModel)

        # no model error should be raised.
        singleton_instance = new_data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton_instance.count, 1)
        self.assertEqual(singleton_instance.factor, 2)

    def test_different_data_types(self):
        """
        Verify that different data types can be stored and decoded correctly.
        """
        self.data_store.register(DataTypeModel)
        self.data_store.set(DataTypeModel("str", True, 666, 62.5))

        # re-init to force reading from Redis
        new_data_store = DataStore()
        new_data_store.register(DataTypeModel)

        # no model error should be raised.
        model_instance = new_data_store.get(DataTypeModel, "str")
        self.assertEqual(model_instance.string, "str")
        self.assertEqual(model_instance.boolean, True)
        self.assertEqual(model_instance.integer, 666)
        self.assertEqual(model_instance.floating, 62.5)

        # re-set some values and check again
        model_instance.boolean = False
        model_instance.integer = 1020
        model_instance.floating = 100.41
        new_data_store.set(model_instance)

        # re-init to force reading from Redis
        new_data_store = DataStore()
        new_data_store.register(DataTypeModel)

        # no model error should be raised.
        model_instance = new_data_store.get(DataTypeModel, "str")
        self.assertEqual(model_instance.string, "str")
        self.assertEqual(model_instance.boolean, False)
        self.assertEqual(model_instance.integer, 1020)
        self.assertEqual(model_instance.floating, 100.41)

    def test_delete_persistent_model_instance(self):
        """
        Verify delete removes a non-singleton from persistent storage.
        """
        self.data_store.register(TestModel)
        self.data_store.set(TestModel("Moens", 2))
        model_instance = self.data_store.get(TestModel, "Moens")
        self.assertEqual(model_instance.name, "Moens")
        self.assertEqual(model_instance.age, 2)

        self.data_store.delete(model_instance)
        with self.assertRaises(KeyError):
            self.data_store.get(TestModel, "Moens")

        new_data_store = DataStore()
        # will fetch from Redis again, now verify that the single can't be
        # gotten
        new_data_store.register(TestModel)

        # should still yield None
        with self.assertRaises(KeyError):
            new_data_store.get(TestModel, "Moens")

    def test_delete_persistent_singleton(self):
        """
        Verify delete removes a singleton instance from persistent storage.
        """
        self.data_store.register(SingletonModel)
        self.data_store.set(SingletonModel(1, 2))
        singleton_instance = self.data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton_instance.count, 1)
        self.assertEqual(singleton_instance.factor, 2)

        self.data_store.delete(singleton_instance)
        singleton_instance = self.data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton_instance, None)

        new_data_store = DataStore()
        # will fetch from Redis again, now verify that the single can't be
        # gotten
        new_data_store.register(SingletonModel)

        # should still yield None
        singleton_instance = new_data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton_instance, None)

    def test_delete_all(self):
        """
        Verify the delete_all function works and that it flushes all data,
        both persistent and local.
        """
        test_model_range = range(0, 50)
        local_model_range = range(0, 100)

        self.data_store.register(TestModel)
        for i in test_model_range:
            self.data_store.set(TestModel(str(i), i))

        self.data_store.register(SingletonModel)
        self.data_store.set(SingletonModel(12, 10))

        self.data_store.register(LocalModel)
        for i in local_model_range:
            self.data_store.set(LocalModel(str(i), i*10))

        self.data_store.delete_all()

        for i in test_model_range:
            with self.assertRaises(KeyError):
                self.data_store.get(TestModel, str(i))

        singleton = self.data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton, None)

        for i in local_model_range:
            with self.assertRaises(KeyError):
                self.data_store.get(LocalModel, str(i))

        # Attempt Redis re-fetch and check that everything is REALLY gone
        new_data_store = DataStore()
        new_data_store.register(SingletonModel)
        new_data_store.register(TestModel)

        for i in test_model_range:
            with self.assertRaises(KeyError):
                new_data_store.get(TestModel, str(i))

        singleton = new_data_store.get(SingletonModel, SINGLETON)
        self.assertEqual(singleton, None)

    def test_delete_all_from_model(self):
        test_model_range = range(0, 50)
        local_model_range = range(0, 100)

        self.data_store.register(TestModel)
        for i in test_model_range:
            self.data_store.set(TestModel(str(i), i))

        self.data_store.register(SingletonModel)
        self.data_store.set(SingletonModel(12, 10))

        self.data_store.register(LocalModel)
        for i in local_model_range:
            self.data_store.set(LocalModel(str(i), i * 10))

        self.data_store.delete_all(model=TestModel)

        for i in test_model_range:
            # still raises exceptions since the model data was cleared
            with self.assertRaises(KeyError):
                self.data_store.get(TestModel, str(i))

        singleton = self.data_store.get(SingletonModel, SINGLETON)
        self.assertNotEqual(singleton, None)

        for i in local_model_range:
            # no exceptions shall be raised.
            self.data_store.get(LocalModel, str(i))

        # Attempt Redis re-fetch and check that everything is REALLY gone
        new_data_store = DataStore()
        new_data_store.register(SingletonModel)
        new_data_store.register(TestModel)

        for i in test_model_range:
            with self.assertRaises(KeyError):
                new_data_store.get(TestModel, str(i))

        singleton = new_data_store.get(SingletonModel, SINGLETON)
        self.assertNotEqual(singleton, None)
