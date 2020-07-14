import logging


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to HINT.
"""


def pair(hume):
    """
    Sends a pairing request for the parameter HUME.

    :param hume:
    :return:
    """
    LOGGER.debug(f"sending pairing request for HUME: {hume.hume_id}")


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT attach message: {message_content}")


def device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT device event message: {message_content}")


def sub_device_event(message_content):
    """
    Sends HINT an event message.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sending HINT event message: {message_content}")
