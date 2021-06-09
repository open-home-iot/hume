import json
import logging

import defs

from rabbitmq_client import ConsumeOK

from device import device_procedures


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

    LOGGER.debug(f"got command from HC: {command}")

    decoded_command = json.loads(command.decode('utf-8'))

    command_type = decoded_command["type"]

    if command_type == defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")

        device_procedures.discover_devices(decoded_command["content"])

    elif command_type == defs.CONFIRM_ATTACH:
        LOGGER.info(f"received confirm attach command for device: "
                    f"{decoded_command['content']}")

        device_procedures.confirm_attach(decoded_command["content"])

    elif command_type == defs.DETACH:
        LOGGER.info(f"received detach command for device: "
                    f"{decoded_command['content']}")

        device_procedures.detach(decoded_command["content"])