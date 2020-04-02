import logging


LOGGER = logging.getLogger(__name__)


def handle_device_message(message):
    """
    Starting point for device originated messages.

    :param bytes message: incoming device message
    :return: may return an answer
    """
    LOGGER.info("device in handler for device messages")
