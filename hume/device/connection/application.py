import asyncio
import logging

import storage

from defs import CLI_DEVICE_TRANSPORT, CLI_DEVICE_TRANSPORT_BLE
from util.args import get_arg
from device.models import Device
from device.connection.gci import GCIImplementer
from device.connection.ble.connection import BLEConnection


LOGGER = logging.getLogger(__name__)

_gci_implementer = GCIImplementer()


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    # Select connection type
    if get_arg(CLI_DEVICE_TRANSPORT) == CLI_DEVICE_TRANSPORT_BLE:
        _gci_implementer.instance = BLEConnection(asyncio.get_event_loop())


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
