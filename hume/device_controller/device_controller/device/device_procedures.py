import logging

import hume_storage

from device_controller.device.models import Device
from device_controller.device import device_req_lib
from device_controller import dispatch


LOGGER = logging.getLogger(__name__)


def discover_devices(command_content):
    """
    Sends a capability request to each unattached device that the HUME knows
    about, and then responds with the result to HC.

    :type command_content: str
    """
    LOGGER.debug(f"discover devices command content: {command_content}")

    devices = hume_storage.get_all(Device)
    result = []

    for device in devices:
        if not device.attached:
            result.append(device_req_lib.capability_request(device))

    LOGGER.debug(f"the following devices responded: {result}")

    dispatch.hc_command(result)
