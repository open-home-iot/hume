from device_controller.utility.dispatch.dispatcher import Dispatch
from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase


class ConfigServer(ServerBase, Dispatch):
    """
    This server handles configuration scheduling, any conditions (such as state-
    dependent schedules actions), and limit-triggering.
    """
    dispatch_id = "ConfigServer"

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
        pass

    def stop(self):
        """
        Not needed for now.
        """
        pass

    def on_dispatch(self, message):
        print("Config server got dispatch: {}".format(message))

    def set_dispatch_tier(self, dispatch_tier: str) -> str:
        print("Config server setting dispatch tier: {}".format(dispatch_tier))
        self.dispatch_tier = dispatch_tier
        return self.dispatch_tier
