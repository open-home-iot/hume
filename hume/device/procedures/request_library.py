import logging

from device.models import Device
from device import connection
from device.connection.gci import GCI
from defs import DeviceMessage

LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to a device.
"""


def capability(device: Device):
    """
    Sends a capability request to the target device.

    :param device: device to send the capability request to
    """
    content = f"{DeviceMessage.CAPABILITY}"
    connection.send(GCI.Message(content), device)
