import logging

from device_controller.utility.broker import Broker
from device_controller.utility.procedures import Procedure
from device_controller.utility.dispatch import Dispatch

from device_controller.device.model import Device, DeviceAction, DeviceState, \
    DeviceStatus
from device_controller.utility import storage

from device_controller.library.server_base import ServerBase


LOGGER = logging.getLogger(__name__)


class DeviceServer(ServerBase, Dispatch, Procedure):
    """
    This server handles configuration scheduling, any conditions (such as
    storage-dependent scheduler actions), and limit-triggering.
    """
    dispatch_id = "DeviceServer"

    def __init__(self, broker: Broker = None):
        """
        :param broker: application wide broker instance
        """
        LOGGER.debug("device server __init__")

        self.broker = broker

    def start(self):
        """
        Starts up the device server.
        """
        LOGGER.debug("device server start")

        storage.register(Device)
        storage.register(DeviceAction)
        storage.register(DeviceState)
        storage.register(DeviceStatus)
        # TODO get configuration from storage and load it into memory

    def stop(self):
        """
        Not needed for now.
        """
        pass

    def on_dispatch(self, message):
        """
        Called on message dispatched to application.

        :param message: dispatched message
        """
        LOGGER.debug(f"device server dispatched message: {message}")

    def start_procedure(self, *args):
        """
        Start procedure with provided arguments.

        :param args: arguments
        """
        LOGGER.debug(f"device server start procedure with arguments: {args}")
