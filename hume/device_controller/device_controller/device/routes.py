import logging

from bottle import request, route

from device_controller.messages.application import incoming_device_message, \
    DEVICE_MESSAGE_ATTACH


LOGGER = logging.getLogger(__name__)


@route('/attach')
def attach():
    LOGGER.info("device attach received")

    device_ip = request.environ.get("REMOTE_ADDR")
    LOGGER.debug(f"device IP: {device_ip}")

    request.json["device_ip"] = device_ip
    LOGGER.debug(f"attach content: {request.json}")

    result = incoming_device_message(DEVICE_MESSAGE_ATTACH, request.json)

    return {"result": "ok"}
