from device_controller.utility.dispatch import dispatcher
from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase
from device_controller.zigbee.server import ZigbeeServer
from device_controller.rpc.server import RPCServer
from device_controller.configuration.server import ConfigServer


class RootApp(ServerBase):
    """
    A wrapping class for all HUME sub-applications, ensures start order and
    initial dependency injections.
    """
    cli_args = None

    # Pub/Sub (global or local) and RPC.
    broker: Broker

    dispatch_tier = "root_app"

    zigbee_server: ZigbeeServer
    rpc_server: RPCServer
    config_server: ConfigServer

    def __init__(self, cli_args=None):
        """
        :param cli_args: arguments provided on start
        """
        self.cli_args = cli_args

        self.broker = Broker()

        self.zigbee_server = ZigbeeServer(broker=self.broker)
        self.rpc_server = RPCServer(broker=self.broker)
        self.config_server = ConfigServer(broker=self.broker)

    def start(self):
        """
        Starts the RootApp and all its sub-applications.
        """
        print("RootApp start")
        # core start
        self.broker.start()

        # register to dispatcher
        dispatcher.register(self.dispatch_tier, self.zigbee_server)
        dispatcher.register(self.dispatch_tier, self.rpc_server)
        dispatcher.register(self.dispatch_tier, self.config_server)

        # application start
        self.zigbee_server.start()
        self.rpc_server.start()
        self.config_server.start()

    def stop(self):
        """
        Stops all RootApp sub-applications in order to clean up used resources.
        """
        print("RootApp stop")
        # application stop
        self.zigbee_server.stop()
        self.rpc_server.stop()
        self.config_server.stop()

        # core stop
        self.broker.stop()
