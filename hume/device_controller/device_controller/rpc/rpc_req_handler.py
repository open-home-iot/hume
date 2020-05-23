import json
import logging

from device_controller.device.model import Device
from device_controller.util import storage
from device_controller.config import application as config

LOGGER = logging.getLogger(__name__)

# HINT ORIGINATED
HINT_MESSAGE_CONFIRM_ATTACH = 1
HINT_MESSAGE_DEVICE_CONFIGURATION = 2
HINT_MESSAGE_DEVICE_ACTION = 3
HINT_MESSAGE_SUB_DEVICE_ACTION = 4


"""
This module acts as a starting point for HINT controller originated RPC reqs.
"""


def incoming_rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("messages got new rpc request")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    if decoded_req["message_type"] == HINT_MESSAGE_CONFIRM_ATTACH:
        confirm_attach(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_CONFIGURATION:
        device_configuration(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_ACTION:
        device_action(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_SUB_DEVICE_ACTION:
        sub_device_action(decoded_req["message_content"])

    # TODO, result should depend on outcome
    return json.dumps({"result": "OK"}).encode('utf-8')


def confirm_attach(message_content):
    """
    Called on HINT controller confirming an attached device.

    :param dict message_content:
    :return:
    """
    LOGGER.debug(f"confirm attach received: {message_content}")

    # Resolve device
    uuid = message_content["uuid"]
    device = storage.get(Device, uuid)
    LOGGER.debug(f"found device: {device}")

    # Mark device as attached
    device.attached = True
    storage.save(device)


def device_configuration(message_content):
    """
    Called on HINT controller forwarding a device's new configuration data.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"device configuration received: {message_content}")

    # Load into config application
    config.new_configuration(message_content["uuid"], message_content["config"])


def device_action(message_content):
    """
    Called on HINT controller forwarding a device action.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"device action received: {message_content}")

    # TODO forward action to the device


def sub_device_action(message_content):
    """
    Called on HINT controller forwarding a sub device action.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sub device action received: {message_content}")

    # TODO forward action to the device
