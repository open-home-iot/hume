import logging

from hint_controller.rpc import application as rpc
from hint_controller.messages.definitions import *


LOGGER = logging.getLogger(__name__)


def confirm_attach(uuid):
    """
    Handler function for confirm attach messages.

    :param uuid:
    """
    LOGGER.debug(f"got message confirm attach for UUID: {uuid}")

    # TODO add retry functionality?
    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_CONFIRM_ATTACH,
        "message_content": {"uuid": uuid}
    })

    LOGGER.debug(f"Device controller responded: {response}")


def device_configuration(message_content, uuid):
    """
    Handler function for device configuration messages.

    :param message_content:
    :param uuid:
    """
    LOGGER.debug(f"device configuration handler, message content: "
                 f"{message_content}, uuid: {uuid}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DEVICE_CONFIGURATION,
        "message_content": {"uuid": uuid, "config": message_content}
    })

    LOGGER.debug(f"device controller responded: {response}")


def device_action(uuid, action_id):
    """
    Handler function for device actions.

    :param uuid:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"device action handler {uuid} {action_id}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DEVICE_ACTION,
        "message_content": {"uuid": uuid, "action_id": action_id}
    })

    LOGGER.debug(f"device controller responded: {response}")


def sub_device_action(uuid, device_id, action_id):
    """
    Handler function for sub device actions.

    :param uuid:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sub device action handler {uuid} {device_id} {action_id}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_SUB_DEVICE_ACTION,
        "message_content": {
            "uuid": uuid,
            "device_id": device_id,
            "action_id": action_id
        }
    })

    LOGGER.debug(f"device controller responded: {response}")
