import logging


LOGGER = logging.getLogger(__name__)


def handle_rpc_request(rpc_req):
    """
    Called on incoming RPC requests

    :param bytes rpc_req: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.info("rpc in message handler for rpc request")

    return b'some reply'


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
