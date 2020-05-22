import logging


LOGGER = logging.getLogger(__name__)

"""
This module acts as a starting point for device originated messages.
"""


def attach(message_content):
    """
    :param dict message_content: incoming device message
    :return dict: result of message handling
    """
    LOGGER.debug("start handling device message")

    # Save HUME specific parameters and forward rest to HINT.

