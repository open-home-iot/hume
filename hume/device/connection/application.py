import asyncio
import logging
import signal
import time

import storage

from threading import Thread

from defs import CLI_DEVICE_TRANSPORT, CLI_DEVICE_TRANSPORT_BLE
from util.args import get_arg
from device.models import Device
from device.connection.gci import GCIImplementer
from device.connection.ble.connection import BLEConnection


LOGGER = logging.getLogger(__name__)

event_loop = asyncio.new_event_loop()
event_loop_thread: Thread

_gci_implementer = GCIImplementer()


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")

    # Select connection type
    if get_arg(CLI_DEVICE_TRANSPORT) == CLI_DEVICE_TRANSPORT_BLE:

        def run_event_loop(loop: asyncio.AbstractEventLoop):
            loop.run_forever()

        global event_loop_thread
        event_loop_thread = Thread(target=run_event_loop, args=(event_loop,))
        event_loop_thread.start()

        _gci_implementer.instance = BLEConnection(event_loop)


def start():
    """
    Starts up the ble application.
    """
    LOGGER.info("start")

    devices = storage.get_all(Device)

    for device in devices:
        # connect to each attached device
        if device.attached:
            connected = _gci_implementer.instance.connect(device)

            if not connected:
                LOGGER.error(f"failed to connect device {device.address}")


def stop():
    """
    Stop the ble application.
    """
    LOGGER.info("stop")

    disconnected = _gci_implementer.instance.disconnect_all()

    if not disconnected:
        LOGGER.error("failed to disconnect at least one device")

    event_loop.call_soon_threadsafe(event_loop.stop)
    event_loop_thread.join()
    LOGGER.debug("thread joined, device connection app stopped completely")
