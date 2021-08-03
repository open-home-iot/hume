import asyncio
import functools
import logging

from bleak import BleakScanner

from device.connection.gci import GCI
from device.models import Device
from device.connection.ble.defs import (
    NUS_SVC_UUID,
    HOME_SVC_DATA_UUID,
    HOME_SVC_DATA_VAL_HEX,
)


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
                        _advertisement_data):
        """
        Handle a bleak scanner device found event. Forward information to the
        on_devices_discovered callback, but format it first to something HUME
        understands. Only devices that are HOME compatible will be forwarded
        to the caller's callback.

        :param on_devices_discovered: callable([Device])
        :param device: bleak.backends.device.BLEDevice
        :param _advertisement_data: bleak.backends.scanner.AdvertisementData
        """
        # Interesting device, look for HOME compatibility
        if NUS_SVC_UUID in device.metadata["uuids"]:

            # Check for HOME service data
            home_svc_data_val = (
                device.metadata["service_data"].get(HOME_SVC_DATA_UUID))
            if home_svc_data_val is not None and (
                    home_svc_data_val.hex() == HOME_SVC_DATA_VAL_HEX):

                # Push device discovered to callback
                on_devices_discovered([Device(address=device.address,
                                              name=device.name)])

    def connect(self, device: Device) -> bool:
        pass

    def send(self, msg: GCI.Message, device: Device) -> bool:
        pass

    def disconnect(self, device: Device):
        pass

    def notify(self, callback: callable(GCI.Message), device: Device):
        pass
