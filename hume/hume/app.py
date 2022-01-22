import logging

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

        self.device.register_callback(self._on_device_message)
        self.hint.register_callback(self._on_hint_message)

        self.device.post_start()
        self.hint.post_start()

    def stop(self):
        """Stops the HUME."""
        LOGGER.info("Hume stop")

        self.device.pre_stop()
        self.hint.pre_stop()

        self.device.stop()
        self.hint.stop()

        self.device.post_stop()
        self.hint.post_stop()

    """
    Private
    """

    def _on_device_message(self, device, msg_type, msg):
        """
        Registered to be called by the Device app when a new message is
        received from a connected device.
        """
        LOGGER.debug("HUME handling device message")

    def _on_hint_message(self, msg_type, msg):
        """
        Registered to be called by the Hint app when a new message is received
        from HINT.
        """
        LOGGER.debug("HUME handling HINT message")
