import logging

from device_controller.messages.handlers import device, rpc


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


def rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("messages got new rpc request")
    return rpc.handle_rpc_request(rpc_req)


def device_message(message):
    """
    Called on incoming device messages.

    :param bytes message: incoming device message
    :return: may return an answer
    """
    LOGGER.info("messages got new device message")
    return device.handle_device_message(message)
