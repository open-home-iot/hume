import json
import logging


LOGGER = logging.getLogger(__name__)


def handle_rpc_request(rpc_req):
    """
    Called on incoming RPC requests

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.debug(f"RPC request received: {rpc_req}")

    return json.dumps({"result": "OK"}).encode('utf-8')


class BaseDeviceProperties:
    pass


# IN
class RPCIn:

    class DeviceAction(BaseDeviceProperties):
        pass

    class DeviceConfiguration(BaseDeviceProperties):
        pass


# OUT
class RPCOut:
    pass  # Any at all?
