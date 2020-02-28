import logging
from datetime import datetime

from device_controller.device.model import DeviceStatus, Device
from device_controller.utility import storage
from device_controller.utility.broker import Broker
from device_controller.utility.procedures import Procedure
from device_controller.utility.dispatch import Dispatch

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
        LOGGER.info("DeviceServer start")

        # Trying some queries to the storage
        storage.set_obj(DeviceStatus(1, datetime.now(), "inactive"))
        storage.set_obj(DeviceStatus(2, datetime.now(), "napping"))
        storage.set_obj(DeviceStatus(1, datetime.now(), "active"))
        storage.set_obj(DeviceStatus(4, datetime.now(), "took a nap"))
        storage.set_obj(DeviceStatus(5, datetime.now(), "exploded"))
        storage.set_obj(Device(name="temp", type=0))
        storage.set_obj(Device(name="lamp", type=1))

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
