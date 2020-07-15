import logging

from bottle import request, route, put, post, delete

from . import hint_req_handler

LOGGER = logging.getLogger(__name__)


@route('/confirm-pairing', method='POST')
def confirm_pairing():
    """
    HINT confirms the pairing of the HUME.

    :return:
    """
    LOGGER.info("got message confirm pairing from HINT")

    result = hint_req_handler.confirm_pairing()

    # TODO make result depend on message handling outcome
    return {"result": "ok"}


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


@post('/device/<uuid>/configurations/timers')
def device_timer_configuration_create(uuid):
    """
    HINT sends device timer configuration for a device (and potentially for its
    sub-devices).

    :param uuid:
    :return:
    """
    LOGGER.info("got device timer configuration create from HINT")

    result = hint_req_handler.device_timer_configuration_create(uuid,
                                                                request.json)

    # TODO make result depend on message handling outcome
    return result


@delete('/device/<uuid>/configurations/timers/<timer>')
def device_timer_configuration_delete(uuid, timer):
    """
    HINT sends a delete for a device timer configuration for a device (and
    potentially for its sub-devices).

    :param uuid:
    :param timer:
    :return:
    """
    LOGGER.info("got device timer configuration delete from HINT")

    result = hint_req_handler.device_timer_configuration_delete(uuid,
                                                                timer)

    # TODO make result depend on message handling outcome
    return result


@put('/device/<uuid>/actions/<action_id:int>')
def device_action(uuid, action_id: int):
    """
    HINT sends an action invocation for a device action.

    :param uuid:
    :param action_id:
    :return:
    """
    LOGGER.info("got device action invocation from HINT")

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

    result = hint_req_handler.sub_device_action(uuid, device_id, action_id)

    # TODO make result depend on message handling outcome
    return {"result": "ok"}
