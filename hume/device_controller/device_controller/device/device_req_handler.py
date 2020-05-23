import logging

from peewee import DoesNotExist

from device_controller.device.models import Device
from device_controller.util import storage
from device_controller.rpc import application as rpc
from .application import device_req_mod

LOGGER = logging.getLogger(__name__)

# DEVICE ORIGINATED
DEVICE_MESSAGE_ATTACH = 0


"""
This module acts as a starting point for device originated messages.
"""


def attach(message_content):
    """
    :param dict message_content: incoming device message
    :return dict: result of message handling
    """
    LOGGER.debug("saving device information and forwarding info to HINT "
                 "controller")

    # Save HUME specific parameters and forward rest to HINT.
    device_ip = message_content.pop("device_ip")
    uuid = message_content["uuid"]

    try:
        device = Device.get(Device.uuid == uuid)
        LOGGER.debug("device was already attached, confirming back to device")
        # TODO send device confirm attach request.
        device_req_mod.confirm_attach(device)

    except DoesNotExist:
        LOGGER.debug("device not previously attached")
        device = Device(uuid=uuid, ip_address=device_ip)
        storage.save(device)

    hint_controller_message = {
        "message_type": DEVICE_MESSAGE_ATTACH,
        "message_content": message_content
    }

    response = rpc.send_hint_controller_message(hint_controller_message)
    LOGGER.debug(f"HINT controller responded: {response}")
