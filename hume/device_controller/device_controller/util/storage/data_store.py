import logging
import peewee

from .local import LocalStorage
from .persistent import PersistentStorage
from .persistent.postgres import PersistentModel


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


def save(obj):
    """
    Save an object.

    :param obj: object to save
    """
    LOGGER.info("saving object")

    _store.save(obj)


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

        if issubclass(model, PersistentModel):
            # load data into state
            LOGGER.debug("persistent model, loading DB data")
            pass

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
        LOGGER.debug(f"saving object: {obj}")

        if issubclass(obj.__class__, PersistentModel):
            LOGGER.debug("saving persistently")
            self._persistent_storage.save(obj)

        LOGGER.debug("saving locally")
        self._local_storage.save(obj)


_store = DataStore()
