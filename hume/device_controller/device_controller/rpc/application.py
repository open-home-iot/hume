import logging

from device_controller.util import broker
from device_controller.messages import application as messages


LOGGER = logging.getLogger(__name__)

DEVICE_CONTROLLER_QUEUE = "rpc_device_controller"


def start():
    """
    Starts the RPC application
    """
    LOGGER.info("rpc start")

    broker.enable_rpc_server(DEVICE_CONTROLLER_QUEUE, messages.rpc_request)


def stop():
    """
    Stops the RPC application
    """
    LOGGER.info("rpc stop")
