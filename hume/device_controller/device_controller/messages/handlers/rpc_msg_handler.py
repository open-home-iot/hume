import logging

from device_controller.device.model import Device
from device_controller.util import storage

LOGGER = logging.getLogger(__name__)


def confirm_attach(message_content):
    """
    Called on HINT controller confirming an attached device.

    :param dict message_content:
    :return:
    """
    LOGGER.debug(f"RPC request received: {message_content}")

    # Resolve device
    uuid = message_content["uuid"]
    device = storage.get(Device, uuid)
    LOGGER.debug(f"found device with properties: {device}")

    # Mark device as attached
    device.attached = True
    storage.save(device)


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
