import logging

from bottle import request, put, post
from . import device_req_handler


LOGGER = logging.getLogger(__name__)


@post('/device/attach')
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


@put('/device/<uuid>/events/<event_id:int>')
def device_event(uuid, event_id: int):
    """
    A device sends an event.

    :param uuid:
    :param event_id:
    :return:
    """
    LOGGER.info("device event received")

    result = device_req_handler.device_event(uuid, event_id, request.json)

    return {"result": "ok"}


@put('/device/<uuid>/sub-devices/<device_id:int>/events/<event_id:int>')
def sub_device_event(uuid, device_id: int, event_id: int):
    """
    A device sends an event.

    :param uuid:
    :param device_id:
    :param event_id:
    :return:
    """
    LOGGER.info("sub device event received")

    result = device_req_handler.sub_device_event(uuid,
                                                 device_id,
                                                 event_id,
                                                 request.json)

    return {"result": "ok"}
