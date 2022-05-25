from __future__ import annotations

import functools
import logging

from typing import Union

from app.abc import App
from app.device.connection.aggregator import ConnectionAggregator
from app.device.connection.gdci import GDCI
from app.device.models import Device
from app.device.connection.defs import DeviceMessage
from util.storage import DataStore


LOGGER = logging.getLogger(__name__)


class DeviceApp(App):

    def __init__(self, cli_args: dict, storage: DataStore):
        super().__init__()
        self.storage = storage
        self.aggregator = ConnectionAggregator(cli_args)

        self._registered_callback = lambda device, msg_type, msg: \
            LOGGER.warning("no registered callback to propagate device msg to")

    """
    App LCM
    """

    def pre_start(self):
        LOGGER.info("device app pre_start")

        self.storage.register(Device)

    def start(self):
        LOGGER.info("device app start")
        self.aggregator.start()
        self._connect_attached_devices()

    def post_start(self):
        LOGGER.info("device app post_start")

    def pre_stop(self):
        LOGGER.info("device app pre_stop")

    def stop(self):
        LOGGER.info("device app stop")
        self.aggregator.stop()

    def post_stop(self):
        LOGGER.info("device app post_stop")

    """
    Public
    """

    def register_callback(self, callback: callable):
        """
        Registers a callback with the device app to be called when a device has
        sent the HUME a message.

        callback: callable(Device, int, bytearray)
        """
        LOGGER.info("registering callback")
        self._registered_callback = callback

    def discover(self, callback: callable):
        """
        Discovers devices in the HUME's local area.
        """
        LOGGER.info("discovering devices")
        cb = functools.partial(self._devices_discovered, callback=callback)
        self.aggregator.discover(cb)

    def request_capabilities(self, device: Device) -> bool:
        """
        Requests capabilities of the input device, usually the start of an
        attach procedure. Returns True if the request could be sent.
        """
        LOGGER.info(f"requesting device {device.uuid[:4]} capabilities")
        if self._connect_to(device):
            LOGGER.info("connected, requesting capabilities")
            return self._request_capabilities(device)

        return False

    def detach(self, device: Device):
        """
        Detach the input device, disconnect and forget it.
        """
        LOGGER.info(f"detaching device {device.uuid[:4]}")
        if self.aggregator.is_connected(device):
            self.aggregator.disconnect(device)
            # not much to do if this fails, at least the device won't be
            # connected to again on start.

        self.storage.delete(device)

    def stateful_action(self, device: Device, group_id: int, state_id: int):
        """
        Sends a stateful action request to the device.
        """
        LOGGER.debug(f"sending device {device.uuid[:4]} a stateful action "
                     f"request")
        message = GDCI.Message(
            f"{DeviceMessage.ACTION_STATEFUL.value}{group_id}{state_id}"
        )
        self.aggregator.send(message, device)

    def action_states(self, device: Device):
        """
        Fetch all stateful action (current) states.
        """
        LOGGER.debug(f"sending device {device.uuid[:4]} a request for all of "
                     f"its current stateful action states")
        message = GDCI.Message(
            f"{DeviceMessage.ACTION_STATES.value}"
        )
        self.aggregator.send(message, device)

    def reset(self):
        """
        Resets the device application.
        """
        LOGGER.info("resetting the device application...")
        self.aggregator.disconnect_all()
        self.storage.delete_all(model=Device)

    """
    Private
    """

    def _devices_discovered(self,
                            devices: [Device],
                            callback: callable):
        """
        Called when a device (or more) has been discovered.
        """
        for device in devices:
            self.storage.set(device)

        callback(devices)

    def _on_device_message(self,
                           device: Device,
                           message_type: Union[
                               DeviceMessage.ACTION_STATEFUL.value,
                               DeviceMessage.CAPABILITY.value
                           ],
                           body: bytearray):
        """
        Called when a connected device sends HUME a message.
        """
        LOGGER.debug(f"received device message from {device.uuid[:4]}")
        self._registered_callback(device, message_type, body)

    def _connect_attached_devices(self):
        """
        Establishes a connection with all attached devices.
        """
        LOGGER.info("connecting attached devices")

        devices = self.storage.get_all(Device)
        for device in devices:
            if device.attached:
                self._connect_to(device)

    def _connect_to(self, device: Device) -> bool:
        """
        Checks if the input device is already connected. If not, the device
        is connected to.
        """
        LOGGER.debug(f"connecting to device {device.uuid[:4]}")

        if not self.aggregator.is_connected(device):
            if not self.aggregator.connect(device):
                LOGGER.error(f"failed to connect to device "
                             f"{device.uuid[:4]}")
                return False

            self.aggregator.notify(self._on_device_message, device)

        return True

    def _request_capabilities(self, device: Device) -> bool:
        """
        Requests the capabilities of the input device.
        """
        message = GDCI.Message(f"{DeviceMessage.CAPABILITY.value}")
        return self.aggregator.send(message, device)
