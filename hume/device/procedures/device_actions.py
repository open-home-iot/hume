import logging

import storage

from device import connection
from device.connection.gci import GCI
from device.models import Device
from defs import DeviceRequest


LOGGER = logging.getLogger(__name__)


def device_action(device_uuid,
                  group_id=None,
                  state_id=None,
                  **kwargs):
    """
    :param device_uuid: str
    :param group_id: int
    :param state_id: int
    """
    device = storage.get(Device, device_uuid)
    if device is None:
        LOGGER.error(f"got action request for unknown device: {device_uuid}")
        raise ValueError("unknown device")

    # Check if STATEFUL action
    if group_id is not None:
        content = f"{DeviceRequest.ACTION_STATEFUL}" \
                  f"{group_id}" \
                  f"{state_id}"
        connection.send(GCI.Message(content), device)

    else:
        LOGGER.error("unable to recognize action type")
        raise ValueError("could not resolve action request type")
