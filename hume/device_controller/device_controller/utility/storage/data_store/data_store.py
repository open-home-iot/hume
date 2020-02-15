from device_controller.utility.broker import Broker
from device_controller.utility.storage.data_store.local_storage import \
    LocalStorage
from device_controller.utility.storage.data_store.storage_service import \
    StorageService, PERSISTENT_TABLE_ALREADY_DEFINED
from device_controller.utility.storage.definitions import DataModel


def initialize(broker, service_name):
    global _store
    _store = DataStore(broker, service_name)


def register(model):
    assert issubclass(model, DataModel)

    _store.register(model)


def get_all(cls):
    _store.get_all(cls)


def get_one(cls, key):
    _store.get(cls, key)


def set_all(cls, new_data):
    _store.set_all(cls, new_data)


def set_one(cls, instance):
    _store.set(cls, instance)


class DataStore:

    _broker: Broker
    _service_name: str
    _store: dict

    _storage_service: StorageService
    _local_storage: LocalStorage

    def __init__(self, broker, service_name):
        self._broker = broker
        self._service_name = service_name
        self._store = dict()
        self._storage_service = StorageService(self._broker, self._service_name)
        self._local_storage = LocalStorage(self._broker)

    def register(self, model):
        # Registration process:
        # 1. Instantiate model class
        # 2. Define storage space in _store, named same as model class
        # 3. Call storage service to define table(s)
        # 4. TODO Get data from storage if tables were already defined and at
        #    TODO least one field is marked persistent

        model_instance = model()
        print("model _store key: {}".format(model.__name__))
        print("model key field: {}".format(model_instance.key()))
        self.define_storage(model_instance)

    def define_storage(self, model_instance: DataModel):
        # Allocate local storage
        self._store[str(model_instance.__class__.__name__)] = dict()
        print("_store state: {}".format(self._store))

        if model_instance.persistent:
            result = self._storage_service.define_table(model_instance)

            if result == PERSISTENT_TABLE_ALREADY_DEFINED:
                # Get data as we have been alive before
                self._storage_service.get_persistent_data(
                    model_instance.__class__
                )

    def get_all(self, cls):
        pass

    def get_one(self, cls, key):
        self._store.get(cls.__name__).get(key)

    def set_all(self, cls, new_data):
        self._store.get(cls.__name__).update(new_data)

    def set_one(self, cls, instance):
        self._store.get(cls.__name__).update(
            {
                getattr(instance, instance.key()): instance
            }
        )


_store = None
