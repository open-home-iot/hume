import requests
import logging


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to a device.
"""


def confirm_attach(device):
    """
    Sends the parameter device an attach confirm message

    :param device:
    :return:
    """
    LOGGER.info(f"sending confirm attach request to device: {device.uuid}")


def device_action(device, action_id):
    """
    Sends a device an action invocation.

    :param device:
    :param action_id:
    :return:
    """
    LOGGER.info(f"sending device action: {device} {action_id}")


def sub_device_action(device, device_id, action_id):
    """
    Sends a sub device an action invocation.

    :param device:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.info(f"sending sub device action: {device} {device_id} {action_id}")
