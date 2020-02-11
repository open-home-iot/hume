from device_controller.utility.broker import Broker


class LocalStorage:

    _broker: Broker

    def __init__(self, broker):
        self._broker = broker