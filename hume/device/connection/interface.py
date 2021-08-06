"""
Designed as glue between the GCI implementer and callers, since callers are
calling discovery from a synchronous context.
"""


import logging

from device.connection.application import _gci_implementer
from device.models import Device

LOGGER = logging.getLogger(__name__)


def discover(on_devices_discovered):
    """
    Interface function for the discovery action of the GCI.
    """
    LOGGER.info("connection interface calling for a device discovery")

    _gci_implementer.instance.discover(on_devices_discovered)


def connect(device: Device) -> bool:
    """
    Interface function for the connect action of the GCI.

    :param device: Device
    :return: True if connected
    """
    LOGGER.info("connection interface calling for a device connection")

    return _gci_implementer.instance.connect(device)
