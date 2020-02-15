from device_controller.utility.storage import data_store


def initialize(broker, service_name):
    data_store.initialize(broker, service_name)


def register(model):
    print("storage interface register model: {}".format(model))
    data_store.register(model)


def get_all(cls):
    data_store.get_all(cls)


def get(cls, key):
    data_store.get(cls, key)
