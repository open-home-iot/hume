import logging


LOGGER = logging.getLogger(__name__)


def attach(message_content):
    """
    Sends HINT an attach message.

    :param message_content:
    :return:
    """
    LOGGER.info(f"sending HINT attach message: {message_content}")
