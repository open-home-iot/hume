import logging

from device.connection.gci import GCI
from device.connection.sim.specs import BASIC_LED_CAPS
from device.models import Device


LOGGER = logging.getLogger(__name__)


def discovered_device(device_dict):
    return Device(name=device_dict["name"],
                  address=device_dict["uuid"],
                  uuid=device_dict["uuid"])


class SimConnection(GCI):

    def __init__(self):
        super().__init__()
        # device.uuid -> Device
        self.device_registry = dict()

    def discover(self, on_devices_discovered):
        LOGGER.info("starting device discovery")
        on_devices_discovered(self._unattached_devices())

    def _unattached_devices(self) -> [Device]:
        # Ok for now, needs to be changed when new device types are added to
        # the sim.
        if len(self.device_registry) == 0:
            return [discovered_device(BASIC_LED_CAPS)]

    def connect(self, device: Device) -> bool:
        LOGGER.info(f"connecting to device {device.address}")

        return True

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.address}")

        return True

    def disconnect_all(self) -> bool:
        return True

    def send(self, msg: GCI.Message, device: Device) -> bool:
        LOGGER.debug(f"sending device {device.address} message {msg.content}")

        return True

    def notify(self, callback: callable, device: Device):
        ...
