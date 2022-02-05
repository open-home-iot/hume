import logging

from app.abc import App
from app.device.connection.connector import DeviceConnector
from app.device.connection.gdci import GDCI
from app.device.models import Device, DeviceHealth
from app.device.defs import DeviceMessage
from util.storage import DataStore


LOGGER = logging.getLogger(__name__)


class DeviceApp(App):

    def __init__(self, cli_args: dict, storage: DataStore):
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
        LOGGER.info("device app pre_start")

        self.storage.register(Device)
        self.storage.register(DeviceHealth)

    def start(self):
        LOGGER.info("device app start")
        self.device_connector.start()
        self._connect_attached_devices()

    def post_start(self):
        LOGGER.info("device app post_start")

    def pre_stop(self):
        LOGGER.info("device app pre_stop")

    def stop(self):
        LOGGER.info("device app stop")
        self.device_connector.stop()

    def post_stop(self):
        LOGGER.info("device app post_start")

    """
    Public
    """

    def register_callback(self, callback: callable):
        """
        Registers a callback with the device app to be called when a device has
        sent the HUME a message.

        callback: callable(Device, int, bytearray)
        """
        LOGGER.info("registering callback")
        self._registered_callback = callback

    def discover(self, callback: callable):
        """
        Discovers devices in the HUME's local area.
        """
        LOGGER.info("discovering devices")
        self.device_connector.discover(callback)

    def request_capabilities(self, device: Device) -> bool:
        """
        Requests capabilities of the input device, usually the start of an
        attach procedure. Returns True if the request could be sent.
        """
        LOGGER.info(f"requesting device {device.uuid[:4]} capabilities")
        if self._connect_to(device):
            return self._request_capabilities(device)

        return False

    def detach(self, device: Device):
        """
        Detach the input device, disconnect and forget it.
        """
        LOGGER.info(f"detaching device {device.uuid[:4]}")
        if self.device_connector.is_connected(device):
            self.device_connector.disconnect(device)
            # not much to do if this fails, at least the device won't be
            # connected to again on start.

        self.storage.delete(device)

    def stateful_action(self, device: Device, group: int, state: int):
        """
        Sends a stateful action request to the device.
        """
        LOGGER.debug(f"sending device {device.uuid[:4]} a stateful action "
                     f"request")
        message = GDCI.Message(
            f"{DeviceMessage.ACTION_STATEFUL.value}{group}{state}"
        )
        self.device_connector.send(message, device)

    def reset(self):
        """
        Resets the device application.
        """
        LOGGER.info("resetting the device application...")
        self.device_connector.disconnect_all()

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

    def _request_capabilities(self, device: Device) -> bool:
        """
        Requests the capabilities of the input device.
        """
        message = GDCI.Message(f"{DeviceMessage.CAPABILITY.value}")
        return self.device_connector.send(message, device)
