import asyncio
import logging

from threading import Thread

from defs import CLI_SIMULATION
from app.device.connection.ble.connection import BLEConnection
from app.device.connection.sim.connection import SimConnection


LOGGER = logging.getLogger(__name__)


class DeviceConnection:

    def __init__(self, cli_args):
        if cli_args.get(CLI_SIMULATION):
            self.simulation = True
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
            disconnected = self.ble.disconnect_all()
            if not disconnected:
                LOGGER.error("failed to disconnect some BLE device")

            self._event_loop.call_soon_threadsafe(self._event_loop.stop)
            self._event_loop_thread.join()

            if self._event_loop_thread.is_alive():
                LOGGER.error("failed to join event loop thread")

    @staticmethod
    def _run_event_loop(event_loop):
        """Runs the event loop."""
        LOGGER.info("DeviceConnection run event loop")
        event_loop.run_forever()
