import json
import logging

from .handlers import device_msg_handler, rpc_msg_handler
from .definitions import *


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

    if decoded_req["message_type"] == HINT_MESSAGE_CONFIRM_ATTACH:
        rpc_msg_handler.confirm_attach(decoded_req["message_content"])
    elif decoded_req["message_type"] == HINT_MESSAGE_DEVICE_CONFIGURATION:
        rpc_msg_handler.device_configuration(decoded_req["message_content"])

    # TODO, result should depend on outcome
    return json.dumps({"result": "OK"}).encode('utf-8')


def incoming_device_message(message_type, message_content):
    """
    Called on incoming device messages.

    :param int message_type: type of message
    :param dict message_content: message content
    :return dict | None: may return an answer in dict form
    """
    LOGGER.info("messages got new device message")

    if message_type == DEVICE_MESSAGE_ATTACH:
        return device_msg_handler.attach(message_content)
    else:
        return {"error": "does not exist"}
