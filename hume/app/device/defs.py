from enum import Enum


TRANSPORT_BLE = "ble"
TRANSPORT_SIM = "sim"


class DeviceMessage(Enum):
    CAPABILITY = 0
    ACTION_STATEFUL = 1
    HEARTBEAT = 2
