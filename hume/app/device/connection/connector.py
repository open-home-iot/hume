import asyncio
import logging

from threading import Thread

from defs import CLI_SIMULATION
from .ble.connection import BLEConnection
from .sim.connection import SimConnection
from ..models import Device

LOGGER = logging.getLogger(__name__)


class DeviceConnector:
    """
    Layer of abstraction for the Device application to connect to devices. As
    more transport types are added, the DeviceConnector class keeps the GCI
    simple for the DeviceApp and takes care of the complexity in calling
    different interfaces depending on the transport of a device.
    """

    def __init__(self, cli_args):
        self.simulation = (
            True if cli_args.get(CLI_SIMULATION) else False
        )
        if self.simulation:
            self.sim = SimConnection()
        else:
            self._event_loop = asyncio.new_event_loop()
            self._event_loop_thread = Thread(target=self._run_event_loop,
                                             args=(self._event_loop,))
            self.ble = BLEConnection(self._event_loop)

    def start(self):
        """Starts up the device connection."""
        LOGGER.info("DeviceConnection start")

        if not self.simulation:
            self._event_loop_thread.start()

    def stop(self):
        """Stops the device connection."""
        LOGGER.info("DeviceConnection stop")

        if not self.simulation:
            LOGGER.info("stopping event loop")
            self._event_loop.call_soon_threadsafe(self._event_loop.stop)
            self._event_loop_thread.join(timeout=2.0)

            if self._event_loop_thread.is_alive():
                LOGGER.error("failed to join event loop thread")

    """
    Public (GCI proxy)
    """

    def discover(self, callback: callable):
        """
        Discovers devices in the local HOME network and returns them by
        calling the provided callback.
        """
        if self.simulation:
            self.sim.discover(callback)
        else:
            self.ble.discover(callback)

    def is_connected(self, device: Device) -> bool:
        """
        Returns True if the device is already connected.
        """
        return (self.sim.is_connected(device) if self.simulation
                else self.ble.is_connected(device))

    def connect(self, device: Device) -> bool:
        """
        Returns True if the device was successfully connected to.
        """
        return (self.sim.connect(device) if self.simulation
                else self.ble.connect(device))

    def notify(self, callback: callable, device: Device):
        """
        Returns True if the device was successfully connected to.
        """
        if self.simulation:
            self.sim.notify(callback, device)
        else:
            self.ble.notify(callback, device)

    """
    Private
    """

    @staticmethod
    def _run_event_loop(event_loop):
        """Runs the event loop."""
        LOGGER.info("DeviceConnection run event loop")
        event_loop.run_forever()
        LOGGER.info("event loop stopped")
