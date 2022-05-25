# flake8: noqa: E402
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../hume"))

from util.storage import DataStore
from defs import CLI_SIMULATION
from app.device import DeviceApp
from app.device.models import Device
from app.device.connection.defs import DeviceTransport, DeviceMessage
from app.device.connection.sim_specs import DEVICE_UUID_LED


def _device_msg_squelcher(_d, _t, _m):
    pass


def attach_device(uuid: str, app: DeviceApp):
    device = app.storage.get(Device, uuid)
    device.attached = True
    app.storage.set(device)
    app.aggregator.connect(device)
    app.aggregator.notify(_device_msg_squelcher, device)


class TestModel(unittest.TestCase):

    def test_model_decoding(self):
        """Verify the Device model decoding works as intended."""
        decoded_device = Device.decode("UUID",
                                       "name",
                                       DeviceTransport.BLE.value,
                                       "address",
                                       "1")

        self.assertEqual(decoded_device.uuid, "UUID")
        self.assertEqual(decoded_device.name, "name")
        self.assertEqual(decoded_device.transport, DeviceTransport.BLE.value)
        self.assertEqual(decoded_device.address, "address")
        self.assertEqual(decoded_device.attached, True)


class TestAppLCM(unittest.TestCase):

    def setUp(self):
        self.storage = DataStore()

    def tearDown(self):
        self.storage.delete_all()

    def test_app_lcm(self):
        """
        Verifies the different LCM hooks are doing what they should.
        """
        cli_args = {
            CLI_SIMULATION: True,
        }
        device_app = DeviceApp(cli_args, self.storage)

        # pre_start
        device_app.pre_start()
        # Assert KeyError rather than model error since the table should now
        # be registered.
        with self.assertRaises(KeyError):
            self.storage.get(Device, "fake-key")

        # start
        device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", True)
        self.storage.set(device)
        device_app.start()

        # all attached devices should be connected.
        self.assertEqual(True,
                         device_app.aggregator.is_connected(device))

        # post_start
        device_app.post_start()  # nothing happens in particular...

        # pre_stop
        device_app.pre_stop()  # nothing happens in particular...

        # stop
        device_app.stop()

        # all connections should be torn down
        self.assertEqual(False,
                         device_app.aggregator.is_connected(device))

        # post_stop
        device_app.post_stop()  # nothing happens in particular...


class TestDeviceAppPublicInterface(unittest.TestCase):
    """Verifies all the device app's exported methods."""

    def setUp(self):
        self.cli_args = {
            CLI_SIMULATION: True,
        }
        self.storage = DataStore()
        self.app = DeviceApp(self.cli_args, self.storage)
        self.app.pre_start()

        # To avoid warning printouts happening due to logged warnings in the
        # absence of a registered callback. Method is idempotent, so test cases
        # can re-register freely.
        self.app.register_callback(_device_msg_squelcher)

        self.app.start()
        self.app.post_start()

    def tearDown(self):
        self.app.reset()  # to clear all data

        self.app.pre_stop()
        self.app.stop()
        self.app.post_stop()

    def test_register_callback(self):
        # setup some test stuff :)
        device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", True)
        self.storage.set(device)

        callback_called = False

        def callback(_device, _msg_type, _body):
            nonlocal callback_called
            callback_called = True

        self.app.register_callback(callback)
        self.app._on_device_message(device,
                                    DeviceMessage.ACTION_STATEFUL.value,
                                    bytearray())

        self.assertTrue(callback_called)

    def test_discover(self):
        devices = self.storage.get_all(Device)
        self.assertEqual(len(devices), 0)

        # should mean that simulated devices are now discovered
        self.app.discover(lambda _: ...)

        devices = self.storage.get_all(Device)
        self.assertTrue(len(devices) > 0)

    def test_discover_and_request_capabilities(self):
        discovered_devices = False
        app = self.app

        def discover_result(devices: [Device]):
            nonlocal discovered_devices, app
            discovered_devices = True

            assert len(devices) > 0
            for device in devices:
                # assume capability request can be sent to a discovered device.
                assert app.request_capabilities(device)

        self.app.discover(discover_result)
        self.assertTrue(discovered_devices)

    def test_detach(self):
        # set up an attached device
        device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", True)
        self.storage.set(device)
        self.app.aggregator.connect(device)

        self.app.detach(device)

        with self.assertRaises(KeyError):
            self.storage.get(Device, "uuid")

        self.assertFalse(self.app.aggregator.is_connected(device))

    def test_stateful_action(self):
        non_existent_device = Device(
            DEVICE_UUID_LED, "name", DeviceTransport.SIM.value, "address", False
        )

        # SIM raises exception for non-existent devices.
        with self.assertRaises(ConnectionError):
            self.app.stateful_action(non_existent_device, 0, 1)

        self.app.discover(lambda _: ...)  # to create model instances
        attach_device(DEVICE_UUID_LED, self.app)

        attached_device = self.storage.get(Device, DEVICE_UUID_LED)
        self.app.stateful_action(attached_device, 0, 1)

    def test_reset(self):
        self.app.discover(lambda _: ...)  # to create model instances
        attach_device(DEVICE_UUID_LED, self.app)

        device = self.storage.get(Device, DEVICE_UUID_LED)
        self.assertTrue(self.app.aggregator.is_connected(device))

        self.app.reset()
        self.assertFalse(self.app.aggregator.is_connected(device))
        with self.assertRaises(KeyError):
            self.storage.get(Device, DEVICE_UUID_LED)
