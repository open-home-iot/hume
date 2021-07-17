import logging
import json

import hc_defs
import dc_communication

from rabbitmq_client import ConsumeOK


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

    if command_type == hc_defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")

        # To avoid re-encoding
        dc_communication.forward_command_to_dc(command)

    elif command_type == hc_defs.CONFIRM_ATTACH:
        LOGGER.info("received confirm attach command")

        dc_communication.forward_command_to_dc(command)

    elif command_type == hc_defs.DETACH:
        LOGGER.info("received detach command")

        dc_communication.forward_command_to_dc(command)
