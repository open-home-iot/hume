import json
import logging

from device_controller.device.models import Device
import hume_storage as storage
from device_controller.config import application as config
from device_controller.device import application as device_app

LOGGER = logging.getLogger(__name__)

# HINT ORIGINATED
HINT_MESSAGE_CONFIRM_ATTACH = 1

HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_CREATE = 2
HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_DELETE = 3
HINT_MESSAGE_DEVICE_SCHEDULE_CONFIGURATION_CREATE = 4
HINT_MESSAGE_DEVICE_SCHEDULE_CONFIGURATION_DELETE = 5
HINT_MESSAGE_DEVICE_TRIGGER_CONFIGURATION_CREATE = 6
HINT_MESSAGE_DEVICE_TRIGGER_CONFIGURATION_DELETE = 7

HINT_MESSAGE_DEVICE_ACTION = 8
HINT_MESSAGE_SUB_DEVICE_ACTION = 9


"""
This module acts as a starting point for HINT controller originated RPC reqs.
"""


def incoming_rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("new RPC request received")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    result = {"result": "OK"}

    if decoded_req["message_type"] == HINT_MESSAGE_CONFIRM_ATTACH:
        confirm_attach(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_CREATE:
        result = device_timer_configuration_create(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_DELETE:
        result = device_timer_configuration_delete(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_ACTION:
        device_action(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_SUB_DEVICE_ACTION:
        sub_device_action(decoded_req["message_content"])

    # TODO, more results should depend on outcome
    return json.dumps(result).encode('utf-8')


def confirm_attach(message_content):
    """
    Called on HINT controller confirming an attached device.

    :param dict message_content:
    """
    LOGGER.debug(f"confirm attach received: {message_content}")

    # Resolve device
    uuid = message_content["uuid"]
    device = storage.get(Device, uuid)
    LOGGER.debug(f"found device: {device}")

    # Mark device as attached
    device.attached = True
    storage.save(device)

    device_app.confirm_attach(device)


def device_timer_configuration_create(message_content):
    """
    Called on HINT controller forwarding a device's new timer configuration
    data.

    :param message_content:
    """
    LOGGER.debug(f"create device timer configuration received: "
                 f"{message_content}")

    # Load into config application
    ref = config.create_timer_configuration(
        message_content["uuid"], message_content["timer"]
    )

    return {"ref": ref}


def device_timer_configuration_delete(message_content):
    """
    Called on HINT controller forwarding a device's deleted timer configuration
    data.

    :param message_content:
    """
    LOGGER.debug(f"delete device timer configuration received: "
                 f"{message_content}")

    # delete from config application
    ref = config.delete_timer_configuration(
        message_content["uuid"], message_content["timer"]
    )

    if ref:
        result = {"deleted": ref}
    else:
        result = {"result": "error"}

    return result


def device_action(message_content):
    """
    Called on HINT controller forwarding a device action.

    :param message_content:
    """
    LOGGER.debug(f"device action received: {message_content}")

    # TODO get device info from storage
    device = storage.get(Device, message_content["uuid"])

    device_app.device_action(device, message_content["action_id"])


def sub_device_action(message_content):
    """
    Called on HINT controller forwarding a sub device action.

    :param message_content:
    """
    LOGGER.debug(f"sub device action received: {message_content}")

    # TODO get device info from storage
    device = storage.get(Device, message_content["uuid"])

    device_app.sub_device_action(device,
                                 message_content["device_id"],
                                 message_content["action_id"])
