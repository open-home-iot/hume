import logging
import json

from rabbitmq_client import ConsumeOK

from defs import CommandType
from device import (
    discover_devices,
    attach_device,
)
from hint.procedures.command_library import (
    devices_discovered,
    device_attached,
)


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
    if command_type == CommandType.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")
        discover_devices(devices_discovered)

    elif command_type == CommandType.ATTACH_DEVICE:
        LOGGER.info(f"received device attach command for "
                    f"{decoded_command['device_address']}")

        attach_device(decoded_command["device_address"], device_attached)