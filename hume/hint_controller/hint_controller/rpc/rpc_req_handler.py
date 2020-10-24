import json
import logging

from hint_controller.hint import application as hint


LOGGER = logging.getLogger(__name__)

# DEVICE ORIGINATED
DEVICE_MESSAGE_ATTACH = 0
DEVICE_MESSAGE_DEVICE_EVENT = 1
DEVICE_MESSAGE_SUB_DEVICE_EVENT = 2


def incoming_rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("new RPC request received")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    if decoded_req["message_type"] == DEVICE_MESSAGE_ATTACH:
        attach(decoded_req["message_content"])
    elif decoded_req["message_type"] == DEVICE_MESSAGE_DEVICE_EVENT:
        device_event(decoded_req["message_content"])
    elif decoded_req["message_type"] == DEVICE_MESSAGE_SUB_DEVICE_EVENT:
        sub_device_event(decoded_req["message_content"])

    # TODO, result should depend on outcome
    return json.dumps({"result": "OK"}).encode('utf-8')


def attach(message_content):
    """
    Called when a new device has sent an attach message.

    :param dict message_content: incoming rpc request
    """
    LOGGER.debug(f"device attach rpc message content: {message_content}")

    hint.attach(message_content)


def device_event(message_content):
    """
    Called when a device has send an event.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"device event rpc message content: {message_content}")

    hint.device_event(message_content)


def sub_device_event(message_content):
    """
    Called when a sub device has send an event.

    :param message_content:
    :return:
    """
    LOGGER.debug(f"sub device event rpc message content: {message_content}")

    hint.sub_device_event(message_content)
