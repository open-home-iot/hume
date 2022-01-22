import logging

from app.abc import App
from app.device.connection.connection import DeviceConnection
from app.device.models import Device, DeviceHealth
from app.device.defs import TRANSPORT_BLE, TRANSPORT_SIM
from defs import CLI_SIMULATION
from util.storage import DataStore


LOGGER = logging.getLogger(__name__)


class DeviceApp(App):

    def __init__(self, cli_args, storage: DataStore):
        super().__init__()
        self.cli_args = cli_args
        self.storage = storage
        self.connection = DeviceConnection(cli_args)

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

    def _on_device_message(self, device, message_type, body):
        """
        Called when a connected device
        """
        LOGGER.debug("received device message")

    def _connect_attached_devices(self):
        """
        Establishes a connection with all attached devices.
        """
        LOGGER.info("connecting attached devices")

        devices = self.storage.get_all(Device)
        for device in devices:
            if self.cli_args.get(CLI_SIMULATION):
                if device.attached and device.transport == TRANSPORT_SIM:
                    _connected = self.connection.sim.connect(device)
                    # TODO: implement sim notify!
                    self.connection.sim.notify(self._on_device_message, device)
            else:
                if device.attached and device.transport == TRANSPORT_BLE:
                    connected = self.connection.ble.connect(device)

                    # TODO: reconnect at an interval? At least notify HINT so
                    #  that the user can take action.
                    if not connected:
                        LOGGER.error(f"failed to connect device "
                                     f"{device.uuid[:4]}")
                        continue

                    self.connection.ble.notify(self._on_device_message, device)
