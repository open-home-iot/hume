import logging

from bottle import request, route

from device_controller.messages.application import device_message, \
    DEVICE_MESSAGE_ATTACH


LOGGER = logging.getLogger(__name__)


@route('/attach')
def attach():
    LOGGER.info("device attach received")

    LOGGER.debug(f"attach content: {request.json}")
    result = device_message(DEVICE_MESSAGE_ATTACH, request.json)

    return {"result": "ok"}
