from broker.broker import Broker


DEVICE_EVENT_TOPIC = "device_events"


class ZigbeeServer:
    """
    ZigbeeServer listens for device messages on the ZigBee network.
    """
    broker: Broker

    def __init__(self, broker=None):
        """
        :param broker: broker instance shared among applications.
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