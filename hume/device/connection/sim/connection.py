import logging

from device.connection.gci import GCI
from device.connection.sim.specs import BASIC_LED_CAPS
from device.models import Device


LOGGER = logging.getLogger(__name__)


def discovered_device(device_dict):
    return Device(name=device_dict["name"],
                  # simulated devices have no address, change format to differ
                  # between UUID and address.
                  address=device_dict["uuid"].replace('-', ':'),
                  uuid=device_dict["uuid"])


class SimConnection(GCI):

    def __init__(self):
        super().__init__()
        # device.uuid -> Device
        self.device_registry = dict()

    def discover(self, on_devices_discovered):
        LOGGER.info("starting device discovery")
        on_devices_discovered(self._unattached_devices)

    @property
    def _unattached_devices(self) -> [Device]:
        # Ok for now, needs to be changed when new device types are added to
        # the sim.
        if len(self.device_registry) == 0:
            return [discovered_device(BASIC_LED_CAPS)]

    def is_connected(self, device: Device) -> bool:
        return self.device_registry.get(device.uuid) is not None

    def connect(self, device: Device) -> bool:
        LOGGER.info(f"connecting to device {device.address}")

        self.device_registry[device.uuid] = device

        return True

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.address}")

        self.device_registry.pop(device.uuid)

        return True

    def disconnect_all(self) -> bool:
        self.device_registry = dict()
        return True

    def send(self, msg: GCI.Message, device: Device) -> bool:
        LOGGER.debug(f"sending device {device.address} message {msg.content}")



        return True

    def notify(self, callback: callable, device: Device):
        # No need to implement, send all messages to 'incoming_message' for
        # now.
        ...
