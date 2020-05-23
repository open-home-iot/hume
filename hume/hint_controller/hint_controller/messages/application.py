import json
import logging

from .definitions import *
from .handlers import rpc_msg_handler, hint_msg_handler


LOGGER = logging.getLogger(__name__)


def start():
    """
    Starts up the messages server.
    """
    LOGGER.info("messages start")


def stop():
    """
    Not needed for now.
    """
    LOGGER.info("messages stop")


def incoming_rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("messages got new rpc request")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    if decoded_req["message_type"] == DEVICE_MESSAGE_ATTACH:
        rpc_msg_handler.attach(decoded_req["message_content"])

    # TODO, result should depend on outcome
    return json.dumps({"result": "OK"}).encode('utf-8')


def incoming_hint_message(message_type, *args):
    """
    Called on incoming HINT messages.

    :param int message_type: type of message
    :return dict | None: may return an answer in dict form
    """
    LOGGER.info("got new message from HINT")

    if message_type == HINT_MESSAGE_CONFIRM_ATTACH:
        return hint_msg_handler.confirm_attach(*args)
    elif message_type == HINT_MESSAGE_DEVICE_CONFIGURATION:
        return hint_msg_handler.device_configuration(*args)
    elif message_type == HINT_MESSAGE_DEVICE_ACTION:
        return hint_msg_handler.device_action(*args)
    elif message_type == HINT_MESSAGE_SUB_DEVICE_ACTION:
        return hint_msg_handler.sub_device_action(*args)
    else:
        return {"error": "does not exist"}
