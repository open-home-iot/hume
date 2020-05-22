import logging

from .handlers import device_msg_handler, rpc_msg_handler


LOGGER = logging.getLogger(__name__)

DEVICE_MESSAGE_ATTACH = 0


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
    return rpc_msg_handler.handle_rpc_request(rpc_req)


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
