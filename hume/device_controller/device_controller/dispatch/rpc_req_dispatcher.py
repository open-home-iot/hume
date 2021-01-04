import json
import logging


LOGGER = logging.getLogger(__name__)


"""
This module acts as a starting point for HINT controller originated RPC reqs.
"""


def incoming_rpc_request(rpc_req):
    """
    :param bytes rpc_req: incoming rpc request
    :type rpc_req: bytes
    """
    LOGGER.info("new RPC request received")

    decoded_req = json.loads(rpc_req.decode('utf-8'))

    result = {"result": "OK"}

    # TODO, more results should depend on outcome
    return json.dumps(result).encode('utf-8')
