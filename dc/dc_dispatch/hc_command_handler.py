import json
import logging

import dc_defs

from rabbitmq_client import ConsumeOK

from device import procedures


LOGGER = logging.getLogger(__name__)


"""
This module is the starting point for commands originating from the HC.
"""


def incoming_command(command):
    """
    :param command: HC command
    :type command: bytes
    """
    if isinstance(command, ConsumeOK):
        LOGGER.info("hc command handler got ConsumeOK")
        return

    LOGGER.info("got command from HC")

    decoded_command = json.loads(command.decode('utf-8'))

    command_type = decoded_command["type"]

    if command_type == dc_defs.MessageType.DISCOVER_DEVICES:
        LOGGER.info("received device discovery")

        procedures.discover_devices(decoded_command["content"])

    elif command_type == dc_defs.MessageType.CONFIRM_ATTACH:
        LOGGER.info("received confirm attach")

        procedures.confirm_attach(decoded_command["content"])

    elif command_type == dc_defs.MessageType.DETACH:
        LOGGER.info("received detach command")

        procedures.detach(decoded_command["content"])
