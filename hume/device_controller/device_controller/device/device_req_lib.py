import logging


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to a device.
"""


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sending device action: {device} {action_id}")


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sending sub device action: {device} {device_id} {action_id}")
