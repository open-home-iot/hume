from device_controller.utility.broker import Broker
from device_controller.utility.procedures import run_in_procedure
from device_controller.utility.procedures import Procedure
from device_controller.utility.dispatch import Dispatch

from device_controller.library.server_base import ServerBase


class DeviceServer(ServerBase, Dispatch, Procedure):
    """
    This server handles configuration scheduling, any conditions (such as
    storage-dependent scheduler actions), and limit-triggering.
    """
    dispatch_id = "DeviceServer"

    broker: Broker

    # TODO load configuration from storage into memory on start
    _device_config = None

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        """
        self.broker = broker

    def start(self):
        """
        Starts up the configuration server.
        """
        # TODO get configuration from storage and load it into memory
        # TODO create base configuration for the device_controller
        run_in_procedure(self, "device server bitches!")

    def stop(self):
        """
        Not needed for now.
        """
        pass

    def on_dispatch(self, message):
        print("Device server got dispatch: {}".format(message))

    def start_procedure(self, *args):
        print("device server start_procedure called with args: {}".format(args))
