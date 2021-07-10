"""
Definitions for the Device Controller.
"""


#
# CLI args
#
CLI_HUME_UUID = "hume_uuid"

# TESTING PARAMETERS
CLI_TEST_DEVICE_MOCK_ADDRESS = "test_device_mock_address"
CLI_TEST_RUN_DEVICE_SIMULATOR = "test_run_device_simulator"


#
# Message types
#
class MessageType:
    DISCOVER_DEVICES = 0
    CONFIRM_ATTACH = 1
    DETACH = 2
