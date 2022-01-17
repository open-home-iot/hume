import logging

from app.abc import App
from app.device.connection.connection import DeviceConnection
from app.device.models import Device, DeviceHealth
from app.device.defs import TRANSPORT_BLE
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

        self.connect_attached_devices()

    def post_start(self):
        LOGGER.info("Device post_start")

    def pre_stop(self):
        LOGGER.info("Device pre_stop")

    def stop(self):
        LOGGER.info("Device stop")
        self.connection.stop()

    def post_stop(self):
        LOGGER.info("Device post_start")

    def connect_attached_devices(self):
        """
        Establishes a connection with all attached devices.
        """
        LOGGER.info("connecting attached devices")

        devices = self.storage.get_all(Device)
        for device in devices:
            if device.transport == TRANSPORT_BLE:
                self.connection.ble.connect(device)
