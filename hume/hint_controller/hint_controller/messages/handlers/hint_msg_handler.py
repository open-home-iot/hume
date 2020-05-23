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
