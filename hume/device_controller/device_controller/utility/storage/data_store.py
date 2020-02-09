from device_controller.utility.storage.definitions import DataModel


def register(model):
    assert issubclass(model, DataModel)

    _store.register(model)


class DataStore:

    _store: dict

    def __init__(self):
        self._store = dict()

    def register(self, model):
        # Registration process:
        # 1. Instantiate model class
        # 2. Define storage space in _store, named same as model class
        # 3. TODO Call storage to define table(s)
        # 4. TODO Get data from storage if tables were already defined and at
        #    TODO least one field is marked persistent

        model_instance = model()
        print("model key field: {}".format(model_instance.key()))
        print("model _store key: {}".format(model.__name__))
        self._store[str(model.__name__)] = dict()

        print("_store state: {}".format(self._store))


_store = DataStore()
