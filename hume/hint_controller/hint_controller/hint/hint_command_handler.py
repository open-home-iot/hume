import logging
import json

from hint_controller import defs, dispatch


LOGGER = logging.getLogger(__name__)


def incoming_command(command):
    """
    :param command: HINT command
    :type command: bytes
    """
    decoded_command = json.loads(command.decode('utf-8'))

    command_type = decoded_command["type"]

    if command_type == defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")

        # To avoid re-encoding
        dispatch.forward_command_to_dc(command)

    elif command_type == defs.CONFIRM_ATTACH:
        LOGGER.info("received confirm attach command")

        dispatch.forward_command_to_dc(command)

    elif command_type == defs.DETACH:
        LOGGER.info("received detach command")

        dispatch.forward_command_to_dc(command)
