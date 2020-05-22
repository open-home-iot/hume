import logging

import peewee

from device_controller.util.storage.local import LocalStorage
from device_controller.util.storage.persistent import PersistentStorage


LOGGER = logging.getLogger(__name__)


def start():
    """
    Initialize the data store.
    """
    LOGGER.info("data store start")


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

    def register(self, model):
        """
        Register models with the DataStore.

        :param model: model to register
        """
        # Registration process:
        # 1. Define storage space in _store, named same as model class
        # 2. TODO Get data from storage if persistent
        LOGGER.debug(f"Registering model")

        self.define_storage(model)

        if issubclass(model, peewee.Model):
            # load data into state
            pass

    def define_storage(self, model):
        """
        Allocates storage both locally and towards the database. Tables are
        only created if the model is a descendant of peewee.Model

        :param model: model to define storage for
        """

        if issubclass(model, peewee.Model):
            LOGGER.debug("Defining persistent storage")
            self._persistent_storage.define_storage(model)

        LOGGER.debug("Defining local storage")
        self._local_storage.define_storage(model)


_store = DataStore()
