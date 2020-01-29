from broker.broker import Broker
from zigbee_server.server import DEVICE_EVENT_TOPIC


DEVICE_ACTION_RPC_QUEUE = "device_actions"


class ProcedureHandler:
    """
    ProcedureHandler is meant to be the core interface for all device
    communication; be it device or HINT originated. At its top, the handler
    subscribes to both device actions posted via a RabbitMQ RPC queue and
    the device controller internal subscription for new device events.
    """
    broker: Broker

    def __init__(self, broker=None):
        """
        :param broker: broker instance shared among applications
        """
        self.broker = broker

    def start(self):
        """
        Starts the ProcedureHandler and prepares it for operation.
        """
        self.broker.enable_rpc_server(DEVICE_ACTION_RPC_QUEUE,
                                      self.device_action)
        self.broker.subscribe_local(DEVICE_EVENT_TOPIC,
                                    self.device_event)

    def stop(self):
        """
        Releases all resources consumed by the ProcedureHandler.
        """
        print("ProcedureHandler stop")

    def device_action(self, message: bytes):
        """
        Invoked on a new device action to perform, as received from the device
        action RPC queue.

        :param message:
        """
        pass

    def device_event(self, headers, message):
        """
        Invoked on a new device event, as received from a device via the
        ZigbeeServer.

        :param headers:
        :param message:
        """
        pass
