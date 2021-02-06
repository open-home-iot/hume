import logging
import json

from hume_broker import broker

from device_controller.dispatch import hc_rpc_req_handler
from device_controller.dispatch import hc_command_handler


LOGGER = logging.getLogger(__name__)

DEVICE_CONTROLLER_RPC = "rpc_device_controller"
HINT_CONTROLLER_RPC = "rpc_hint_controller"

HINT_CONTROLLER_COMMAND_QUEUE = "command_hint_controller"
DEVICE_CONTROLLER_COMMAND_QUEUE = "command_device_controller"


"""
This module is the starting point of the dispatch application, responsible for
registering callbacks for various HUME internal comm. types.
"""


def model_init():
    """
    Initialize models.
    """
    LOGGER.info("model-init")


def pre_start():
    """
    Pre-start, before starting applications.
    """
    LOGGER.info("pre-start")


def start():
    """
    Starts the dispatch application
    """
    LOGGER.info("dc dispatch start")

    broker.enable_rpc_server(DEVICE_CONTROLLER_RPC,
                             hc_rpc_req_handler.incoming_rpc_request)
    broker.command_queue(DEVICE_CONTROLLER_COMMAND_QUEUE,
                         hc_command_handler.incoming_command)


def stop():
    """
    Stops the dispatch application
    """
    LOGGER.info("dc dispatch stop")


def hc_command(command_content):
    """
    Input must be possible to convert to valid JSON.

    :type command_content: dict
    """
    broker.command(HINT_CONTROLLER_COMMAND_QUEUE,
                   json.dumps(command_content).encode('utf-8'))
