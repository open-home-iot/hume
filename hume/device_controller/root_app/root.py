from utility.broker import Broker
from device_procedures.handler import ProcedureHandler
from zigbee_server.server import ZigbeeServer


class RootApp:
    """
    A wrapping class for all HUME sub-applications, ensures start order and
    dependency injections.
    """
    cli_args = None

    broker: Broker

    zigbee_server: ZigbeeServer
    procedure_handler: ProcedureHandler

    def __init__(self, cli_args=None):
        """
        :param cli_args: arguments provided on start
        """
        self.cli_args = cli_args

    def start(self):
        """
        Starts the RootApp and all its sub-applications.
        """
        print("RootApp start")
        self.broker = Broker()
        self.broker.start()

        self.zigbee_server = ZigbeeServer(broker=self.broker)
        self.zigbee_server.start()

        self.procedure_handler = ProcedureHandler(broker=self.broker)
        self.procedure_handler.start()

    def stop(self):
        """
        Stops all RootApp sub-applications in order to clean up used resources.
        """
        print("RootApp stop")
        self.broker.stop()
        self.zigbee_server.stop()
        self.procedure_handler.stop()
