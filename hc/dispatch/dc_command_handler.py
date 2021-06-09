import json
import logging

import defs

from rabbitmq_client import ConsumeOK

from hint import hint_command_lib


LOGGER = logging.getLogger(__name__)


"""
This module is the starting point for commands originating from the DC.
"""


def incoming_command(command):
    """
    :param command: DC command
    :type command: bytes
    """
    if isinstance(command, ConsumeOK):
        LOGGER.info("dc command handler got ConsumeOK")
        return

    LOGGER.debug(f"got command from DC: {command}")

    decoded_command = json.loads(command.decode('utf-8'))

    command_type = decoded_command["type"]

    if command_type == defs.DISCOVER_DEVICES:
        LOGGER.debug("received a discover devices complete from DC")

        # Forward the whole thing, nothing needs to be changed.
        hint_command_lib.discover_devices_done(decoded_command)

    elif command_type == defs.CONFIRM_ATTACH:
        LOGGER.debug("received a confirm attach result from DC")

        hint_command_lib.confirm_attach_result(decoded_command)
