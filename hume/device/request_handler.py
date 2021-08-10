import logging

from device.models import Device

LOGGER = logging.getLogger(__name__)


"""
This module specifies the handling of device messages.
"""


def incoming_message(device: Device, request_type: int, data: bytes):
    """
    A device has sent a message to HUME.

    :param device: sender Device
    :param request_type: type of received message
    :param data: message data
    """
    LOGGER.info(f"device address {device.address} and uuid {device.uuid}")
    LOGGER.info(f"request type: {request_type}")
    LOGGER.info(f"gotten data: {data}")


def capability_response(device, data):
    """
    Called when a device responds to a capability request.

    :param device: Device callee
    :param data: capability data
    :return:
    """
    # TODO: Store the gotten capabilities in HUME as well, HUME needs to
    #  know some things for validation, but add what's needed WHEN it's
    #  needed.
    pass
