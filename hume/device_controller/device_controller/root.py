import logging

from device_controller.utility import storage
from device_controller.utility.dispatch import dispatcher
from device_controller.utility.broker import Broker
from device_controller.utility import log
from device_controller.library.server_base import ServerBase

from device_controller.device.server import DeviceServer
from device_controller.zigbee.server import ZigbeeServer
from device_controller.rpc.server import RPCServer
from device_controller.configuration.server import ConfigServer


SERVICE_NAME = "device_controller"

LOGGER = logging.getLogger(__name__)


class RootApp(ServerBase):
    """
    A wrapping class for all HUME sub-applications, ensures start order and
    initial dependency injections.
    """

    dispatch_tier = "root_app"

    def __init__(self, cli_args=None, log_level=logging.INFO):
        """
        :param cli_args: arguments provided on start
        :param log_level: log level of the device controller application
        """
        LOGGER.debug("root __init__")

        self.cli_args = cli_args

        log.set_up_logging(log_level)

        self.broker = Broker()

        storage.initialize(self.broker, SERVICE_NAME)

        self.zigbee_server = ZigbeeServer(broker=self.broker)
        self.rpc_server = RPCServer(broker=self.broker)
        self.config_server = ConfigServer(broker=self.broker)
        self.device_server = DeviceServer(broker=self.broker)

    def start(self):
        """
        Starts the RootApp and all its sub-applications.
        """
        LOGGER.info("RootApp start")
        # core start
        self.broker.start()

        # register to dispatcher
        dispatcher.register(self.dispatch_tier, self.zigbee_server)
        dispatcher.register(self.dispatch_tier, self.rpc_server)
        dispatcher.register(self.dispatch_tier, self.config_server)
        dispatcher.register(self.dispatch_tier, self.device_server)

        # application start
        self.zigbee_server.start()
        self.rpc_server.start()
        self.config_server.start()
        self.device_server.start()

    def stop(self):
        """
        Stops all RootApp sub-applications in order to clean up used resources.
        """
        LOGGER.info("RootApp stop")
        # application stop
        self.zigbee_server.stop()
        self.rpc_server.stop()
        self.config_server.stop()
        self.device_server.stop()

        # core stop
        self.broker.stop()
