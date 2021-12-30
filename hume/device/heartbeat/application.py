import logging
import threading

from defs import DeviceRequest
from device import connection
from device.connection.gci import GCI

LOGGER = logging.getLogger(__name__)

_t: threading.Timer


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """Starts up the application."""
    LOGGER.info("start")

    global _t
    _t = threading.Timer(10.0, _heartbeat)
    _t.start()


def stop():
    """Stop the application."""
    LOGGER.info("stop")

    _t.cancel()


def _heartbeat():
    """Gets a heartbeat from all currently connected devices."""
    LOGGER.info("getting heartbeat from all connected devices")

    # Restart timer
    global _t
    _t = threading.Timer(10.0, _heartbeat)
    _t.start()

    connection.for_each(
        lambda device:
            connection.send(GCI.Message(f"{DeviceRequest.HEARTBEAT}"), device)
    )
