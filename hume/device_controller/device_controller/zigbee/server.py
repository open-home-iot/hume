import logging

from device_controller.utility.broker import Broker
from device_controller.utility.dispatch import Dispatch
from device_controller.utility.procedures import Procedure
from device_controller.library.server_base import ServerBase
from device_controller.zigbee import decoder
from device_controller.zigbee.messages import ZBIn

LOGGER = logging.getLogger(__name__)

TOPIC_DEVICE_EVENTS = "local_topic_device_events"


class ZigbeeServer(ServerBase, Dispatch, Procedure):
    """
    ZigbeeServer listens for device_controller messages on the ZigBee network.
    """
    dispatch_id = "ZigbeeServer"

    broker: Broker

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        """
        LOGGER.debug("ZigbeeServer __init__")

        self.broker = broker

    def start(self):
        """
        Starts the ZigbeeServer.
        """
        LOGGER.info("ZigbeeServer start")

    def stop(self):
        """
        Stops the ZigbeeServer and releases its resources.
        """
        LOGGER.info("ZigbeeServer stop")

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

    def start_procedure(self, *args):
        print("zigbee server start procedure with args: {}".format(args))
