import logging
import json

from rabbitmq_client import ConsumeOK

from defs import MessageType
from device import discover as discover_devices


LOGGER = logging.getLogger(__name__)


def incoming_command(command):
    """
    :param command: HINT command
    :type command: bytes
    """
    if isinstance(command, ConsumeOK):
        LOGGER.info("hint command handler got ConsumeOK")
        return

    LOGGER.info("got command from HINT")

    decoded_command = json.loads(command.decode('utf-8'))
    command_type = decoded_command["type"]

    """
    Call appropriate procedure from here, or forward to DC for further handling
    """
    if command_type == MessageType.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")
        discover_devices()
