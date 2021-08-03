import logging

import storage

from device.models import Device
from device.connection.ble.connection import BLEConnection


LOGGER = logging.getLogger(__name__)

_conn: BLEConnection


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    # Prep connection object
    global _conn
    _conn = BLEConnection()


def start():
    """
    Starts up the ble application.
    """
    LOGGER.info("start")

    devices = storage.get_all(Device)

    for device in devices:
        # connect to each device
        pass


def stop():
    """
    Stop the ble application.
    """
    LOGGER.info("stop")
