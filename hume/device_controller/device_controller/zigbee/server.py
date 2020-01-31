from device_controller.procedures.handler import ProcedureHandler
from device_controller.utility.broker import Broker, Dispatch
from device_controller.zigbee import decoder


DEVICE_ACTION_DISPATCH = "device_action_dispatch"
DEVICE_EVENT_TOPIC = "device_events"


class ZigbeeServer(Dispatch):
    """
    ZigbeeServer listens for device_controller messages on the ZigBee network.
    """
    broker: Broker
    procedure_handler: ProcedureHandler

    def __init__(self, broker=None, procedure_handler=None):
        """
        :param broker: utility instance shared among applications.
        """
        self.broker = broker
        self.procedure_handler = procedure_handler

    def start(self):
        """
        Starts the ZigbeeServer.
        """
        print("ZigbeeServer start")
        self.broker.register_dispatch(self, DEVICE_ACTION_DISPATCH)

    def stop(self):
        """
        Stops the ZigbeeServer and releases its resources.
        """
        print("ZigbeeServer stop")

    def on_device_event(self, message: bytes):
        """
        Handler function for incoming device events.

        :param bytes message: message sent from a device
        """
        # Decode message
        decoded_message = decoder.decode(message)

        # Determine which procedure shall be started

    def dispatch(self, message: dict):
        """
        Handles a message dispatch.

        :param dict message: message to dispatch
        """
        pass
