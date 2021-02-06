import json
import logging


LOGGER = logging.getLogger(__name__)


"""
This module acts as a starting point for device controller originated RPC reqs.
"""


def incoming_rpc_request(rpc_req):
    """
    Called on incoming RPC requests.

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("new RPC request received")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    result = {"result": "ok"}

    return json.dumps(result).encode('utf-8')
