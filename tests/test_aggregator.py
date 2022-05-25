# flake8: noqa: E402
import threading
import unittest
import sys
import os

from unittest.mock import patch, Mock

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from defs import CLI_SIMULATION
from app.device.models import Device
from app.device.connection.gdci import GDCI
from app.device.connection.defs import DeviceTransport
from app.device.connection.aggregator import ConnectionAggregator
from app.device.connection.sim import SimConnection
from app.device.connection.sim_specs import (
    DEVICE_UUID_LED,
    DEVICE_UUID_AQUARIUM
)


class TestSimConnectionAggregatorGDCI(unittest.TestCase):
    """Test the simulated device connector."""

    def setUp(self):
        self.cli_args = {
            CLI_SIMULATION: True
        }
        self.aggregator = ConnectionAggregator(self.cli_args)
        self.assertTrue(isinstance(self.aggregator.sim, SimConnection))
        self.assertFalse(hasattr(self.aggregator, "ble"))

        self.aggregator.start()

    def tearDown(self):
        self.aggregator.stop()

    def test_discover(self):
        calls = 0

        def callback(devices: [Device]):
            if len(devices) < 1:
                raise ValueError("didn't discover enough devices!")
            nonlocal calls
            calls += 1

        self.aggregator.discover(callback)
        self.assertEqual(1, calls)

    def test_connection(self):
        device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", True)

        # is connected -> False
        # then connect -> True
        # is connected -> True
        self.assertFalse(self.aggregator.is_connected(device))
        self.assertTrue(self.aggregator.connect(device))
        self.assertTrue(self.aggregator.is_connected(device))

        # disconnect -> True
        # is connected -> False
        self.assertTrue(self.aggregator.disconnect(device))
        self.assertFalse(self.aggregator.is_connected(device))

        # connect -> True
        # disconnect all -> True
        # is connected -> False
        self.assertTrue(self.aggregator.connect(device))
        self.assertTrue(self.aggregator.disconnect_all())
        self.assertFalse(self.aggregator.is_connected(device))

    def test_send(self):
        device = Device(DEVICE_UUID_LED,
                        "name",
                        DeviceTransport.SIM.value,
                        "address",
                        True)
        with self.assertRaises(ConnectionError):
            self.assertFalse(self.aggregator.send(GDCI.Message("01"), device))
        self.assertTrue(self.aggregator.connect(device))
        self.aggregator.notify(lambda _d, _mt, _m: ..., device)
        self.assertTrue(self.aggregator.send(GDCI.Message("01"), device))

    def test_notify(self):
        device = Device(
            DEVICE_UUID_AQUARIUM, "name", DeviceTransport.SIM.value, "address", True)
        self.assertTrue(self.aggregator.connect(device))
        self.aggregator.notify(lambda _d, _mt, _m: ..., device)

    def test_for_each(self):
        device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", True)
        device2 = Device(
            DEVICE_UUID_AQUARIUM, "name2", DeviceTransport.SIM.value, "address", True)
        self.assertTrue(self.aggregator.connect(device))
        self.assertTrue(self.aggregator.connect(device2))

        iterated_devices = 0

        def callback(_d: Device):
            nonlocal iterated_devices
            iterated_devices += 1

        self.aggregator.for_each(callback)
        self.assertEqual(iterated_devices, 2)


class TestBLEConnectionAggregatorGDCI(unittest.TestCase):
    """
    Verify the connection aggregator makes the correct calls when not in sim
    mode.
    """

    @patch("app.device.connection.aggregator.BLEConnection")
    def setUp(self, _ble):
        self.cli_args = {
            CLI_SIMULATION: False
        }
        self.aggregator = ConnectionAggregator(self.cli_args)
        self.assertTrue(isinstance(self.aggregator.ble, Mock))
        self.assertFalse(hasattr(self.aggregator, "sim"))

        self.aggregator.start()

    def tearDown(self):
        self.aggregator.stop()

    def test_discover(self):
        self.aggregator.discover(lambda _: ...)
        self.aggregator.ble.discover.assert_called()

    def test_connection(self):
        device = Device(
            "uuid", "name", DeviceTransport.BLE.value, "address", True)
        self.aggregator.connect(device)
        self.aggregator.ble.connect.assert_called_with(device)

        self.aggregator.is_connected(device)
        self.aggregator.ble.is_connected.assert_called_with(device)

        self.aggregator.disconnect(device)
        self.aggregator.ble.disconnect.assert_called_with(device)

        self.aggregator.disconnect_all()
        self.aggregator.ble.disconnect_all.assert_called()

    def test_send(self):
        device = Device(
            "uuid", "name",  DeviceTransport.BLE.value, "address", True)
        msg = GDCI.Message("")
        self.aggregator.send(msg, device)
        self.aggregator.ble.send.assert_called_with(msg, device)

    def test_notify(self):
        device = Device(
            "uuid", "name", DeviceTransport.BLE.value, "address", True)

        def callback(_d, _mt, _m):
            pass

        self.aggregator.notify(callback, device)
        self.aggregator.ble.notify.assert_called_with(callback, device)

    def test_for_each(self):
        device = Device(
            "uuid", "name", DeviceTransport.BLE.value, "address", True)
        self.aggregator.for_each(device)
        self.aggregator.ble.for_each.assert_called_with(device)


class TestConnectionAggregatorEventLoopHandling(unittest.TestCase):

    def setUp(self):
        self.cli_args = {
            CLI_SIMULATION: False
        }
        self.connector = ConnectionAggregator(self.cli_args)
        self.connector.start()

    def tearDown(self):
        # even if test case calls stop, call here as well to ensure no-harm and
        # idempotence
        self.connector.stop()

    def test_event_loop_handling(self):
        # no exceptions should happen :-), if this test case hangs then
        # cleaup was not successful
        self.assertEqual(2, threading.active_count())
        self.connector.stop()
        self.assertEqual(1, threading.active_count())
