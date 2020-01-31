from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase


class ConfigServer(ServerBase):
    """
    This server handles configuration scheduling, any conditions (such as state-
    dependent schedules actions), and limit-triggering.
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
        Starts the configuration server.
        """
        pass

    def stop(self):
        """
        Stops the configuration server and releases all its resources.
        """
        pass
