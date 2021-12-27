import asyncio
import functools
import logging

from bleak import BleakScanner, BleakClient

import storage
from defs import CLI_DEVICE_TRANSPORT
from util import get_arg
from device.connection.gci import GCI
from device.models import Device, DeviceAddress
from device.connection.ble.defs import (
    NUS_SVC_UUID,
    NUS_RX_UUID,
    NUS_TX_UUID,
    HOME_SVC_DATA_UUID,
    HOME_SVC_DATA_VAL_HEX,
    MSG_START,
    MSG_START_ENC,
    MSG_END_ENC
)


LOGGER = logging.getLogger(__name__)


class SimConnection(GCI):

    def __init__(self):
        super().__init__()

    def discover(self, on_devices_discovered):
        LOGGER.info("BLEConnection starting device discovery")

    def connect(self, device: Device) -> bool:
        LOGGER.info(f"connecting to device {device.address}")

        return True

    def disconnect(self, device: Device) -> bool:
        LOGGER.info(f"disconnecting device {device.address}")

        return True

    def disconnect_all(self) -> bool:
        return True

    def send(self, msg: GCI.Message, device: Device) -> bool:
        LOGGER.debug(f"sending device {device.address} message {msg.content}")

        return True

    def notify(self, callback: callable, device: Device):
        ...
