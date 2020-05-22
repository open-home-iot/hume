import logging

from device_controller.device.model import Device
from device_controller.util import storage
from device_controller.rpc import application as rpc
from device_controller.messages.application import DEVICE_MESSAGE_ATTACH


LOGGER = logging.getLogger(__name__)

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

    device = Device(uuid=uuid, ip_address=device_ip)
    storage.save(device)

    hint_controller_message = {
        "message_type": DEVICE_MESSAGE_ATTACH,
        "message_content": message_content

    }

    response = rpc.send_hint_controller_message(hint_controller_message)
    LOGGER.debug(f"HINT controller responded: {response}")
