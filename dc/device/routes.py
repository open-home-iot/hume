import logging

from bottle import request, post
from device import request_handler


LOGGER = logging.getLogger(__name__)


@post('/devices/attach')
def attach():
    """
    A device sends an attach message to HUME.
    """
    LOGGER.info("device attach received")

    request.json["ip_address"] = request.environ.get("REMOTE_ADDR")
    LOGGER.debug(f"device attach request content: {request.json}")

    request_handler.attach(request.json)
