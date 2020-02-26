import logging

from device_controller.utility.broker import Broker
from device_controller.utility.storage.data_store.local_storage import \
    LocalStorage
from device_controller.utility.storage.data_store.storage_service import \
    StorageService, PERSISTENT_TABLE_ALREADY_DEFINED
from device_controller.utility.storage.definitions import DataModel


LOGGER = logging.getLogger(__name__)


def initialize(broker, service_name):
    """
    Initialize the data store with a HUME broker instance and a service name
    to allocate for the user of the data store.

    :param broker: HUME broker instance
    :param service_name: service name of the data store user
    """
    LOGGER.debug("Initialize data store")

    global _store
    _store = DataStore(broker, service_name)


def register(model):
    """
    Interface function to register a new data model

    :param model: data model, descendant of DataModel
    """
    LOGGER.debug("Register model")

    assert issubclass(model, DataModel)

    _store.register(model)


def get_all(cls):
    """
    TODO
    """
    _store.get_all(cls)


def get_one(cls, key):
    """
    TODO
    """
    _store.get(cls, key)


def set_all(cls, new_data):
    """
    TODO
    """
    _store.set_all(cls, new_data)


def set_one(cls, instance):
    """
    TODO
    """
    _store.set(cls, instance)


class DataStore:
    """
    Class that handles storage for the HUME services. It has both local and
    persistent storage. Storage will be allocated using the register function,
    each data model can mark if the model shall be persistent or local. Local
    storage will not allocate space in the storage service.
    """

    def __init__(self, broker, service_name):
        """
        :param broker: HUME broker instance
        :param service_name: name of the service using the HUME storage
        """
        LOGGER.debug("DataStore __init__")

        self._broker: Broker = broker
        self._service_name: str = service_name
        self._store: dict = dict()
        self._storage_service: StorageService = \
            StorageService(self._broker, self._service_name)
        self._local_storage: LocalStorage = LocalStorage(self._broker)

    def register(self, model):
        """
        Register a data model with the DataStore. Will allocate space in the
        storage service if model is marked as persistent.

        :param model: data model, descendant of DataModel
        """
        # Registration process:
        # 1. Instantiate model class, but WHY!?
        # 2. Define storage space in _store, named same as model class
        # 3. Call storage service to define table(s)
        # 4. TODO Get data from storage if tables were already defined and at
        #    TODO least one field is marked persistent
        LOGGER.debug(f"Register model")

        model_instance = model()
        self.define_storage(model_instance)

    def define_storage(self, model_instance: DataModel):
        """
        Allocates storage both locally and towards the storage service, but
        only if the model is marked persistent.

        :param model_instance: instantiated data model
        """
        LOGGER.debug("Defining local storage")
        self._store[str(model_instance.__class__.__name__)] = dict()

        if model_instance.persistent:
            LOGGER.debug("Defining persistent storage")
            result = self._storage_service.define_table(model_instance)

            if result == PERSISTENT_TABLE_ALREADY_DEFINED:
                LOGGER.debug("Table already defined, get persistent data from"
                             "storage service")
                # Get data as we have been alive before
                self._storage_service.get_persistent_data(
                    model_instance.__class__
                )

    def get_all(self, cls):
        """
        TODO
        """
        self._store.get(cls.__name__)

    def get_one(self, cls, key):
        """
        TODO
        """
        self._store.get(cls.__name__).get(key)

    def set_all(self, cls, new_data):
        """
        TODO
        """
        self._store.get(cls.__name__).update(new_data)

    def set_one(self, cls, instance):
        """
        TODO
        """
        self._store.get(cls.__name__).update(
            {
                getattr(instance, instance.key()): instance
            }
        )


_store = None
