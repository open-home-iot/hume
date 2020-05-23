import json
import logging

from hint_controller.util import broker
from . import rpc_req_handler


LOGGER = logging.getLogger(__name__)

HINT_CONTROLLER_QUEUE = "rpc_hint_controller"
DEVICE_CONTROLLER_QUEUE = "rpc_device_controller"


def start():
    """
    Starts the RPC application
    """
    LOGGER.info("rpc start")

    broker.enable_rpc_server(HINT_CONTROLLER_QUEUE,
                             rpc_req_handler.incoming_rpc_request)


def stop():
    """
    Stops the RPC application
    """
    LOGGER.info("rpc stop")


def send_device_controller_message(message):
    """
    Sends a message to the device controller, collocated on the HUME.

    :param dict message: message content
    :return dict: result of device controller message
    """
    return json.loads(broker.rpc_call(DEVICE_CONTROLLER_QUEUE,
                      json.dumps(message).encode('utf-8')).decode('utf-8'))
