import logging

from device_controller.device.models import Device
import hume_storage as storage
from ..rpc import application as rpc
from .settings import req_mod


LOGGER = logging.getLogger(__name__)

# DEVICE ORIGINATED
DEVICE_MESSAGE_ATTACH = 0
DEVICE_MESSAGE_DEVICE_EVENT = 1
DEVICE_MESSAGE_SUB_DEVICE_EVENT = 2


"""
This module acts as a starting point for device originated messages.
"""


def attach(message_content):
    """
    :param dict message_content: incoming device message
    """
    LOGGER.debug("saving device information and forwarding info to HINT "
                 "controller")

    # Save HUME specific parameters and forward rest to HINT.
    device_ip = message_content.pop("device_ip")
    uuid = message_content["uuid"]

    device = storage.get(Device, uuid)

    if device is not None and device.attached:
        LOGGER.debug(
            f"device {uuid} was already attached, confirming back to device right away"
        )

        # TODO return based on outcome
        return

    elif device is not None:
        LOGGER.debug("device already exists but not attached")

    else:
        LOGGER.debug("device not previously attached")
        device = Device(uuid=uuid, ip_address=device_ip)
        storage.save(device)

    hint_controller_message = {
        "message_type": DEVICE_MESSAGE_ATTACH,
        "message_content": message_content
    }

    response = rpc.send_hint_controller_message(hint_controller_message)
    LOGGER.debug(f"HINT controller responded: {response}")

    # TODO return based on outcome.


def device_event(uuid, event_id, message_content):
    """
    :param uuid:
    :param event_id:
    :param message_content:
    """
    LOGGER.debug("forwarding device event to HC")
    LOGGER.debug(f"{message_content}")

    hint_controller_message = {
        "message_type": DEVICE_MESSAGE_DEVICE_EVENT,
        "message_content": {
            "uuid": uuid,
            "event_id": event_id,
            "data": message_content["data"]
        }
    }

    response = rpc.send_hint_controller_message(hint_controller_message)
    LOGGER.debug(f"HINT controller responded: {response}")

    # TODO return based on outcome.


def sub_device_event(uuid, device_id, event_id, message_content):
    """
    :param uuid:
    :param device_id:
    :param event_id:
    :param message_content:
    """
    LOGGER.debug("forwarding sub device event to HC")

    hint_controller_message = {
        "message_type": DEVICE_MESSAGE_SUB_DEVICE_EVENT,
        "message_content": {
            "uuid": uuid,
            "device_id": device_id,
            "event_id": event_id,
            "data": message_content["data"]
        }
    }

    response = rpc.send_hint_controller_message(hint_controller_message)
    LOGGER.debug(f"HINT controller responded: {response}")

    # TODO return based on outcome.
