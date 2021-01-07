import json
import logging

from hint_controller import defs
from hint_controller.hint import hint_command_lib


LOGGER = logging.getLogger(__name__)


"""
This module is the starting point for commands originating from the DC.
"""


def incoming_command(command):
    """
    :param command: DC command
    :type command: bytes
    """
    LOGGER.debug(f"got command from DC: {command}")

    decoded_command = json.loads(command.decode('utf-8'))

    if decoded_command["type"] == defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")
        # Forward the whole thing, nothing needs to be changed.
        hint_command_lib.discover_devices_done(decoded_command)
