# flake8: noqa: E402
import unittest
import sys
import os
import uuid

from bleak.backends.device import BLEDevice

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from app.device.connection import ble
from app.device.connection.defs import DeviceMessage


class TestSupportingFunctions(unittest.TestCase):

    def test_is_message_start(self):
        self.assertEqual(True, ble.is_message_start(bytearray(b"^")))
        self.assertEqual(False, ble.is_message_start(bytearray(b"0")))
        self.assertEqual(False, ble.is_message_start(bytearray(b"abd1^")))

    def test_get_request_type(self):
        self.assertEqual(
            DeviceMessage.CAPABILITY.value,
            ble.get_request_type(bytearray(
                f"^{DeviceMessage.CAPABILITY.value}123".encode())
            )
        )
        self.assertEqual(
            DeviceMessage.ACTION_STATEFUL.value,
            ble.get_request_type(bytearray(
                f"^{DeviceMessage.ACTION_STATEFUL.value}489".encode())
            )
        )

    def test_device_home_compatibility(self):
        self.assertEqual(
            True,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID, uuid.uuid4()],
                service_data={
                    ble.HOME_SVC_DATA_UUID: ble.HOME_SVC_DATA_VAL_HEX
                }
            ))
        )
        # self.assertEqual(False)
        # self.assertEqual(False)
