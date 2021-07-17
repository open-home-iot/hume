import logging

import hume_storage

import dc_dispatch
import dc_defs

from device.models import Device
from device import request_library


LOGGER = logging.getLogger(__name__)


def discover_devices(command_content):
    """
    Sends a capability request to each unattached device that the HUME knows
    about, and then responds with the result to HC.

    :param command_content: currently not in use, empty
    :type command_content: str
    """
    LOGGER.info("discover devices command gotten")

    devices = hume_storage.get_all(Device)
    result = []

    for device in devices:
        if not device.attached:

            device_capability = request_library.capability_request(device)
            if device_capability is not None:
                result.append(device_capability)

    LOGGER.info(f"the following devices responded: "
                f"{[cap['uuid'] for cap in result]}")
    LOGGER.debug(f"full reply content: {result}")

    dc_dispatch.hc_command(
        {
            "type": dc_defs.MessageType.DISCOVER_DEVICES,
            "content": result
        }
    )


def confirm_attach(device_uuid):
    """
    :param device_uuid: device to attach
    :type device_uuid: str
    """
    LOGGER.info(f"sending confirm attach to: {device_uuid}")

    device = hume_storage.get(Device, device_uuid)

    if device:

        if request_library.heartbeat_request(device):
            LOGGER.debug("heartbeat request succeeded")

            device.attached = True
            hume_storage.save(device)

            dc_dispatch.hc_command(
                {
                    "type": dc_defs.MessageType.CONFIRM_ATTACH,
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

    dc_dispatch.hc_command(
        {
            "type": dc_defs.MessageType.CONFIRM_ATTACH,
            "content": {"device_uuid": device_uuid, "success": False}
        }
    )


def detach(device_uuid):
    """
    Detach the parameter device from HUME, removing all associated data.

    NOTE! In the future, this procedure needs to be extended to delete
    configurations as well.

    :param device_uuid: UUID of device to detach
    :type device_uuid: str
    """
    LOGGER.info(f"detaching device: {device_uuid}")

    device = hume_storage.get(Device, device_uuid)

    if device:
        LOGGER.debug("found device to delete")

        hume_storage.delete(device)
    else:
        LOGGER.debug("device does not exist")
