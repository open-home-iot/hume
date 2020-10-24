import logging


LOGGER = logging.getLogger(__name__)


"""
This module provides functions for sending requests to HINT.
"""


def pair():
    """
    Sends a pairing request for the parameter HUME.

    :return:
    """
    LOGGER.debug("sending pairing request")


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
