import logging

import peewee

from device_controller.utility.broker import Broker

from device_controller.utility.storage.local import LocalStorage
from device_controller.utility.storage.persistent import PersistentStorage


LOGGER = logging.getLogger(__name__)


def initialize(broker, service_name):
    """
    Initialize the data store with a HUME broker instance and a service name
    to allocate for the user of the data store.

    :param broker: HUME broker instance
    :param service_name: service name of the data store user
    """
    LOGGER.info("Initialize data store")

    global _store
    _store = DataStore(broker, service_name)


def register(models):
    """
    Interface function to register a new data model

    :param models: .
    """
    LOGGER.info(f"Registering models {models}")

    _store.register(models)


def set_obj(obj):
    """
    Sets input object to storage. Input object must be a registered model
    instance or this operation will fail.

    :param obj: model instance
    """
    LOGGER.info(f"Setting object: {obj}")

    _store.set_obj(obj)


class DataStore:
    """
    Class that handles storage for the HUME services. It has both local and
    persistent storage.
    """

    def __init__(self, broker, service_name):
        """
        :param broker: HUME broker instance
        :param service_name: name of the service using the HUME storage
        """
        LOGGER.debug("DataStore __init__")

        self._broker: Broker = broker
        self._service_name: str = service_name

        self._persistent_storage: PersistentStorage = PersistentStorage()
        self._local_storage: LocalStorage = LocalStorage()

    def register(self, models):
        """
        Register models with the DataStore.

        :param models: .
        """
        # Registration process:
        # 1. Define storage space in _store, named same as model class
        # 2. TODO Get data from storage if persistent
        LOGGER.debug(f"Registering models")

        self.define_storage(models)

    def define_storage(self, models):
        """
        Allocates storage both locally and towards the database. Tables are
        only created if the model is a descendant of peewee.Model

        :param models: .
        """

        p_models = []
        l_models = []
        for model in models:
            if issubclass(model, peewee.Model):
                p_models.append(model)
            else:
                l_models.append(model)

        LOGGER.debug("Defining persistent storage")
        self._persistent_storage.define_storage(p_models)
        LOGGER.debug("Defining local storage")
        self._local_storage.define_storage(l_models)

    def set_obj(self, obj):
        """
        Checks if the object to be set it persistent or local and sets its
        contents to the appropriate store.

        :param obj:
        """
        LOGGER.debug("Setting object")

        if issubclass(obj.__class__, peewee.Model):
            self._persistent_storage.set_obj(obj)
        else:
            self._local_storage.set_obj(obj)


_store = None
