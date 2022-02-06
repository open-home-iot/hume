import logging

from defs import CLI_PSQL_USER, CLI_PSQL_PASSWORD
from util.storage.local_storage import LocalStorage
from util.storage.persistent_storage import PersistentModel, PersistentStorage


LOGGER = logging.getLogger(__name__)


class DataStore:
    """
    Class that handles storage for the HUME services. It has both local and
    persistent storage.
    """

    def __init__(self, cli_args: dict):
        self._persistent_storage: PersistentStorage = PersistentStorage(
            cli_args[CLI_PSQL_USER], cli_args[CLI_PSQL_PASSWORD]
        )
        self._local_storage: LocalStorage = LocalStorage()

    def start(self):
        """Start up the datastore, will lead to connect to Postgres."""
        LOGGER.info("starting DataStore")
        self._persistent_storage.start()

    def stop(self):
        """
        Gracefully shut down the data store, terminating the PSQL
        connection.
        """
        LOGGER.info("stopping DataStore")
        self._persistent_storage.stop()

    def register(self, model):
        """
        Register models with the DataStore.

        :param model: model to register
        """
        # Registration process:
        # 1. Define storage space in _store, named same as model class
        # 2. Get data from storage if persistent
        LOGGER.info(f"registering model: {model.__name__}")

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
            self._persistent_storage.define_storage(model)

        self._local_storage.define_storage(model)

    def set(self, obj):
        """
        Set an object.

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
