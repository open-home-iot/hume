import logging

from hint_controller.rpc import application as rpc
from hint_controller.messages.definitions import HINT_MESSAGE_CONFIRM_ATTACH


LOGGER = logging.getLogger(__name__)


def confirm_attach(uuid):
    """
    Handler function for confirm attach messages.

    :param uuid:
    :return:
    """
    LOGGER.debug(f"got message confirm attach for UUID: {uuid}")

    # TODO add retry functionality?
    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_CONFIRM_ATTACH,
        "message_content": {"uuid": uuid}
    })

    LOGGER.debug(f"Device controller responded: {response}")
