from enum import Enum


class DeviceTransport(Enum):
    BLE = "ble"
    SIM = "sim"


class DeviceMessage(Enum):
    CAPABILITY = 0
    ACTION_STATEFUL = 1
