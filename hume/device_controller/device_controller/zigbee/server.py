from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker
from device_controller.zigbee.handler import ZigbeeHandler

DEVICE_EVENT_TOPIC = "device_events"


class ZigbeeServer:
    """
    ZigbeeServer listens for device_controller messages on the ZigBee network.
    """
    broker: Broker
    procedure_handler: ProcedureHandler

    zigbee_handler: ZigbeeHandler

    def __init__(self, broker=None, procedure_handler=None):
        """
        :param broker: utility instance shared among applications.
        """
        self.broker = broker
        self.procedure_handler = procedure_handler

        self.zigbee_handler = ZigbeeHandler(
            broker=self.broker, procedure_handler=self.procedure_handler
        )

    def start(self):
        """
        Starts the ZigbeeServer.
        """
        print("ZigbeeServer start")
        self.zigbee_handler.start()

    def stop(self):
        """
        Stops the ZigbeeServer and releases its resources.
        """
        print("ZigbeeServer stop")
        self.zigbee_handler.stop()
