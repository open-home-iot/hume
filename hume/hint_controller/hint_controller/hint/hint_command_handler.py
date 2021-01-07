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

    if decoded_command["type"] == defs.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")

        # To avoid re-encoding
        dispatch.forward_command_to_dc(command)
