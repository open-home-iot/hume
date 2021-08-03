from device.connection.gci import GCI
from device.models import Device


class BLEConnection(GCI):

    def __init__(self):
        super().__init__()

    def discover(self) -> [Device]:
        pass

    def connect(self, device: Device) -> bool:
        pass

    def send(self, msg: GCI.Message, device: Device) -> bool:
        pass

    def disconnect(self, device: Device):
        pass

    def notify(self, callback: callable(GCI.Message), device: Device):
        pass
