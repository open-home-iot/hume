from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase


class ConfigServer(ServerBase):
    """
    This server handles configuration scheduling, any conditions (such as state-
    dependent schedules actions), and limit-triggering.
    """
    broker: Broker

    # TODO load configuration from storage into memory on start
    _active_configuration = None

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        :param procedure_handler: application wide procedure handler instance
        """
        self.broker = broker

    def start(self):
        """
        Starts up the configuration server.
        """
        # TODO get configuration from storage and load it into memory
        pass

    def stop(self):
        """
        Not needed for now.
        """
        pass
