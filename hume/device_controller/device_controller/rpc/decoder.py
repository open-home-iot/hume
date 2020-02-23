import json
import logging


LOGGER = logging.getLogger(__name__)


def decode(message: bytes):
    """
    Decodes an RPC request's message body.

    :param bytes message: encoded message
    :return dict decoded_message: decoded message
    """
    LOGGER.debug(f"decoding message: {message}")

    return json.loads(message.decode('utf-8'))
