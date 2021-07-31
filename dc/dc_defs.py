"""
Definitions for the Device Controller.
"""


#
# CLI args
#
CLI_HUME_UUID = "hume_uuid"

CLI_DEVICE_TRANSPORT = "device_transport"
CLI_DEVICE_TRANSPORT_BLE = "ble"  # Bluetooth LE (BLE)


#
# Message types
#
class MessageType:
    DISCOVER_DEVICES = 0
    CONFIRM_ATTACH = 1
    DETACH = 2
