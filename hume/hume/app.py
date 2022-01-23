import logging

from app.abc import StartError
from app.device import DeviceApp, DeviceMessage
from app.hint import HintApp, HintMessage
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

        # Register callbacks prior to starting Apps in case of any
        # confirmation-type messages happen on connection establishment, or in
        # case of queued up messages from HINT.
        self.device.register_callback(self._on_device_message)
        self.hint.register_callback(self._on_hint_message)

        try:
            self.device.start()
            self.hint.start()
        except StartError:
            self.device.stop()
            self.hint.stop()
            raise RuntimeError("failed to start an app")

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

        if msg_type == DeviceMessage.ACTION_STATEFUL:
            pass

        elif msg_type == DeviceMessage.CAPABILITY:
            pass

        else:
            LOGGER.warning(f"got message from device {device.uuid[:4]} of an "
                           f"unknown type: {msg_type}, msg: {msg}")

    def _on_hint_message(self, msg_type, msg):
        """
        Registered to be called by the Hint app when a new message is received
        from HINT.
        """
        LOGGER.debug("HUME handling HINT message")

        if msg_type == HintMessage.DISCOVER_DEVICES:
            pass

        elif msg_type == HintMessage.ATTACH_DEVICE:
            pass

        elif msg_type == HintMessage.DETACH:
            pass

        elif msg_type == HintMessage.UNPAIR:
            pass

        elif msg_type == HintMessage.ACTION_STATEFUL:
            pass

        else:
            LOGGER.warning(f"got message from hint of an unknown type: "
                           f"{msg_type}, msg: {msg}")
