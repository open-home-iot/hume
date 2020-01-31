from device_controller.utility.broker import Broker
from device_controller.utility.server_base import ServerBase
from device_controller.zigbee import decoder


DEVICE_EVENT_TOPIC = "device_events"


class ZigbeeServer(ServerBase):
    """
    ZigbeeServer listens for device_controller messages on the ZigBee network.
    """
    broker: Broker

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        """
        self.broker = broker

    def start(self):
        """
        Starts the ZigbeeServer.
        """
        print("ZigbeeServer start")

    def stop(self):
        """
        Stops the ZigbeeServer and releases its resources.
        """
        print("ZigbeeServer stop")

    def on_device_message(self, message: bytes):
        """
        Handler function for messages sent from a device.

        :param bytes message: message sent from a device
        """
        # Decode message
        decoded_message = decoder.decode(message)

        # Determine which message was received
