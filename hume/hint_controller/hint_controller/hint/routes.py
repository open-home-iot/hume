import logging

from bottle import request, route

from hint_controller.messages.application import incoming_hint_message
from hint_controller.messages.definitions import *

LOGGER = logging.getLogger(__name__)


@route('/device/<uuid>/attach', method='PATCH')
def confirm_attach(uuid):
    """
    HINT confirms the attach of a device.

    :param uuid:
    :return:
    """
    LOGGER.info("got message confirm attach from HINT")

    result = incoming_hint_message(HINT_MESSAGE_CONFIRM_ATTACH,
                                   uuid)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


@route('/device/<uuid>/configurations', method='POST')
def device_configuration(uuid):
    """
    HINT sends configuration for a device (and potentially for its sub-devices).

    :param uuid:
    :return:
    """
    LOGGER.info("got device configuration request from HINT")
    LOGGER.debug(f"{request.json}")

    result = incoming_hint_message(HINT_MESSAGE_DEVICE_CONFIGURATION,
                                   request.json,
                                   uuid)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


@route('device/<uuid>/actions/<action_id:int>', method='PUT')
def device_action(uuid, action_id: int):
    """
    HINT sends an action invocation for a device action.

    :param uuid:
    :param action_id:
    :return:
    """
    LOGGER.info("got device action invocation from HINT")
    LOGGER.debug(f"{uuid} {action_id}")

    result = incoming_hint_message(HINT_MESSAGE_DEVICE_ACTION,
                                   uuid,
                                   action_id)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


@route('device/<uuid>/sub-devices/<device_id:int>/actions/<action_id:int>',
       method='PUT')
def sub_device_action(uuid, device_id: int, action_id: int):
    """
    HINT sends an action invocation for a sub-device action.

    :param uuid:
    :param device_id:
    :param action_id:
    :return:
    """
    LOGGER.info("got sub device action invocation from HINT")
    LOGGER.debug(f"{uuid} {action_id}")

    result = incoming_hint_message(HINT_MESSAGE_SUB_DEVICE_ACTION,
                                   uuid,
                                   device_id,
                                   action_id)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}
