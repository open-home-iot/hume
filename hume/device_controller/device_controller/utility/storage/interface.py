from device_controller.utility.storage import persistent, local, data_store


def initialize(broker):
    persistent.initialize(broker)
    local.initialize(broker)


def register(model):
    print("storage interface register model: {}".format(model))
    data_store.register(model)
