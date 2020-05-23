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
