"""
Designed as glue between the GCI implementer and callers, since callers are
calling discovery from a synchronous context.
"""


import logging

from device.connection.application import _gci_implementer
from device.connection.gci import GCI
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


def is_connected(device: Device) -> bool:
    """
    Interface function for the is_connected check, not part of the GCI.

    :param device: Device
    :return: True if connected
    """
    LOGGER.info("connection interface calling for checking if a device is "
                "connected")

    return _gci_implementer.instance.is_connected(device)


def disconnect(device: Device) -> bool:
    """
    Interface function for the disconnect action of the GCI.

    :param device: Device
    :return: True if successful
    """
    LOGGER.info("connection interface calling for a device disconnect")

    return _gci_implementer.instance.disconnect(device)


def disconnect_all() -> bool:
    """
    Interface function for the disconnect action of the GCI.

    :return: True if successful
    """
    LOGGER.info("connection interface calling for a device disconnect")

    return _gci_implementer.instance.disconnect_all()


def send(msg: GCI.Message, device: Device) -> bool:
    """
    Interface function for the send action of the GCI.

    :param msg: str
    :param device:
    :return:
    """
    LOGGER.info("connection interface calling for a device message")

    return _gci_implementer.instance.send(msg, device)


def notify(callback: callable, device: Device):
    """
    Interface function for waiting for a device message, part of the GCI.

    :param callback:
    :param device:
    :return:
    """
    LOGGER.info("connection interface waiting for a device message")

    _gci_implementer.instance.notify(callback, device)
