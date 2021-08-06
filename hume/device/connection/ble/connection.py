import asyncio
import functools
import logging

from bleak import BleakScanner

import storage
from defs import CLI_DEVICE_TRANSPORT
from util import get_arg
from device.connection.gci import GCI
from device.models import Device
from device.connection.ble.defs import (
    NUS_SVC_UUID,
    HOME_SVC_DATA_UUID,
    HOME_SVC_DATA_VAL_HEX,
)


LOGGER = logging.getLogger(__name__)


def is_home_compatible(device):
    """
    Check a device returned by scanner for HOME compatibility. To be HOME
    compatible, a BLE device should:

     1. Have the Nordic Semiconductor UART service (NUS) available.
     2. Have a HOME-specific service-data entry.

    :param device: bleak.backends.device.BLEDevice
    :return: bool
    """
    # Interesting device, look for HOME compatibility
    if NUS_SVC_UUID in device.metadata["uuids"]:

        # Check for HOME service data
        home_svc_data_val = (
            device.metadata["service_data"].get(HOME_SVC_DATA_UUID))
        if home_svc_data_val is not None and (
                home_svc_data_val.hex() == HOME_SVC_DATA_VAL_HEX):
            return True
    return False


class BLEConnection(GCI):

    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.event_loop = event_loop

    def discover(self, on_devices_discovered):
        """
        :param on_devices_discovered: callable([Device]) will be called when
            one or more devices have been discovered
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
        if is_home_compatible(device):
            LOGGER.info(f"device {device.name} was HOME compatible!")

            # Store discovered device if not exists
            discovered_device = Device(
                transport=get_arg(CLI_DEVICE_TRANSPORT),
                address=device.address,
                name=device.name,
                # Will get updated once/if device is attached, enables
                # quick lookup for duplicates on multiple discoveries
                uuid=device.address,
            )

            existing_device = storage.get(Device, device.address)
            if existing_device is None:
                discovered_device.save()

            # Push device discovered to callback
            on_devices_discovered([discovered_device])

    def connect(self, device: Device) -> bool:
        pass

    def send(self, msg: GCI.Message, device: Device) -> bool:
        pass

    def disconnect(self, device: Device):
        pass

    def notify(self, callback: callable(GCI.Message), device: Device):
        pass
