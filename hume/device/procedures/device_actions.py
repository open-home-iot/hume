import logging

import storage

from device import connection
from device.connection.gci import GCI
from device.models import Device
from defs import DeviceRequest


LOGGER = logging.getLogger(__name__)


def device_action(device_uuid,
                  device_state_group_id=None,
                  device_state_id=None,
                  **kwargs):
    """
    :param device_uuid: str
    :param device_state_group_id: int
    :param device_state_id: int
    """
    device = storage.get(Device, device_uuid)
    if device is None:
        LOGGER.error(f"got action request for unknown device: {device_uuid}")
        return

    # Check if state change request
    if device_state_group_id is not None:
        connection.send(
            GCI.Message(f"^{DeviceRequest.DEVICE_ACTION}"
                        f"{device_state_group_id}"
                        f"{device_state_id}$".encode('utf-8')),
            device
        )

    else:
        raise ValueError("could not resolve action request type")
