import logging

from hint_controller.util import broker
from hint_controller.messages import application as messages


LOGGER = logging.getLogger(__name__)

HINT_CONTROLLER_QUEUE = "rpc_hint_controller"


def start():
    """
    Starts the RPC application
    """
    LOGGER.info("rpc start")

    broker.enable_rpc_server(HINT_CONTROLLER_QUEUE, messages.rpc_request)


def stop():
    """
    Stops the RPC application
    """
    LOGGER.info("rpc stop")
