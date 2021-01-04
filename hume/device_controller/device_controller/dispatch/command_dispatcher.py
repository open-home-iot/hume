import json
import logging

from device_controller import defs
from device_controller.device import device_procedures


LOGGER = logging.getLogger(__name__)


"""
This module is the starting point for commands originating from the HC.
"""


def incoming_command(command):
    """
    :param command: DC command
    :type command: bytes
    """
    LOGGER.debug(f"got command from HC: {command}")

    decoded_command = json.loads(command.decode('utf-8'))

    if decoded_command["type"] == defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")
        device_procedures.discover_devices(decoded_command["content"])
