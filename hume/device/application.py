import logging

import storage as storage

from util import get_arg
from defs import CLI_DEVICE_TRANSPORT, CLI_DEVICE_TRANSPORT_BLE
from device.models import Device
from device.connection.ble import application as ble


LOGGER = logging.getLogger(__name__)

SUB_APPLICATIONS = []


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")
    storage.register(Device)


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    transport = get_arg(CLI_DEVICE_TRANSPORT)
    if transport == CLI_DEVICE_TRANSPORT_BLE:
        SUB_APPLICATIONS.append(ble)


def start():
    """
    Starts up the device application.
    """
    LOGGER.info("device start")

    for sub_app in SUB_APPLICATIONS:
        sub_app.pre_start()

    for sub_app in SUB_APPLICATIONS:
        sub_app.start()


def stop():
    """
    Stop the device application.
    """
    LOGGER.info("device stop")

    for sub_app in SUB_APPLICATIONS:
        sub_app.stop()
