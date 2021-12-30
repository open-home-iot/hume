import json
import logging

import storage

from defs import DeviceRequest
from device.models import Device, DeviceAddress
from hint.models import HintAuthentication
from hint.procedures.request_library import create_device

LOGGER = logging.getLogger(__name__)


"""
This module specifies the handling of device messages.
"""


def incoming_message(device: Device, request_type: int, data: bytes):
    """
    A device has sent a message to HUME.

    :param device: sender Device
    :param request_type: type of received message
    :param data: message data
    """
    LOGGER.info(f"got new message from device {device.uuid}")

    # Device responded to a capability request
    if request_type == DeviceRequest.CAPABILITY:
        capability_response(device, data)


def capability_response(device, data):
    """
    Called when a device responds to a capability request.

    :param device: Device callee
    :param data: capability data
    :return:
    """
    LOGGER.info("handling capability response")
    # TODO: Store the gotten capabilities in HUME as well, HUME needs to
    #  know some things for validation, but add what's needed WHEN it's
    #  needed.
    capabilities = json.loads(data)

    hint_auth = storage.get(HintAuthentication, None)
    if create_device(
            capabilities, hint_auth.session_id, hint_auth.csrf_token
    ):
        LOGGER.info("device created in HINT successfully")

        # Update the device entry, set correct uuid
        storage.delete(device)  # Clear old address-resolved entry from local
        new_device = Device(uuid=capabilities["uuid"],
                            address=device.address,
                            name=device.name,
                            attached=True)
        storage.save(new_device)

        # Update device address entry to enable bi-directional lookups.
        device_address = storage.get(DeviceAddress, device.address)
        device_address.uuid = capabilities["uuid"]
        storage.save(device_address)
