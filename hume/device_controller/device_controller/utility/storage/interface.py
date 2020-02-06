from device_controller.utility.storage import persistent, local


def initialize(broker):
    persistent.initialize(broker)
    local.initialize(broker)


def get(name, id):
    ...


def set(name, id, new):
    ...


def notify(name, callback):
    ...
