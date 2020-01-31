from device_controller.procedures.handler import ProcedureHandler
from device_controller.rpc import decoder
from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase

DEVICE_CONTROLLER_QUEUE = "device_controller"


class RPCServer(ServerBase):
    """
    Takes care of RPC actions, both incoming and outgoing.
    """

    broker: Broker
    procedure_handler: ProcedureHandler

    def __init__(self, broker=None, procedure_handler=None):
        """
        :param broker: application wide broker instance
        :param procedure_handler: application wide procedure handler instance
        """
        self.broker = broker
        self.procedure_handler = procedure_handler

    def start(self):
        """
        Initializes any resources that the RPCHandler depends on.
        """
        self.broker.enable_rpc_server(
            DEVICE_CONTROLLER_QUEUE,
            self.on_rpc_request
        )

    def stop(self):
        """
        Cleanup of any RPCHandler specific resources.
        """
        pass

    def on_rpc_request(self, message: bytes):
        """
        Handler function for incoming RPC requests. Must always return.

        :param bytes message:
        :return: bytes
        """
        # Decode the JSON formatted message
        decoded_message = decoder.decode(message)

        # Determine which procedure shall be invoked

