import logging

from device_controller.util import broker
from device_controller.messages import application as messages


LOGGER = logging.getLogger(__name__)

DEVICE_CONTROLLER_QUEUE = "rpc_device_controller"
HINT_CONTROLLER_QUEUE = "rpc_hint_controller"


def start():
    """
    Starts the RPC application
    """
    LOGGER.info("rpc start")

    broker.enable_rpc_server(DEVICE_CONTROLLER_QUEUE,
                             messages.incoming_rpc_request)


def stop():
    """
    Stops the RPC application
    """
    LOGGER.info("rpc stop")


def send_hint_controller_message(message):
    """
    Sends a message to the HINT controller, collocated on the HUME.

    :param message: message content
    :return: result of HINT controller message
    """
    return broker.rpc_call(HINT_CONTROLLER_QUEUE, message)

