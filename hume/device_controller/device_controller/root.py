from device_controller.utility.broker import Broker
from device_controller.procedures.handler import ProcedureHandler
from device_controller.zigbee.server import ZigbeeServer
from device_controller.rpc.server import RPCServer
from device_controller.configuration.server import ConfigServer


class RootApp:
    """
    A wrapping class for all HUME sub-applications, ensures start order and
    initial dependency injections.
    """
    cli_args = None

    broker: Broker
    procedure_handler: ProcedureHandler

    zigbee_server: ZigbeeServer
    rpc_server: RPCServer
    config_server: ConfigServer

    def __init__(self, cli_args=None):
        """
        :param cli_args: arguments provided on start
        """
        self.cli_args = cli_args

        self.broker = Broker()

        self.procedure_handler = ProcedureHandler()

        self.zigbee_server = ZigbeeServer(
            broker=self.broker, procedure_handler=self.procedure_handler
        )
        self.rpc_server = RPCServer(
            broker=self.broker, procedure_handler=self.procedure_handler
        )
        self.config_server = ConfigServer(
            broker=self.broker, procedure_handler=self.procedure_handler
        )

    def start(self):
        """
        Starts the RootApp and all its sub-applications.
        """
        print("RootApp start")
        # core start
        self.broker.start()

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
