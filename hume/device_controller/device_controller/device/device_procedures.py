import logging

import hume_storage

from device_controller.device.models import Device
from device_controller.device import device_req_lib
from device_controller import dispatch
from device_controller import defs


LOGGER = logging.getLogger(__name__)


def discover_devices(command_content):
    """
    Sends a capability request to each unattached device that the HUME knows
    about, and then responds with the result to HC.

    :param command_content: currently not in use, empty
    :type command_content: str
    """
    LOGGER.debug(f"discover devices command content: {command_content}")

    devices = hume_storage.get_all(Device)
    result = []

    for device in devices:
        if not device.attached:

            device_capability = device_req_lib.capability_request(device)
            if device_capability is not None:
                result.append(device_capability)

    LOGGER.debug(f"the following devices responded: {result}")

    dispatch.hc_command(
        {
            "type": defs.DISCOVER_DEVICES,
            "content": result
        }
    )


def confirm_attach(device_uuid):
    """
    :param device_uuid: device to attach
    :type device_uuid: str
    """
    LOGGER.debug(f"confirm attach for: {device_uuid}")

    device = hume_storage.get(Device, device_uuid)

    if device:
        if device_req_lib.heartbeat_request(device):
            device.attached = True
            hume_storage.save(device)

            dispatch.hc_command(
                {
                    "type": defs.CONFIRM_ATTACH,
                    "content": {"device_uuid": device_uuid, "success": True}
                }
            )
            return
        else:
            LOGGER.warning("device did not respond to heartbeat request")
            # Remove if not attached, either the device info is faulty, or
            # device has issues
            if not device.attached:
                hume_storage.delete(device)
    else:
        LOGGER.error("device to be attached does not exist")

    dispatch.hc_command(
        {
            "type": defs.CONFIRM_ATTACH,
            "content": {"device_uuid": device_uuid, "success": False}
        }
    )
