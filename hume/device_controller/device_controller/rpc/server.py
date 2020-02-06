from device_controller.rpc import decoder
from device_controller.rpc.requests import RPCIn
from device_controller.utility.broker import Broker
from device_controller.utility.dispatch import Dispatch
from device_controller.utility.procedures import run_in_procedure, Procedure
from device_controller.library.server_base import ServerBase


DEVICE_CONTROLLER_QUEUE = "rpc_device_controller"


class RPCServer(ServerBase, Dispatch, Procedure):
    """
    Takes care of RPC actions, both incoming and outgoing.
    """
    dispatch_id = "RPCServer"

    broker: Broker

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        """
        self.broker = broker

    def start(self):
        """
        Initializes any resources that the RPCHandler depends on.
        """
        self.broker.enable_rpc_server(
            DEVICE_CONTROLLER_QUEUE,
            self.on_rpc_request
        )
        run_in_procedure(self, "yee haaaaa")

    def stop(self):
        """
        Cleanup of any RPCHandler specific resources.
        """
        pass

    def on_rpc_request(self, message: bytes):
        """
        Handler function for incoming RPC requests. Must always return.

        :param bytes message: incoming message
        :return bytes response: response to the RPC request
        """
        # Decode the JSON formatted message
        decoded_message = decoder.decode(message)

        # Determine which request was received
        if isinstance(decoded_message, RPCIn.DeviceAttach):
            # TODO cast to local subscriptions or direct call, depends on
            # TODO where the RPC calls will be blocked waiting for a response
            pass
        elif isinstance(decoded_message, RPCIn.DeviceAction):
            # TODO cast to local subscriptions or direct call, depends on
            # TODO where the RPC calls will be blocked waiting for a response
            pass
        elif isinstance(decoded_message, RPCIn.DeviceConfiguration):
            # TODO cast to local subscriptions or direct call, depends on
            # TODO where the RPC calls will be blocked waiting for a response
            pass

        return  # response

    def on_dispatch(self, message):
        print("RPC server got dispatch: {}".format(message))

    def start_procedure(self, *args):
        print("rpc server procedure started with args: {}".format(args))
