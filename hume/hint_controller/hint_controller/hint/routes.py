import logging

from bottle import request, route, put

from . import hint_req_handler

LOGGER = logging.getLogger(__name__)


@route('/device/<uuid>/attach', method='PATCH')
def confirm_attach(uuid):
    """
    HINT confirms the attach of a device.

    :param uuid:
    :return:
    """
    LOGGER.info("got message confirm attach from HINT")

    result = hint_req_handler.confirm_attach(uuid)

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

    result = hint_req_handler.device_configuration(request.json, uuid)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


@put('/device/<uuid>/actions/<action_id:int>')
def device_action(uuid, action_id: int):
    """
    HINT sends an action invocation for a device action.

    :param uuid:
    :param action_id:
    :return:
    """
    LOGGER.info("got device action invocation from HINT")
    LOGGER.debug(f"{uuid} {action_id}")

    result = hint_req_handler.device_action(uuid, action_id)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


@put('/device/<uuid>/sub-devices/<device_id:int>/actions/<action_id:int>')
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

    result = hint_req_handler.sub_device_action(uuid, device_id, action_id)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}
