import asyncio
import logging

from threading import Thread

from defs import CLI_SIMULATION
from app.device.connection.ble.ble import BLEConnection
from app.device.connection.gdci import GDCI
from app.device.connection.sim.sim import SimConnection
from app.device.models import Device

LOGGER = logging.getLogger(__name__)


class DeviceConnector(GDCI):
    """
    Layer of abstraction and aggregator for different device transports. As
    more transport types are added, the DeviceConnector class keeps the GCI
    simple for the DeviceApp and takes care of the complexity in calling
    different interfaces depending on the transport of a device.
    """

    def __init__(self, cli_args):
        self.simulation = cli_args.get(CLI_SIMULATION)
        if self.simulation:
            self.sim = SimConnection()
        else:
            self._event_loop = asyncio.new_event_loop()
            self._event_loop_thread = Thread(target=self._run_event_loop,
                                             args=(self._event_loop,))
            self.ble = BLEConnection(self._event_loop)

    def start(self):
        """Starts up the device connection."""
        LOGGER.info("device connector start")

        if not self.simulation:
            self._event_loop_thread.start()

    def stop(self):
        """Stops the device connection."""
        LOGGER.info("device connector stop")
        if self.disconnect_all():
            LOGGER.info("successfully disconnected all devices")
        else:
            LOGGER.warning("failed to disconnect one or more devices")

        if not self.simulation:
            LOGGER.info("stopping BLE event loop")
            self._event_loop.call_soon_threadsafe(self._event_loop.stop)
            self._event_loop_thread.join(timeout=2.0)

            if self._event_loop_thread.is_alive():
                LOGGER.error("failed to join event loop thread")

    """
    Public (GDCI proxy)
    """

    def discover(self, callback: callable):
        """
        Discovers devices in the local HOME network and returns them by
        calling the provided callback.
        """
        LOGGER.info("checking available transports for discovery")
        if self.simulation:
            self.sim.discover(callback)
        else:
            self.ble.discover(callback)

    def connect(self, device: Device) -> bool:
        """
        Returns True if the device was successfully connected to.
        """
        LOGGER.info(f"connecting to device {device.uuid[:4]}")
        return (self.sim.connect(device) if self.simulation
                else self.ble.connect(device))

    def is_connected(self, device: Device) -> bool:
        """
        Returns True if the device is already connected.
        """
        LOGGER.info(f"checking if device {device.uuid[:4]} is connected")
        return (self.sim.is_connected(device) if self.simulation
                else self.ble.is_connected(device))

    def disconnect(self, device: Device) -> bool:
        """
        Disconnect the input device, return True if successful.
        """
        LOGGER.info(f"disconnecting device {device.uuid[:4]}")
        return (self.sim.disconnect(device) if self.simulation
                else self.ble.disconnect(device))

    def disconnect_all(self) -> bool:
        """
        Disconnects all devices, returns True if all devices were disconnected
        successfully.
        """
        LOGGER.info("disconnecting all devices")
        return (self.sim.disconnect_all() if self.simulation
                else self.ble.disconnect_all())

    def send(self, msg: GDCI.Message, device: Device) -> bool:
        """
        Send a message to a device.
        """
        LOGGER.debug(f"sending message to device {device.uuid[:4]}")
        return (self.sim.send(msg, device) if self.simulation
                else self.ble.send(msg, device))

    def notify(self, callback: callable, device: Device):
        """
        Returns True if the device was successfully connected to.
        """
        LOGGER.info(f"enabling notify for device {device.uuid[:4]}")
        if self.simulation:
            self.sim.notify(callback, device)
        else:
            self.ble.notify(callback, device)

    def for_each(self, callback: callable):
        """
        Calls the callback for each connected device.
        """
        LOGGER.info("for each device do...")
        if self.simulation:
            self.sim.for_each(callback)
        else:
            self.ble.for_each(callback)

    """
    Private
    """

    @staticmethod
    def _run_event_loop(event_loop):
        """Runs the event loop."""
        LOGGER.info("DeviceConnection run event loop")
        event_loop.run_forever()
        LOGGER.info("event loop stopped")
