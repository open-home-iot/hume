import logging

from bottle import request, route
from . import device_req_handler


LOGGER = logging.getLogger(__name__)


@route('/device/attach', method='POST')
def attach():
    """
    A device sends an attach message.

    :return:
    """
    LOGGER.info("device attach received")

    device_ip = request.environ.get("REMOTE_ADDR")
    LOGGER.debug(f"device IP: {device_ip}")

    request.json["device_ip"] = device_ip
    LOGGER.debug(f"attach content: {request.json}")

    result = device_req_handler.attach(request.json)

    return {"result": "ok"}
