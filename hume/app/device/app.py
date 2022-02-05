import logging

from app.abc import App
from app.device.connection.connector import DeviceConnector
from app.device.connection.gdci import GDCI
from app.device.models import Device, DeviceHealth
from app.device.defs import DeviceMessage
from util.storage import DataStore


LOGGER = logging.getLogger(__name__)


class DeviceApp(App):

    def __init__(self, cli_args, storage: DataStore):
        super().__init__()
        self.cli_args = cli_args
        self.storage = storage
        self.device_connector = DeviceConnector(cli_args)

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
        self.device_connector.start()
        self._connect_attached_devices()

    def post_start(self):
        LOGGER.info("Device post_start")

    def pre_stop(self):
        LOGGER.info("Device pre_stop")

    def stop(self):
        LOGGER.info("Device stop")
        self.device_connector.stop()

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
        self.device_connector.discover(callback)

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

        if not self.device_connector.is_connected(device):
            if not self.device_connector.connect(device):
                LOGGER.error(f"failed to connect to device "
                             f"{device.uuid[:4]}")
                return False

            self.device_connector.notify(self._on_device_message, device)

        return True

    def _request_capabilities(self, device: Device):
        """
        Requests the capabilities of the input device.
        """
        message = GDCI.Message(f"{DeviceMessage.CAPABILITY}")
        self.device_connector.send(message, device)
