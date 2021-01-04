import logging

import hume_storage

from device_controller.device.models import Device


LOGGER = logging.getLogger(__name__)


"""
This module specifies the handling of device messages.
"""


def attach(request_content):
    """
    :param dict request_content: incoming device message
    """
    device = hume_storage.get(Device, request_content["uuid"])

    # If exists, device has rebooted, save new IP
    if device:
        LOGGER.debug("device exists")
        device.ip_address = request_content["ip_address"]
    else:
        LOGGER.debug("new device")
        device = Device(uuid=request_content["uuid"],
                        ip_address=request_content["ip_address"])

    hume_storage.save(device)
