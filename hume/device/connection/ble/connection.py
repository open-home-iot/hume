import asyncio
import functools
import logging
import storage

from bleak import BleakScanner, BleakClient

from defs import CLI_DEVICE_TRANSPORT
from device.connection.messages import has_message_start, get_request_type
from util import get_arg
from device.connection.gci import GCI
from device.models import Device, DeviceAddress
from device.connection.ble.defs import (
    NUS_SVC_UUID,
    NUS_RX_UUID,
    NUS_TX_UUID,
    HOME_SVC_DATA_UUID,
    HOME_SVC_DATA_VAL_HEX,
    MSG_START_ENC,
    MSG_END_ENC
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
            end_index+1 if len(data[end_index+1:]) > 0 else 0
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


class BLEConnection(GCI):

    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.event_loop = event_loop
        # str(address): BleakClient
        self.clients = dict()
        # str(address): bytearray
        self.requests = dict()
        # str(address): callable
        self.listeners = dict()

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
            device_address = DeviceAddress(
                transport=get_arg(CLI_DEVICE_TRANSPORT),
                address=device.address,
                uuid=device.address
            )
            discovered_device = Device(uuid=device.address,
                                       address=device.address,
                                       name=device.name)

            existing_address_entry = storage.get(DeviceAddress, device.address)
            if existing_address_entry is None:
                LOGGER.info("no existing address entry, storing")
                storage.save(device_address)
                storage.save(discovered_device)

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
        LOGGER.info(f"connecting to device {device.address}")

        async def connect(client: BleakClient):
            return await client.connect()

        device_client = BleakClient(device.address)
        future = asyncio.run_coroutine_threadsafe(
            connect(device_client), self.event_loop
        )
        connected = await_future(future)
        if connected:
            self.clients[device.address] = device_client

        return connected

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
        LOGGER.debug(f"sending device {device.address} message {msg.content}")

        async def write(client: BleakClient):
            await client.write_gatt_char(NUS_RX_UUID, msg.content)

        future = asyncio.run_coroutine_threadsafe(
            write(self.clients[device.address]), self.event_loop)

        await_future(future)

        return True

    def notify(self, callback: callable, device: Device):
        self.listeners[device.address] = callback

        device_client = self.clients[device.address]

        cb = functools.partial(self.on_device_msg, device)

        future = asyncio.run_coroutine_threadsafe(
            device_client.start_notify(NUS_TX_UUID, cb), self.event_loop)
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
        if has_message_start(data):
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
        self.requests[device.address] = None  # Cleared when done

        # more is the index at which the additional message data starts, if 0,
        # there is no more data to parse.
        if more:
            LOGGER.debug("there is more, handle it immediately!")
            # Don't schedule with event loop to ensure the message content gets
            # handled in the order which it was received, should another device
            # message arrive during parsing.
            self.on_device_msg(device, _sender, data[more:])

    def for_each(self, callback: callable):
        for device_address in self.clients.keys():
            callback(Device(address=device_address))
