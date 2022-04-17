# flake8: noqa: E402
import unittest
import sys
import os
import uuid
from unittest.mock import Mock

from bleak.backends.device import BLEDevice

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from app.device.connection import ble
from app.device.connection.ble import BLEConnection
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
        # Has both NUS and HOME service ID
        self.assertEqual(
            True,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID, uuid.uuid4()],
                service_data={
                    # LEEEEEEEEEEET
                    ble.HOME_SVC_DATA_UUID: b"\x13\x37"
                }
            ))
        )
        # Has NUS but empty service data
        self.assertEqual(
            False,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID, uuid.uuid4(), uuid.uuid4()],
                service_data={}
            ))
        )
        # Has only HOME service ID
        self.assertEqual(
            False,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[uuid.uuid4(), uuid.uuid4()],
                service_data={
                    # LEEEEEEEEEEET
                    ble.HOME_SVC_DATA_UUID: b"\x13\x37"
                }
            ))
        )
        # Has neither NUS not HOME service ID
        self.assertEqual(
            False,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[uuid.uuid4(), uuid.uuid4()],
                service_data={}
            ))
        )
        # Scrambled NUS and HOME service ID
        self.assertEqual(
            False,
            ble.home_compatible(BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID[1:], uuid.uuid4(), uuid.uuid4()],
                service_data={
                    # LEEEEEEEEEEET
                    ble.HOME_SVC_DATA_UUID: b"\x13\x37"
                }
            ))
        )

    def test_scan_data(self):

        def make_bytearray(string):
            ba = bytearray()
            for c in string:
                # ord -> unicode code point for a given character
                ba.append(ord(c))
            return ba

        # fully formed message, with a start and an ending
        data = make_bytearray("^01$")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("1"))
        self.assertEqual(ends, True)
        self.assertEqual(more, 0)

        # no ending
        data = make_bytearray("^01")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("1"))
        self.assertEqual(ends, False)
        self.assertEqual(more, 0)

        # no start nor ending
        data = make_bytearray("01")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("01"))
        self.assertEqual(ends, False)
        self.assertEqual(more, 0)

        # no start but an ending
        data = make_bytearray("01$")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("01"))
        self.assertEqual(ends, True)
        self.assertEqual(more, 0)

        # no start but an ending and more stuff
        data = make_bytearray("01$1")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("01"))
        self.assertEqual(ends, True)
        self.assertEqual(more, 3)

        # start, ending and more stuff
        data = make_bytearray("^1234$abc123")
        data, ends, more = ble.scan_data(data)
        self.assertEqual(data, make_bytearray("234"))
        self.assertEqual(ends, True)
        self.assertEqual(more, 6)


class TestBLEConnectionInterface(unittest.TestCase):

    def test_on_device_found(self):
        mock = Mock()
        BLEConnection.on_device_found(
            mock, BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID, uuid.uuid4()],
                service_data={
                    # LEEEEEEEEEEET
                    ble.HOME_SVC_DATA_UUID: b"\x13\x37"
                }
            ),
            _advertisement_data={}
        )
        mock.assert_called()

        mock = Mock()
        BLEConnection.on_device_found(
            mock, BLEDevice(
                "address", "name",
                uuids=[ble.NUS_SVC_UUID, uuid.uuid4()],
                service_data={}
            ),
            _advertisement_data={}
        )
        mock.assert_not_called()
