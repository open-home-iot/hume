import logging

import storage as storage

from device.models import Device, DeviceAddress, DeviceHealth
from device.connection import application as connection
from device.heartbeat import application as heartbeat


LOGGER = logging.getLogger(__name__)


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")

    storage.register(Device)
    storage.register(DeviceAddress)
    storage.register(DeviceHealth)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    connection.pre_start()
    heartbeat.pre_start()


def start():
    """
    Starts up the device application.
    """
    LOGGER.info("device start")

    connection.start()
    heartbeat.start()


def stop():
    """
    Stop the device application.
    """
    LOGGER.info("device stop")

    connection.stop()
    heartbeat.stop()
