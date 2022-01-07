import logging

from .local import LocalStorage
from .persistent import PersistentStorage
from .persistent.postgres import PersistentModel


LOGGER = logging.getLogger(__name__)


def start():
    """
    Initialize the data store.
    """
    LOGGER.info("data store start")
    _store.start()


def stop():
    """
    Stop the data store.
    """
    LOGGER.info("data store stop")


def register(model):
    """
    Interface function to register a new data model.

    :param model: model to register
    """
    LOGGER.info(f"Registering model {model}")

    _store.register(model)


def save(obj):
    """
    Save an object.

    :param obj: object to save
    """
    LOGGER.info("saving object")

    _store.save(obj)


def get(cls, key, **kwargs):
    """
    Get a single object matching the provided key. Will always check local
    storage only as it should be up to date with persistent storage.

    :param cls: class
    :param key: key
    :return: class object matching key
    """
    LOGGER.info("getting object")
    return _store.get(cls, key, **kwargs)


def get_all(cls):
    """
    Get all object for the provided model class.

    :param cls:
    :return:
    """
    LOGGER.info("getting all objects")
    return _store.get_all(cls)


def delete(obj):
    """
    Removes the object from both local and persistent storage.

    :param obj:
    :return:
    """
    if obj is None:
        LOGGER.warning("tried to delete None")
        return

    LOGGER.info("deleting object")
    _store.delete(obj)


def delete_all():
    """
    Delete all data.
    """
    LOGGER.info("deleting all data")
    _store.delete_all()


class DataStore:
    """
    Class that handles storage for the HUME services. It has both local and
    persistent storage.
    """

    def __init__(self):
        """
        """
        LOGGER.debug("DataStore __init__")

        self._persistent_storage: PersistentStorage = PersistentStorage()
        self._local_storage: LocalStorage = LocalStorage()

    def start(self):
        """Start up the datastore, will lead to connect to Postgres."""
        LOGGER.info("starting DataStore")

        self._persistent_storage.start()

    def register(self, model):
        """
        Register models with the DataStore.

        :param model: model to register
        """
        # Registration process:
        # 1. Define storage space in _store, named same as model class
        # 2. Get data from storage if persistent
        LOGGER.debug("Registering model")

        self.define_storage(model)

        if issubclass(model, PersistentModel):
            # load data into state
            model_data = self._persistent_storage.get_all(model)
            self._local_storage.save_all(model_data)

    def define_storage(self, model):
        """
        Allocates storage both locally and towards the database. Tables are
        only created if the model is a descendant of peewee.Model

        :param model: model to define storage for
        """

        if issubclass(model, PersistentModel):
            LOGGER.debug("Defining persistent storage")
            self._persistent_storage.define_storage(model)

        LOGGER.debug("Defining local storage")
        self._local_storage.define_storage(model)

    def save(self, obj):
        """
        Save an object.

        :param obj: object to save
        """

        if issubclass(obj.__class__, PersistentModel):
            LOGGER.debug("saving persistently")
            self._persistent_storage.save(obj)

        LOGGER.debug("saving locally")
        self._local_storage.save(obj)

    def get(self, cls, key, **kwargs):
        """
        Get a single object matching the provided key. Will always check local
        storage only as it should be up-to-date with persistent storage.

        :param cls: class
        :param key: key
        :return: class object matching key
        """
        return self._local_storage.get(cls, key, **kwargs)

    def get_all(self, cls):
        """
        Get all object of the provided class.

        :param cls:
        :return:
        """
        return self._local_storage.get_all(cls)

    def delete(self, obj):
        """
        Removes the object from both local and persistent storage.

        :param obj:
        """
        if issubclass(obj.__class__, PersistentModel):
            self._persistent_storage.delete(obj)

        self._local_storage.delete(obj)

    def delete_all(self):
        """
        Clears data from all registered tables.
        """
        self._local_storage.delete_all()
        self._persistent_storage.delete_all()


_store = DataStore()
