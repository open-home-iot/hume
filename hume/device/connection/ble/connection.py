import asyncio
import functools
import logging

from bleak import BleakScanner

from device.connection.gci import GCI
from device.models import Device


LOGGER = logging.getLogger(__name__)


class BLEConnection(GCI):

    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.event_loop = event_loop

    def discover(self, on_devices_discovered):
        """
        :param on_devices_discovered: callable([Device]) will be called when one
                                      or more devices have been discovered
        """
        LOGGER.info("BLEConnection starting device discovery")

        cb = None
        if on_devices_discovered is not None:
            cb = functools.partial(BLEConnection.on_device_found,
                                   on_devices_discovered)

        asyncio.run(
            BleakScanner.discover(detection_callback=cb)
        )

    @staticmethod
    def on_device_found(on_devices_discovered,
                        device,
                        advertisement_data):
        """
        Handle a bleak scanner device found event. Forward information to the
        on_devices_discovered callback, but format it first to something HUME
        understands.
        """
        LOGGER.info(on_devices_discovered)
        LOGGER.info(device)
        LOGGER.info(advertisement_data)

    def connect(self, device: Device) -> bool:
        pass

    def send(self, msg: GCI.Message, device: Device) -> bool:
        pass

    def disconnect(self, device: Device):
        pass

    def notify(self, callback: callable(GCI.Message), device: Device):
        pass
