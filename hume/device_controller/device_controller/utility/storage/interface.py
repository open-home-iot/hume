import logging

from device_controller.utility.storage import data_store


LOGGER = logging.getLogger(__name__)


def initialize(broker, service_name):
    """
    Initialize storage interface function.

    :param broker: HUME broker instance
    :param service_name: name of using service
    """
    LOGGER.info("Initialize storage")

    data_store.initialize(broker, service_name)


def register(model):
    """
    Model registration interface function.

    :param model: model class to register
    """
    LOGGER.info(f"Register model {model}")

    data_store.register(model)


def get_all(cls):
    """
    TODO
    """
    data_store.get_all(cls)


def get_one(cls, key):
    """
    TODO
    """
    data_store.get_one(cls, key)


def set_all(cls, new_data):
    """
    TODO
    """
    data_store.set_all(cls, new_data)


def set_one(cls, instance):
    """
    TODO
    """
    data_store.set_one(cls, instance)
