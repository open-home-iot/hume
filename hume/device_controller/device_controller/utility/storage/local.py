from device_controller.utility.broker import Broker


_broker: Broker


def initialize(broker):
    global _broker
    _broker = broker
