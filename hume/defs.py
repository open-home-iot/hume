"""
Definitions for the Device Controller.
"""


#
# CLI args
#
CLI_HUME_UUID = "hume_uuid"

CLI_DEVICE_TRANSPORT = "device_transport"
CLI_DEVICE_TRANSPORT_BLE = "ble"  # Bluetooth LE (BLE)

CLI_HINT_IP_ADDRESS = "hint_ip_address"
CLI_HINT_PORT = "hint_port"

CLI_BROKER_IP_ADDRESS = "broker_ip_address"
CLI_BROKER_PORT = "broker_port"


#
# Message types
#
class CommandType:
    DISCOVER_DEVICES = 0
    ATTACH_DEVICE = 1