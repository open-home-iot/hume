import asyncio
import functools
import logging
import copy

from bleak import BleakScanner, BleakClient

import storage
from defs import CLI_DEVICE_TRANSPORT
from util import get_arg
from device.connection.gci import GCI
from device.models import Device
from device.connection.ble.defs import (
    NUS_SVC_UUID,
    NUS_RX_UUID,
    NUS_TX_UUID,
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


FUTURE_TIMEOUT = 5.0
DISCOVERY_TIMEOUT = 5.0


def await_future(f, timeout=FUTURE_TIMEOUT):
    """
    Generic future handling from sync context.

    :returns: future result if gotten within timeout
    """
    result = None

    try:
        result = f.result(timeout=timeout)
    except asyncio.TimeoutError:
        pass

    return result


class BLEConnection(GCI):

    def __init__(self, event_loop):
        super().__init__()
        self.event_loop = event_loop
        # str(address): BleakClient
        self.clients = dict()

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

        asyncio.run_coroutine_threadsafe(
            BleakScanner.discover(detection_callback=cb), self.event_loop
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
        """
        Connect to the device and indicate if the connection was successful
        through the returned bool. Also starts notify on the device's TX
        characteristic.

        :param device: device to connect to
        :returns: True if successful
        """
        async def connect(client: BleakClient):
            return await client.connect()

        device_client = BleakClient(device.address)
        future = asyncio.run_coroutine_threadsafe(
            connect(device_client), self.event_loop
        )
        connected = await_future(future)
        if connected:
            self.clients[device.address] = device_client

            cb = functools.partial(self.on_device_msg, device.address)
            future = asyncio.run_coroutine_threadsafe(
                device_client.start_notify(NUS_TX_UUID, cb), self.event_loop)
            await_future(future)

        return connected

    def on_device_msg(self, device_address: str, sender: int, data: bytearray):
        """
        Bleak-standard callback for characteristic notifications, called when a
        connected device sends a message on its TX characteristic.

        :param device_address:
        :param sender:
        :param data:
        :return:
        """
        LOGGER.info(f"device address {device_address} sent message {data} from sender {sender}")

    def is_connected(self, device: Device):
        return self.clients.get(device.address) is not None

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.address}")

        device_client = self.clients.pop(device.address)
        disconnected = await_future(
            asyncio.run_coroutine_threadsafe(
                self.disconnect_client(device_client),
                self.event_loop
            )
        )

        return disconnected

    @staticmethod
    async def disconnect_client(client: BleakClient):
        """Disconnect the input client"""
        return await client.disconnect()

    def disconnect_all(self) -> bool:
        """
        Disconnect all devices, used as cleanup before shutdown. Returns false
        if ANY disconnection has failed.
        """
        LOGGER.info("disconnecting all connected devices")

        disconnections = []

        for client in self.clients.values():
            disconnections.append(
                await_future(
                    asyncio.run_coroutine_threadsafe(
                        self.disconnect_client(client), self.event_loop
                    )
                )
            )

        self.clients = dict()

        return False not in disconnections

    def send(self, msg: GCI.Message, device: Device) -> bool:
        async def write(client: BleakClient):
            await client.write_gatt_char(NUS_RX_UUID, msg.content)

        future = asyncio.run_coroutine_threadsafe(
            write(self.clients[device.address]), self.event_loop)

        await_future(future)

        return True

    def notify(self, callback: callable(GCI.Message), device: Device):
        pass
