import logging
import json

from hume_broker import broker

from hint_controller.dispatch import rpc_req_dispatcher
from hint_controller.dispatch import command_dispatcher


LOGGER = logging.getLogger(__name__)

HINT_CONTROLLER_RPC = "rpc_hint_controller"
DEVICE_CONTROLLER_RPC = "rpc_device_controller"

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
    LOGGER.info("hc dispatch start")

    broker.enable_rpc_server(HINT_CONTROLLER_RPC,
                             rpc_req_dispatcher.incoming_rpc_request)
    broker.command_queue(HINT_CONTROLLER_COMMAND_QUEUE,
                         command_dispatcher.incoming_command)


def stop():
    """
    Stops the dispatch application
    """
    LOGGER.info("hc dispatch stop")


def forward_command_to_dc(command):
    """
    :type command: bytes
    """
    broker.command(DEVICE_CONTROLLER_COMMAND_QUEUE, command)


def dc_command(command_content):
    """
    Input must be possible to convert to valid JSON.

    :type command_content: dict
    """
    broker.command(DEVICE_CONTROLLER_COMMAND_QUEUE,
                   json.dumps(command_content).encode('utf-8'))
