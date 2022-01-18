import logging
import threading
import time

from app.device import DeviceApp
from app.hint import HintApp
from util.storage import DataStore

LOGGER = logging.getLogger(__name__)


class Hume:

    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.storage = DataStore()
        self.device = DeviceApp(cli_args, self.storage)
        self.hint = HintApp(cli_args, self.storage)

    def start(self):
        """Starts the HUME."""
        LOGGER.info("Hume start")

        self.storage.start()

        self.device.pre_start()
        self.hint.pre_start()

        self.device.start()
        self.hint.start()

        self.device.post_start()
        self.hint.post_start()

        time.sleep(1)
        print("# THREADING")
        print(f"# Active threads: {threading.active_count()}")
        print("# List of threads:")
        for thread in threading.enumerate():
            print(f"# {thread}")

    def stop(self):
        """Stops the HUME."""
        LOGGER.info("Hume stop")

        self.device.pre_stop()
        self.hint.pre_stop()

        self.device.stop()
        self.hint.stop()

        self.device.post_stop()
        self.hint.post_stop()
