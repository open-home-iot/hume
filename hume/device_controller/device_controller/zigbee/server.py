from device_controller.utility.broker import Broker
from device_controller.utility.dispatch.dispatcher import Dispatch
from device_controller.utility.server_base import ServerBase
from device_controller.zigbee import decoder
from device_controller.zigbee.messages import ZBIn


DEVICE_EVENT_TOPIC = "device_events"


class ZigbeeServer(ServerBase, Dispatch):
    """
    ZigbeeServer listens for device_controller messages on the ZigBee network.
    """
    dispatch_id = "ZigbeeServer"

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
        if isinstance(decoded_message, ZBIn.DeviceCapabilities):
            # TODO cast to local subscriptions
            pass
        elif isinstance(decoded_message, ZBIn.DeviceEvent):
            # TODO cast to local subscriptions
            pass
        elif isinstance(decoded_message, ZBIn.DeviceActionResponse):
            # TODO notify RPC that a response has been received
            pass
        elif isinstance(decoded_message, ZBIn.DeviceHeartbeat):
            # TODO cast to local subscriptions
            pass

    def on_dispatch(self, message):
        print("Zigbee server got dispatch: {}".format(message))

    def set_dispatch_tier(self, dispatch_tier: str) -> str:
        print("Zigbee server setting dispatch tier: {}".format(dispatch_tier))
        self.dispatch_tier = dispatch_tier
        return self.dispatch_tier
