import logging

from device_controller.configuration.model import DeviceConfiguration
from device_controller.utility.broker import Broker
from device_controller.utility.dispatch import Dispatch
from device_controller.utility.procedures import Procedure
from device_controller.library.server_base import ServerBase
from device_controller.utility import storage


LOGGER = logging.getLogger(__name__)


class ConfigServer(ServerBase, Dispatch, Procedure):
    """
    This server handles configuration scheduling, any conditions (such as
    storage-dependent scheduler actions), and limit-triggering.
    """

    dispatch_id = "ConfigServer"

    def __init__(self, broker: Broker = None):
        """
        :param broker: application wide broker instance
        """
        LOGGER.debug("configuration server __init__")

        self.broker = broker

    def start(self):
        """
        Starts up the configuration server.
        """
        LOGGER.info("ConfigurationServer start")

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
        LOGGER.debug(f"config server dispatched message: {message}")

    def start_procedure(self, *args):
        """
        Start procedure with provided arguments.

        :param args: arguments
        """
        LOGGER.debug(f"config server start procedure with arguments: {args}")
