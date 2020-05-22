import logging

from .handlers import rpc_msg_handler, hint_msg_handler


LOGGER = logging.getLogger(__name__)

HINT_MESSAGE_CONFIRM_ATTACH = 0


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


def rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("messages got new rpc request")
    return rpc_msg_handler.handle_rpc_request(rpc_req)


def hint_message(message_type, message_content):
    """
    Called on incoming HINT messages.

    :param int message_type: type of message
    :param dict message_content: message content
    :return dict | None: may return an answer in dict form
    """
    LOGGER.info("got new message from HINT")

    if message_type == HINT_MESSAGE_CONFIRM_ATTACH:
        return hint_msg_handler.confirm_attach(message_content)
    else:
        return {"error": "does not exist"}
