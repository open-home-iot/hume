import json
import logging


LOGGER = logging.getLogger(__name__)


def attach(message_content):
    """
    Called on incoming RPC requests

    :param dict message_content: incoming rpc request
    :return bytes: rpc response
    """
    LOGGER.debug(f"device attach rpc message content: {message_content}")

    # TODO send HTTP request to HINT


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
