import asyncio
import functools
import logging
import sys

from typing import Union

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice

from app.device.models import Device
from app.device.connection.defs import DeviceTransport
from app.device.connection.gdci import GDCI

HOME_SVC_DATA_UUID = "0000a1b2-0000-1000-8000-00805f9b34fb"
HOME_SVC_DATA_VAL_HEX = "1337"

NUS_SVC_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
NUS_RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

MSG_START = "^"
MSG_START_ENC = b"^"
MSG_END = "$"
MSG_END_ENC = b"$"

LOGGER = logging.getLogger(__name__)


def is_message_start(data: bytearray):
    """Checks if the input data is the start of a device message."""
    return data[0] == ord(MSG_START)


def get_request_type(data: bytearray) -> int:
    """:returns: the message request type"""
    # chr -> looks up the ASCII table for which character the number
    # corresponds to
    # int -> convert the character to an integer, for example '1' -> 1
    return int(chr(data[1]))


def home_compatible(device):
    """
    Check a device returned by scanner for HOME compatibility. To be HOME
    compatible, a BLE device should:

     1. Have the Nordic Semiconductor UART service (NUS) available.
     2. Have a HOME-specific service-data entry.

    :param device: bleak.backends.device.BLEDevice
    :return: bool
    """

    def check_for_home_svc_data(d: BLEDevice) -> Union[bytearray, None]:
        """
        mac-backends will have a 'service_data' metadata property.
        linux-backends will have a path.props 'ServiceData' property.

        {'path': '/org/bluez/hci0/dev_D3_64_79_85_A2_61', 'props': {
          ...
          'ServiceData': {
            '0000a1b2-0000-1000-8000-00805f9b34fb': bytearray(b'\x137')},
            ...
          }
        }
        """
        if sys.platform.startswith("linux"):
            return d.details \
                .get("props", dict()) \
                .get("ServiceData", dict()) \
                .get(HOME_SVC_DATA_UUID)

        return d.metadata.get("service_data", dict()).get(HOME_SVC_DATA_UUID)

    LOGGER.debug(f"checking device with metadata {device.metadata}")
    LOGGER.debug(f"device.details: {device.details}")

    # If the NUS service exists, continue checking
    if NUS_SVC_UUID in device.metadata["uuids"]:
        # Check for HOME service data
        home_svc_data_val = check_for_home_svc_data(device)
        return home_svc_data_val is not None and (
                home_svc_data_val.hex() == HOME_SVC_DATA_VAL_HEX)

    return False


def scan_data(data: bytearray) -> (bytearray, bool, int):
    """
    Scans input data for message body content, if the message has an ending,
    and if there is more content to parse after a found ending, the index at
    which to start parsing, else 0.
    """
    start_index = 0
    try:
        data.index(MSG_START_ENC)
        start_index = 2  # skip MSG_START & request type
    except ValueError:
        pass

    try:
        end_index = data.index(MSG_END_ENC)
        return (
            data[start_index:end_index],
            True,
            # +1 to skip MSG_END character, 0 = does not end
            end_index + 1 if len(data[end_index + 1:]) > 0 else 0
        )
    except ValueError:
        return data[start_index:], False, 0


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


class BLEConnection(GDCI):

    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.event_loop = event_loop
        # str(address): BleakClient
        self.clients = dict()
        # str(address): bytearray
        self.requests = dict()
        # str(address): callable
        self.listeners = dict()
        # str(address): Device
        self.devices = dict()

        # str(address): BLEDevice
        # Needed because if you do not keep device details another discovery is
        # started and bleak cannot handle more than 1 simultaneous discovery at
        # a given time -> exception.
        self._discovery_cache = dict()

    def discover(self, on_devices_discovered):
        """
        :param on_devices_discovered: callable([Device]) will be called when
            one or more devices have been discovered
        """
        LOGGER.info("BLEConnection starting device discovery")

        cb = functools.partial(self.on_device_discovered,
                               on_devices_discovered)

        # Reset discovery cache to avoid buildup
        self._discovery_cache.clear()

        asyncio.run_coroutine_threadsafe(
            BleakScanner.discover(detection_callback=cb), self.event_loop
        )

    def on_device_discovered(self,
                             on_devices_discovered,
                             device: BLEDevice,
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
        LOGGER.info(f"discovered device {device.name}")

        if home_compatible(device):
            LOGGER.info(f"device {device.name} was HOME compatible!")

            # The device is always referred to with its address
            self._discovery_cache[device.address] = BLEDevice

            discovered_device = Device(device.address,
                                       device.name,
                                       DeviceTransport.BLE.value,
                                       device.address,
                                       False)

            # Push device discovered to callback
            on_devices_discovered([discovered_device])

        else:
            LOGGER.debug("device wasn't compatible with HOME!")

    def connect(self, device: Device) -> bool:
        """
        Connect to the device and indicate if the connection was successful
        through the returned bool. Also starts notify on the device's TX
        characteristic.

        :param device: device to connect to
        :returns: True if successful
        """
        LOGGER.info(f"connecting to device {device.address}")

        async def _connect(client: BleakClient):
            return await client.connect()

        def fetch_device_info_to_connect_to(address: str) -> \
                Union[BLEDevice, str]:
            cache_result = self._discovery_cache.get(address, address)
            if isinstance(cache_result, BLEDevice):
                LOGGER.info("found discovered BLEDevice instance:")
                LOGGER.info(cache_result.__str__())

            return cache_result

        bledevice_or_address = fetch_device_info_to_connect_to(device.address)

        device_client = BleakClient(bledevice_or_address)
        future = asyncio.run_coroutine_threadsafe(
            _connect(device_client), self.event_loop
        )
        connected = await_future(future)
        if connected:
            # TODO: Set disconnected callback.
            self.clients[device.address] = device_client
            self.devices[device.address] = device

        return connected

    def is_connected(self, device: Device):
        return self.clients.get(device.address) is not None

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.address[:4]}")

        device_client = self.clients.pop(device.address)
        self.devices.pop(device.address)

        # pop optionals
        if self.requests.get(device.address) is not None:
            self.requests.pop(device.address)
        if self.listeners.get(device.address) is not None:
            self.listeners.pop(device.address)

        async def disconnect_client(client: BleakClient):
            """Disconnect the input client"""
            return await client.disconnect()

        disconnected = await_future(
            asyncio.run_coroutine_threadsafe(
                disconnect_client(device_client),
                self.event_loop
            )
        )

        if not disconnected:
            LOGGER.warning("failed to disconnect device")

        return disconnected

    def disconnect_all(self) -> bool:
        """
        Disconnect all devices, used as cleanup before shutdown. Returns false
        if ANY disconnection has failed.
        """
        LOGGER.info("disconnecting all connected devices")

        disconnections = []

        # To avoid mutating the collection being iterated over.
        devices = list(self.devices.values())

        for device in devices:
            disconnections.append(self.disconnect(device))

        return False not in disconnections

    def send(self, msg: GDCI.Message, device: Device) -> bool:
        LOGGER.debug(f"sending device {device.address[:4]} "
                     f"message {msg.content}")

        async def write(client: BleakClient):
            await client.write_gatt_char(NUS_RX_UUID, msg.content)

        future = asyncio.run_coroutine_threadsafe(
            write(self.clients[device.address]), self.event_loop)

        await_future(future)

        return True

    def notify(self, callback: callable, device: Device):
        LOGGER.info("enabling notify")

        if self.devices.get(device.address) is None:
            LOGGER.error(f"can't notify device {device.uuid[:4]}, it's not "
                         f"connected")
            return

        self.listeners[device.address] = callback

        device_client = self.clients[device.address]

        cb = functools.partial(self.on_device_msg, device)

        future = asyncio.run_coroutine_threadsafe(
            device_client.start_notify(NUS_TX_UUID, cb), self.event_loop
        )
        await_future(future)

    def on_device_msg(self, device: Device, _sender: int, data: bytearray):
        """
        Bleak-standard callback for characteristic notifications, called when a
        connected device sends a message on its TX characteristic.

        :param device: device which sent data
        :param _sender: char handle
        :param data: bytes
        """
        LOGGER.debug(f"device {device.name} sent message {data} from char "
                     f"{_sender}")

        # some messages are too long for the arduino message buffer, meaning
        # they will come as two separate messages. Find the start and end tags
        # of messages to make a complete request body for decoding.
        if is_message_start(data):
            LOGGER.debug("has start tag, wiping request record for device")
            request_type = get_request_type(data)
            self.requests[device.address] = (request_type, bytearray(),)

        body, ends, more = scan_data(data)
        LOGGER.debug(f"body: {body} ends: {ends} more: {more}")

        # check existing request content
        request = self.requests.get(device.address)
        if request is None:  # stop handling
            LOGGER.error("missed a start tag somewhere, no in progress request"
                         " found")
            return

        # unpack ongoing request
        request_type, existing_body = request

        if not ends:  # store the gotten body -> end handling
            LOGGER.debug("does not end, save progress and quit")
            self.requests[device.address] = (
                request_type, existing_body + body,)
            return
        LOGGER.debug(f"finalized message body: {existing_body + body}")

        # End tag found, call registered callback
        self.listeners[device.address](
            device, request_type, existing_body + body
        )
        self.requests.pop(device.address)  # Cleared when done

        # more is the index at which the additional message data starts, if 0,
        # there is no more data to parse.
        if more:
            LOGGER.debug("there is more, handle it immediately!")
            # Don't schedule with event loop to ensure the message content gets
            # handled in the order which it was received, should another device
            # message arrive during parsing.
            self.on_device_msg(device, _sender, data[more:])

    def for_each(self, callback: callable):
        for device in self.devices.items():
            callback(device)
