import logging

import storage as storage

from device.models import Device, DeviceAddress
from device.connection import application as connection


LOGGER = logging.getLogger(__name__)


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")

    storage.register(Device)
    storage.register(DeviceAddress)


def model_reset():
    """
    Reset models.
    """
    storage.delete()


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    connection.pre_start()


def start():
    """
    Starts up the device application.
    """
    LOGGER.info("device start")

    connection.start()


def stop():
    """
    Stop the device application.
    """
    LOGGER.info("device stop")

    connection.stop()
