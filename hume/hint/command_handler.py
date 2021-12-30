import logging
import json
import storage

from rabbitmq_client import ConsumeOK

from defs import HINTCommand
from device import (
    discover_devices,
    attach_device,
    detach_device,
    device_action,
    connection
)
from hint.procedures.command_library import (
    devices_discovered,
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
    if command_type == HINTCommand.DISCOVER_DEVICES:
        LOGGER.info("received device discovery command")
        discover_devices(devices_discovered)

    elif command_type == HINTCommand.ATTACH_DEVICE:
        LOGGER.info(f"received device attach command for "
                    f"{decoded_command['identifier']}")

        attach_device(decoded_command["identifier"])

    elif command_type == HINTCommand.DEVICE_ACTION:
        LOGGER.info(f"received a device action command for: "
                    f"{decoded_command['device_uuid']}")
        device_uuid = decoded_command.pop("device_uuid")
        decoded_command.pop("type")
        device_action(device_uuid, **decoded_command)

    elif command_type == HINTCommand.UNPAIR:
        LOGGER.info("received an unpair command, factory resetting hume")
        connection.disconnect_all()
        storage.delete_all()

    elif command_type == HINTCommand.DETACH:
        LOGGER.info(f"got detach for device {decoded_command['device_uuid']}")
        detach_device(decoded_command["device_uuid"])

    else:
        LOGGER.info(f"got unknown command: {decoded_command}")
