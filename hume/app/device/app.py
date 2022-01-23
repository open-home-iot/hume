import logging

from app.abc import App
from app.device.connection.connection import DeviceConnection
from app.device.connection.gci import GCI
from app.device.models import Device, DeviceHealth
from app.device.defs import TRANSPORT_BLE, TRANSPORT_SIM
from defs import CLI_SIMULATION
from util.storage import DataStore


LOGGER = logging.getLogger(__name__)


class DeviceMessage:
    CAPABILITY = 0
    ACTION_STATEFUL = 1
    HEARTBEAT = 2


class DeviceApp(App):

    def __init__(self, cli_args, storage: DataStore):
        super().__init__()
        self.cli_args = cli_args
        self.storage = storage
        self.connection = DeviceConnection(cli_args)

        self._registered_callback = lambda device, msg_type, msg: \
            LOGGER.warning("no registered callback to propagate device msg to")

    """
    App LCM
    """

    def pre_start(self):
        LOGGER.info("Device pre_start")

        self.storage.register(Device)
        self.storage.register(DeviceHealth)

    def start(self):
        LOGGER.info("Device start")
        self.connection.start()
        self._connect_attached_devices()

    def post_start(self):
        LOGGER.info("Device post_start")

    def pre_stop(self):
        LOGGER.info("Device pre_stop")
        if not self.connection.simulation:
            self.connection.ble.disconnect_all()

    def stop(self):
        LOGGER.info("Device stop")
        self.connection.stop()

    def post_stop(self):
        LOGGER.info("Device post_start")

    """
    Public
    """

    def register_callback(self, callback):
        """
        Registers a callback with the device app to be called when a device has
        sent the HUME a message.

        :param callback: callable(Device, int, bytearray)
        :return:
        """
        LOGGER.info("registering callback")
        self._registered_callback = callback

    def discover(self, callback):
        """
        Discovers devices in the HUME's local area.
        """
        if self.connection.simulation:
            self.connection.sim.discover(callback)
        else:
            self.connection.ble.discover(callback)

    def request_capabilities(self, device) -> bool:
        """
        Requests capabilities of the input device, usually the start of an
        attach procedure. Returns true if the request could be sent.
        """
        if self._connect_to(device):
            self._request_capabilities(device)
            return True
        else:
            return False

    def detach(self, device):
        pass

    def stateful_action(self, device, **kwargs):
        pass

    def reset(self):
        pass

    """
    Private
    """

    def _on_device_message(self,
                           device: Device,
                           message_type: int,
                           body: bytearray):
        """
        Called when a connected device sends HUME a message.
        """
        LOGGER.debug(f"received device message from {device.uuid[:4]}")
        self._registered_callback(device, message_type, body)

    def _connect_attached_devices(self):
        """
        Establishes a connection with all attached devices.
        """
        LOGGER.info("connecting attached devices")

        devices = self.storage.get_all(Device)
        for device in devices:
            if device.attached:
                self._connect_to(device)

    def _connect_to(self, device: Device) -> bool:
        """
        Checks if the input device is already connected. If not, the device
        is connected to.
        """
        LOGGER.debug(f"connecting to device {device.uuid[:4]}")

        if self.connection.simulation and device.transport == TRANSPORT_SIM:
            self.connection.sim.connect(device)
            self.connection.sim.notify(self._on_device_message, device)
        elif (not self.connection.ble.is_connected(device) and
              device.transport == TRANSPORT_BLE):
            if not self.connection.ble.connect(device):
                LOGGER.error(f"failed to connect to device "
                             f"{device.uuid[:4]}")
                return False

            self.connection.ble.notify(self._on_device_message, device)

        return True

    def _request_capabilities(self, device: Device):
        """
        Requests the capabilities of the input device.
        """
        message = GCI.Message(f"{DeviceMessage.CAPABILITY}")
        if self.connection.simulation:
            self.connection.sim.send(message, device)
        else:
            self.connection.ble.send(message, device)
