import json
import logging

from hume_broker import broker
from . import rpc_req_handler


LOGGER = logging.getLogger(__name__)

DEVICE_CONTROLLER_QUEUE = "rpc_device_controller"
HINT_CONTROLLER_QUEUE = "rpc_hint_controller"


def start():
    """
    Starts the RPC application
    """
    LOGGER.info("dc rpc start")

    broker.enable_rpc_server(DEVICE_CONTROLLER_QUEUE,
                             rpc_req_handler.incoming_rpc_request)


def stop():
    """
    Stops the RPC application
    """
    LOGGER.info("dc rpc stop")


def send_hint_controller_message(message):
    """
    Sends a message to the HINT controller, collocated on the HUME.

    :param dict message: message content
    :return dict: result of HINT controller message
    """
    LOGGER.info("sending HINT controller a message")
    LOGGER.debug(f"message contents: {message}")

    return json.loads(broker.rpc_call(HINT_CONTROLLER_QUEUE,
                      json.dumps(message).encode('utf-8')).decode('utf-8'))
