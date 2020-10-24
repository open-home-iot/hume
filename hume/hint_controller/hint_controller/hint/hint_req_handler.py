import logging

import hume_storage as storage
from hint_controller.rpc import application as rpc
from .util import read_hume_id


LOGGER = logging.getLogger(__name__)

# HINT ORIGINATED
HINT_MESSAGE_CONFIRM_ATTACH = 1
HINT_MESSAGE_DETACH = 2

HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_CREATE = 3
HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_DELETE = 4
HINT_MESSAGE_DEVICE_SCHEDULE_CONFIGURATION_CREATE = 5
HINT_MESSAGE_DEVICE_SCHEDULE_CONFIGURATION_DELETE = 6
HINT_MESSAGE_DEVICE_TRIGGER_CONFIGURATION_CREATE = 7
HINT_MESSAGE_DEVICE_TRIGGER_CONFIGURATION_DELETE = 8

HINT_MESSAGE_DEVICE_ACTION = 9
HINT_MESSAGE_SUB_DEVICE_ACTION = 10


"""
This module is the starting point of HINT originating request handling.
"""


def confirm_pairing():
    """
    Handler function for confirm pairing.

    :return:
    """
    LOGGER.debug("got message confirm pairing")

    # TODO return based on outcome


def unpair():
    """
    Handler function for unpair.

    :return:
    """
    LOGGER.debug("get message unpair")

    # TODO return based on outcome


def confirm_attach(uuid):
    """
    Handler function for confirm attach messages.

    :param uuid:
    """
    LOGGER.debug(f"got message confirm attach for UUID: {uuid}")

    # TODO add retry functionality?
    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_CONFIRM_ATTACH,
        "message_content": {"uuid": uuid}
    })

    LOGGER.debug(f"Device controller responded: {response}")

    # TODO return based on outcome.


def detach(uuid):
    """
    Handler function for detach messages.

    :param uuid:
    :return:
    """
    LOGGER.debug(f"got message detach for UUID: {uuid}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DETACH,
        "message_content": {"uuid": uuid}
    })

    LOGGER.debug(f"Device controller responded: {response}")

    # TODO return based on outcome


def device_timer_configuration_create(uuid, message_content):
    """
    Handler function for device timer configuration create messages.

    :param uuid:
    :param message_content:
    """
    LOGGER.debug(f"device configuration handler, message content: "
                 f"{message_content}, uuid: {uuid}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_CREATE,
        "message_content": {"uuid": uuid, "timer": message_content}
    })

    LOGGER.debug(f"device controller responded: {response}")

    # TODO return based on outcome.
    return response


def device_timer_configuration_delete(uuid, timer):
    """
    Handler function for device timer configuration delete messages.

    :param uuid:
    :param timer:
    """
    LOGGER.debug(f"device configuration handler, message content: "
                 f"uuid: {uuid} timer: {timer}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DEVICE_TIMER_CONFIGURATION_DELETE,
        "message_content": {"uuid": uuid, "timer": timer}
    })

    LOGGER.debug(f"device controller responded: {response}")

    # TODO return based on outcome.
    return response


def device_action(uuid, action_id):
    """
    Handler function for device actions.

    :param uuid:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"device action handler {uuid} {action_id}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_DEVICE_ACTION,
        "message_content": {"uuid": uuid, "action_id": action_id}
    })

    LOGGER.debug(f"device controller responded: {response}")

    # TODO return based on outcome.


def sub_device_action(uuid, device_id, action_id):
    """
    Handler function for sub device actions.

    :param uuid:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.debug(f"sub device action handler {uuid} {device_id} {action_id}")

    response = rpc.send_device_controller_message({
        "message_type": HINT_MESSAGE_SUB_DEVICE_ACTION,
        "message_content": {
            "uuid": uuid,
            "device_id": device_id,
            "action_id": action_id
        }
    })

    LOGGER.debug(f"device controller responded: {response}")

    # TODO return based on outcome.
