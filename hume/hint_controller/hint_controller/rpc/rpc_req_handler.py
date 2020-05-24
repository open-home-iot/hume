import json
import logging

from hint_controller.hint import application as hint


LOGGER = logging.getLogger(__name__)

# DEVICE ORIGINATED
DEVICE_MESSAGE_ATTACH = 0


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

    # TODO, result should depend on outcome
    return json.dumps({"result": "OK"}).encode('utf-8')


def attach(message_content):
    """
    Called when a new device has sent an attach message.

    :param dict message_content: incoming rpc request
    """
    LOGGER.debug(f"device attach rpc message content: {message_content}")

    hint.attach(message_content)
