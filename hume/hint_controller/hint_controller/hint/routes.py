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


@route('/device/<uuid>/configurations')
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
