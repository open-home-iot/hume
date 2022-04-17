# flake8: noqa: E402
import json
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from app.device import DeviceTransport, DeviceMessage
from app.device.models import Device
from app.device.connection.gdci import GDCI
from app.device.connection.sim import SimConnection
from app.device.connection.sim_specs import (
    DEVICE_UUID_LED,
    DEVICE_UUID_AQUARIUM,
    BASIC_LED_CAPS,
    AQUARIUM_CAPS,
)

DEVICE_LED = Device(
    DEVICE_UUID_LED,
    BASIC_LED_CAPS["name"],
    DeviceTransport.SIM.value,
    "address",
    True
)
DEVICE_AQUARIUM = Device(
    DEVICE_UUID_AQUARIUM,
    AQUARIUM_CAPS["name"],
    DeviceTransport.SIM.value,
    "address",
    True
)


class TestConnectionSimulator(unittest.TestCase):

    def setUp(self):
        self.sim = SimConnection()

    def test_connect(self):
        self.assertFalse(self.sim.is_connected(DEVICE_LED))
        self.assertTrue(self.sim.connect(DEVICE_LED))
        self.assertTrue(self.sim.is_connected(DEVICE_LED))

        self.assertTrue(self.sim.disconnect(DEVICE_LED))
        self.assertFalse(self.sim.is_connected(DEVICE_LED))

    def test_disconnect_all(self):
        self.assertFalse(self.sim.is_connected(DEVICE_LED))
        self.assertFalse(self.sim.is_connected(DEVICE_AQUARIUM))
        self.assertTrue(self.sim.connect(DEVICE_LED))
        self.assertTrue(self.sim.connect(DEVICE_AQUARIUM))
        self.assertTrue(self.sim.is_connected(DEVICE_LED))
        self.assertTrue(self.sim.is_connected(DEVICE_AQUARIUM))

        self.assertTrue(self.sim.disconnect_all())
        self.assertFalse(self.sim.is_connected(DEVICE_LED))
        self.assertFalse(self.sim.is_connected(DEVICE_AQUARIUM))

    def test_send_to_disconnected_device(self):
        with self.assertRaises(ConnectionError):
            self.sim.send(
                GDCI.Message(f"{DeviceMessage.CAPABILITY.value}"), DEVICE_LED
            )

    def test_unattached_devices(self):
        self.sim.connect(DEVICE_LED)
        unattached_devices = self.sim._unattached_devices
        for device in unattached_devices:
            if device.uuid == DEVICE_UUID_LED:
                self.fail("Basic LED still resolved as an unattached device")

    def test_for_each(self):
        calls = 0

        def callback(_):
            nonlocal calls
            calls += 1

        self.sim.for_each(callback)
        self.assertEqual(calls, 0)

        self.sim.connect(DEVICE_LED)

        self.sim.for_each(callback)
        self.assertEqual(calls, 1)


class TestBasicLed(unittest.TestCase):

    def setUp(self):
        self.sim = SimConnection()
        self.assertTrue(self.sim.connect(DEVICE_LED))

    def test_send_capability(self):
        error = True

        def callback(device: Device, msg_type: int, msg: bytearray):
            nonlocal error
            if (device.uuid == DEVICE_UUID_LED and
                    msg_type == DeviceMessage.CAPABILITY.value and
                    json.loads(msg) == BASIC_LED_CAPS):
                error = False

        self.sim.notify(callback, DEVICE_LED)
        self.sim.send(
            GDCI.Message(f"{DeviceMessage.CAPABILITY.value}"), DEVICE_LED
        )

        self.assertFalse(error)

    def test_send_stateful_action(self):
        error = True

        def callback(device: Device, msg_type: int, msg: bytearray):
            nonlocal error
            if (device.uuid == DEVICE_UUID_LED and
                    msg_type == DeviceMessage.ACTION_STATEFUL.value and
                    msg == b"00"):
                error = False

        self.sim.notify(callback, DEVICE_LED)
        self.sim.send(
            GDCI.Message(
                f"{DeviceMessage.ACTION_STATEFUL.value}00"
            ), DEVICE_LED
        )

        self.assertFalse(error)

    def test_send_nonexistent_stateful_action(self):
        with self.assertRaises(ValueError):
            self.sim.send(
                GDCI.Message(
                    f"{DeviceMessage.ACTION_STATEFUL.value}02"
                ), DEVICE_LED
            )
